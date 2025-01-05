import time
import pty
import os
import subprocess
from colorama import Fore, Style, init
import select
import sys

command_start = [
    "docker",
    "run",
    "-d",
    "--name", "netrun",
    "ubuntu:latest", 
    "tail", "-f", "/dev/null"
]

command_rm = [
    "docker",
    "rm",
    "-f",
    "netrun"
]

command_exec = [
    "docker",
    "exec",
    "-it",
    "netrun",
    "/bin/bash"
]

import random
from datetime import datetime, timedelta

# Predefined components for generating logs
commands = [
    "run with --install /usr/bin/awk awk /usr/bin/mawk 5 --slave /usr/share/man/man1/awk.1.gz awk.1.gz /usr/share/man/man1/mawk.1.gz --slave /usr/bin/nawk nawk /usr/bin/mawk --slave /usr/share/man/man1/nawk.1.gz nawk.1.gz /usr/share/man/man1/mawk.1.gz",
    "link group awk updated to point to /usr/bin/mawk",
    "run with --install /usr/bin/which which /usr/bin/which.debianutils 0 --slave /usr/share/man/man1/which.1.gz which.1.gz /usr/share/man/man1/which.debianutils.1.gz",
    "link group which updated to point to /usr/bin/which.debianutils",
    "run with --install /usr/share/man/man7/builtins.7.gz builtins.7.gz /usr/share/man/man7/bash-builtins.7.gz 10",
    "link group builtins.7.gz updated to point to /usr/share/man/man7/bash-builtins.7.gz",
    "run with --install /usr/sbin/rmt rmt /usr/sbin/rmt-tar 50 --slave /usr/share/man/man8/rmt.8.gz rmt.8.gz /usr/share/man/man8/rmt-tar.8.gz",
    "link group rmt updated to point to /usr/sbin/rmt-tar",
    "run with --remove builtins.7.gz /usr/share/man/man7/bash-builtins.7.gz",
    "link group builtins.7.gz fully removed",
    "auto-repair link group which",
    "auto-repair link group awk",
    "auto-repair link group rmt",
    "auto-repair link group pager",
]

# Function to generate a random timestamp within the past two days
def random_timestamp_within_past_2_days():
    now = datetime.now()
    past_2_days_start = now - timedelta(days=2)
    random_time = past_2_days_start + timedelta(seconds=random.randint(0, 2 * 24 * 3600))
    return random_time

# Function to generate random log entries
def generate_log_entries(num_entries=500):
    logs = []
    for _ in range(num_entries):
        timestamp = random_timestamp_within_past_2_days().strftime("%Y-%m-%d %H:%M:%S")
        command = random.choice(commands)
        log_entry = f"update-alternatives {timestamp}: {command}"
        logs.append(log_entry)
    return logs


def run_command_in_container(command):
    subprocess.run(["docker", "exec", "netrun", "bash", "-c", command], check=True)


def set_container_settings():
    # Commands to modify settings
    commands = [
        # Enable color for ls and other commands
        'echo "export LS_COLORS=\'di=34:fi=32\'" >> ~/.bashrc',
        'echo "alias ls=\'ls --color=never\'" >> ~/.bashrc',
        'echo "alias grep=\'grep --no-color\'" >> ~/.bashrc',

        # Set a colorful PS1 prompt
        'echo \'export PS1="\\[\\e[32m\\]\\u@\\h:\\[\\e[34m\\]\\w\\[\\e[0m\\]$ "\' >> ~/.bashrc',

        # Enable bracketed paste mode
        #'echo -e \'\\e[?2004h\' >> ~/.bashrc',

        # Set TERM to support color
        #'echo "export TERM=xterm-256color" >> ~/.bashrc',
    ]

    # Execute each command in the container
    for cmd in commands:
        run_command_in_container(cmd)

def exec_to_container():
    # Create a pseudo-terminal pair
    master, slave = pty.openpty()
    
    # Start the Docker exec command in the pseudo-terminal
    process = subprocess.Popen(
        command_exec,
        stdin=slave,
        stdout=slave,
        stderr=slave,
        text=True,
        bufsize=0,  # Unbuffered output
    )

    default_color = Fore.LIGHTBLACK_EX
    
    try:
        while True:
            # Use select to check if there is data to read
            rlist, _, _ = select.select([master], [], [], 0.1)
            
            if master in rlist:
                # Read and decode output from the Docker container
                output = os.read(master, 1024).decode('utf-8')
                if output:
                    # Print container response with a specific color
                    print(f"{default_color}{output}{default_color}", end='')

            # Check for user input to send to the container
            if select.select([sys.stdin], [], [], 0.1)[0]:
                user_input = input(f"{Fore.YELLOW}> {default_color}")  # Prompt in yellow
                
                if user_input.lower() in ["exit", "quit"]:
                    print(f"{Fore.RED}Exiting...{default_color}")
                    break
                
                # Send user input to the container
                os.write(master, (user_input + "\n").encode('utf-8'))
    except KeyboardInterrupt:
        print(f"{Fore.RED}\nSession terminated.{default_color}")
    finally:
        process.terminate()
        os.close(master)
        os.close(slave)


def run_cmd(command):
    try:
        return subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.strip()}")
        raise e


def mainframe(_state):
    print("Stopping any potential containers")
    res = run_cmd(command_rm)
    print(f"Result: {res.stdout.strip()}")

    print("Starting a new container")
    res = run_cmd(command_start)
    print(f"Result: {res.stdout.strip()}")

    time.sleep(.5)

    # Generate 500 log entries for the past 2 days
    log_entries = generate_log_entries(500)
    # concatenate log entries to string
    log_entries = "\n".join(log_entries)
    run_command_in_container(f"echo '{log_entries}' >> /var/log/alternatives.log")

    # Call the function to enable settings in the Docker container
    set_container_settings()

    print("Executing a shell in the container")
    exec_to_container()


if __name__ == "__main__":

    # Initialize Colorama
    init()
    mainframe(None)