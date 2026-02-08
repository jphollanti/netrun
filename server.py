#!/usr/bin/env python3
"""
Web server for Netrun — serves the game as a browser-based terminal.

Usage:
    python server.py [--host 0.0.0.0] [--port 8080]

The CLI game is unchanged. This module spawns mloop.py inside a
pseudo-terminal (pty) and bridges I/O over a WebSocket to an xterm.js
frontend, so every ANSI colour, cool_print animation, and getch() call
works exactly as it does in a real terminal.
"""

import argparse
import fcntl
import os
import select
import signal
import struct
import subprocess
import sys
import termios
import threading

from flask import Flask, send_from_directory
from flask_sock import Sock

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
sock = Sock(app)


# ── static file routes ──────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(os.path.join(BASE_DIR, "web"), "index.html")


@app.route("/css/<path:filename>")
def css(filename):
    return send_from_directory(os.path.join(BASE_DIR, "web", "css"), filename)


@app.route("/js/<path:filename>")
def js(filename):
    return send_from_directory(os.path.join(BASE_DIR, "web", "js"), filename)


# ── pty helpers ──────────────────────────────────────────────────────

def _set_pty_size(fd, cols, rows):
    """Resize the pty to *cols* x *rows*."""
    winsize = struct.pack("HHHH", rows, cols, 0, 0)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


# ── websocket handler ───────────────────────────────────────────────

@sock.route("/ws")
def terminal(ws):
    """One WebSocket connection = one game session in its own pty."""

    master_fd, slave_fd = os.openpty()

    # sensible defaults until the client sends a resize event
    _set_pty_size(master_fd, 120, 40)

    env = os.environ.copy()
    env["TERM"] = "xterm-256color"
    env["COLUMNS"] = "120"
    env["LINES"] = "40"

    process = subprocess.Popen(
        [sys.executable, os.path.join(BASE_DIR, "mloop.py")],
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        cwd=BASE_DIR,
        env=env,
        close_fds=True,
        preexec_fn=os.setsid,
    )
    os.close(slave_fd)

    # -- reader thread: pty → websocket --
    alive = threading.Event()
    alive.set()

    def _read_pty():
        while alive.is_set() and process.poll() is None:
            try:
                rlist, _, _ = select.select([master_fd], [], [], 0.05)
                if rlist:
                    data = os.read(master_fd, 4096)
                    if not data:
                        break
                    try:
                        ws.send(data.decode("utf-8", errors="replace"))
                    except Exception:
                        break
            except OSError:
                break

        # drain anything left in the buffer
        try:
            while True:
                rlist, _, _ = select.select([master_fd], [], [], 0.1)
                if rlist:
                    data = os.read(master_fd, 4096)
                    if data:
                        try:
                            ws.send(data.decode("utf-8", errors="replace"))
                        except Exception:
                            break
                    else:
                        break
                else:
                    break
        except OSError:
            pass

    reader = threading.Thread(target=_read_pty, daemon=True)
    reader.start()

    # -- main thread: websocket → pty --
    try:
        while process.poll() is None:
            try:
                msg = ws.receive(timeout=1)
            except Exception:
                break

            if msg is None:
                continue

            # resize messages arrive as e.g. "\x01R80,24"
            if isinstance(msg, str) and msg.startswith("\x01R"):
                try:
                    cols, rows = msg[2:].split(",")
                    _set_pty_size(master_fd, int(cols), int(rows))
                except (ValueError, OSError):
                    pass
                continue

            if isinstance(msg, str):
                msg = msg.encode("utf-8")

            try:
                os.write(master_fd, msg)
            except OSError:
                break
    except Exception:
        pass
    finally:
        alive.clear()
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except (ProcessLookupError, OSError):
            pass
        try:
            os.close(master_fd)
        except OSError:
            pass


# ── entry point ──────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Netrun Web Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    args = parser.parse_args()

    print(f"Netrun — http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port)
