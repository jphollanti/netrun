/**
 * Netrun web terminal — connects xterm.js to the server over WebSocket.
 */
(function () {
  "use strict";

  var statusEl = document.getElementById("status");

  // ── create terminal ──────────────────────────────────────────
  var term = new Terminal({
    cursorBlink: true,
    cursorStyle: "block",
    fontSize: 15,
    fontFamily: "'Courier New', 'Consolas', monospace",
    theme: {
      background: "#0a0a0f",
      foreground: "#b0ffb0",
      cursor: "#00ff88",
      cursorAccent: "#0a0a0f",
      selectionBackground: "#00ff8844",
      black:   "#0a0a0f",
      red:     "#ff4444",
      green:   "#00ff88",
      yellow:  "#ffcc00",
      blue:    "#4488ff",
      magenta: "#cc44ff",
      cyan:    "#00cccc",
      white:   "#cccccc",
      brightBlack:   "#555555",
      brightRed:     "#ff6666",
      brightGreen:   "#66ff99",
      brightYellow:  "#ffdd44",
      brightBlue:    "#6699ff",
      brightMagenta: "#dd66ff",
      brightCyan:    "#44dddd",
      brightWhite:   "#ffffff",
    },
    scrollback: 1000,
    convertEol: true,
  });

  var fitAddon = new FitAddon.FitAddon();
  term.loadAddon(fitAddon);
  term.loadAddon(new WebLinksAddon.WebLinksAddon());

  term.open(document.getElementById("terminal"));
  fitAddon.fit();

  // ── websocket ────────────────────────────────────────────────
  var proto = location.protocol === "https:" ? "wss:" : "ws:";
  var wsUrl = proto + "//" + location.host + "/ws";
  var ws = null;
  var reconnectDelay = 1000;

  function connect() {
    ws = new WebSocket(wsUrl);

    ws.onopen = function () {
      statusEl.textContent = "ONLINE";
      statusEl.className = "status online";
      reconnectDelay = 1000;

      // tell server our current size
      sendResize();
    };

    ws.onmessage = function (ev) {
      term.write(ev.data);
    };

    ws.onclose = function () {
      statusEl.textContent = "DISCONNECTED";
      statusEl.className = "status offline";
      // auto-reconnect with back-off
      setTimeout(connect, reconnectDelay);
      reconnectDelay = Math.min(reconnectDelay * 2, 8000);
    };

    ws.onerror = function () {
      ws.close();
    };
  }

  // send keystrokes to server
  term.onData(function (data) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(data);
    }
  });

  // send resize events as a control message: \x01R<cols>,<rows>
  function sendResize() {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send("\x01R" + term.cols + "," + term.rows);
    }
  }

  term.onResize(function () {
    sendResize();
  });

  // re-fit when the browser window resizes
  window.addEventListener("resize", function () {
    fitAddon.fit();
  });

  connect();
})();
