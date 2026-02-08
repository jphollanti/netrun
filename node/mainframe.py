import time
import pty
import os
import subprocess
from colorama import Fore, Style, init
import select
import sys
import string
from datetime import datetime, timedelta
import random
from cool_print import cool_print
from cool_print import min_delay_provider

# Path for the access log
access_log_path = "/var/access_log"

MAIN_FRAME_FORE_COLOR = Fore.CYAN

# Generate a large list of fictional pages for access logs with page IDs
base_pages = [
    "/home/dashboard",
    "/home/reports",
    "/admin/settings",
    "/admin/users",
    "/finance/budget",
    "/finance/payroll",
    "/it/resources",
    "/it/security",
    "/hr/policies",
    "/hr/benefits"
]
pages_with_ids = [f"{page}?id={pid}" for page in base_pages for pid in range(1, 21)]
generic_pages = [f"/department{d}/resource{r}" for d in range(1, 21) for r in range(1, 11)]
pages = pages_with_ids + generic_pages
http_methods = ["GET", "POST", "PUT"]

# Function to generate random content for files
def random_content(file_type):
    if file_type == "document.txt":
        projects = ["AI Assistant", "Web Scraper", "Data Analysis Tool", "Weather App", "Game Engine"]
        selected_projects = random.sample(projects, k=random.randint(2, len(projects)))
        return f"This document contains information about user projects and ideas.\n\n" + "\n".join(f"- {project}" for project in selected_projects) + "\n"

    elif file_type == "notes.md":
        notes = ["Learn Python", "Explore machine learning libraries", "Set up development environment", "Master Docker", "Build portfolio website"]
        selected_notes = random.sample(notes, k=random.randint(2, len(notes)))
        return "# Notes\n\n" + "\n".join(f"- {note}" for note in selected_notes) + "\n"
    elif file_type == "config.json":
        themes = ["dark", "light", "blue", "green"]
        name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        email = f"{name.lower()}@example.com"
        return (
            "{\n"
            f"    \"settings\": {{\n"
            f"        \"theme\": \"{random.choice(themes)}\",\n"
            f"        \"notifications\": {random.choice(['true', 'false'])}\n"
            f"    }},\n"
            f"    \"user\": {{\n"
            f"        \"name\": \"{name}\",\n"
            f"        \"email\": \"{email}\"\n"
            "    }\n"
            "}\n"
        )
    elif file_type == "script.py":
        functions = ["greet", "calculate", "process"]
        selected_function = random.choice(functions)
        return f"# Sample Python Script\n\ndef {selected_function}():\n    print(\"Hello from {selected_function}!\")\n\nif __name__ == \"__main__\":\n    {selected_function}()\n"

    elif file_type == "logfile.log":
        actions = ["logged in", "accessed settings", "updated profile", "logged out"]
        return "\n".join(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] User {random.choice(actions)}"
            for _ in range(random.randint(3, 5))
        ) + "\n"

# Function to create sample files with randomized content in a user's directory
def create_sample_files_in_container(user_path):
    sample_files = ["document.txt", "notes.md", "config.json", "script.py", "logfile.log"]
    for file_name in sample_files:
        content = random_content(file_name)
        file_path = os.path.join(user_path, file_name)
        escaped_content = content.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$')
        command = f"echo \"{escaped_content}\" > {file_path}"
        run_command_in_container(command)

# Function to create random users and populate their directories in a Docker container
def create_users_and_files_in_container(num_users=44):
    run_command_in_container(f"mkdir -p {home_base_path}")

    for _ in range(num_users):
        username = generate_random_username()
        user_path = os.path.join(home_base_path, username)
        run_command_in_container(f"mkdir -p {user_path}")
        create_sample_files_in_container(user_path)
    
    user_path = os.path.join(home_base_path, "holljuhp")
    run_command_in_container(f"mkdir -p {user_path}")
    create_sample_files_in_container(user_path)

# Function to generate random usernames
def generate_random_username():
    return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=8))

# Function to generate access log entries directly in the Docker container
def generate_access_logs_in_container(num_entries=2000, custom_entry=None):
    log_entries = []

    # If a custom entry is provided, include it at a random position
    custom_added = False
    for i in range(num_entries):
        timestamp = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S")
        username = generate_random_username()
        page = random.choice(pages)
        access_type = "[ESCALATED ACCESS]" if random.random() < 0.1 else ""
        method = random.choice(http_methods)

        # Insert the custom entry at a random position if not already added
        if custom_entry and not custom_added and random.random() < 1 / (num_entries - i):
            log_entries.append(f"{timestamp} {custom_entry['username']} {custom_entry['method']} {custom_entry['url']} {custom_entry['access_type']}\n")
            custom_added = True

        log_entries.append(f"{timestamp} {username} {method} {page} {access_type}\n")
    
    if not custom_added and custom_entry:
        log_entries.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {custom_entry['username']} accessed {custom_entry['url']} {custom_entry['access_type']}\n")

    # Combine all log entries into a single string
    log_data = ''.join(log_entries)

    # Write directly to the Docker container

    escaped_content = log_data.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$')
    command = f"echo \"{escaped_content}\" > {access_log_path}"
    run_command_in_container(command)

home_base_path = "/home"

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
        # disable colors for ls and grep
        'echo "export LS_COLORS=\'di=34:fi=32\'" >> ~/.bashrc',
        'echo "alias ls=\'ls --color=never\'" >> ~/.bashrc',
        'echo "alias grep=\'grep --color=never\'" >> ~/.bashrc',

        'echo \'PS1=" # \\u\\$ (\\#): "\' >> ~/.bashrc',

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

    default_color = MAIN_FRAME_FORE_COLOR
    
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
                    print(f"{Fore.RED}Session terminated...{default_color}")
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
    def delay_provider(x, y):
        return [0.03, 0.1, 0.003, 0.01]
    
    cool_print("Welcome to the mainframe!")
    cool_print("A mainframe functions the same way as old terminal systems, with a Unix-like command line interface.", delay_provider=delay_provider, state=_state)
    cool_print("You have root access, meaning you can access any file on the server.", delay_provider=delay_provider, state=_state)
    cool_print("At any point type in 'mission' to get a reminder of your mission.", delay_provider=delay_provider, state=_state)
    cool_print("")

    cool_print("Mission Briefing:", state=_state)
    cool_print("Find a file called access_log and remove the entry with your clients username 'holljuhp'.", delay_provider=min_delay_provider, state=_state)
    cool_print("Do not to delete the entire access log file. This will raise suspicion.", delay_provider=min_delay_provider, state=_state)
    cool_print("You can use command \"sed -i '/holljuhp/d' access_log\" to delete lines from the file that contain holljuhp", delay_provider=min_delay_provider, state=_state)
    cool_print("You only get one try. Make it count. Good luck!", delay_provider=min_delay_provider, state=_state)
    cool_print("")

    cool_print("The folder structure in the mainframe is as follows:", delay_provider=delay_provider, state=_state)
    cool_print("  /", delay_provider=delay_provider, state=_state)
    cool_print("  ├── bin", delay_provider=delay_provider, state=_state)
    cool_print("  ├── dev", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── home", delay_provider=min_delay_provider, state=_state)
    cool_print("  │   ├── holljuhp", delay_provider=min_delay_provider, state=_state)
    cool_print("  │   │   ├── document.txt", delay_provider=min_delay_provider, state=_state)
    cool_print("  │   │   ├── notes.md", delay_provider=min_delay_provider, state=_state)
    cool_print("  │   │   ├── config.json", delay_provider=min_delay_provider, state=_state)
    cool_print("  │   │   ├── script.py", delay_provider=min_delay_provider, state=_state)
    cool_print("  │   │   └── logfile.log", delay_provider=min_delay_provider, state=_state)
    cool_print("  │   └── ... ", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── media", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── opt", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── root", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── sbin", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── sys", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── usr", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── boot", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── etc", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── lib", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── mnt", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── proc", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── run", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── srv", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── tmp", delay_provider=min_delay_provider, state=_state)
    cool_print("  ├── var", delay_provider=min_delay_provider, state=_state)

    t1 = "  │   └── access_log "
    t2 = "<-- Contains access logs. This is the file you're after!"
    color_map = {}
    for i in range(len(t2)):
        color_map[len(t1) + i] = Fore.YELLOW
    
    cool_print(t1 + t2, color_map=color_map, state=_state)
    time.sleep(.5)

    cool_print("")
    cool_print("Press any key to continue.", fore_color=Fore.YELLOW, state=_state)
    input()

    cool_print("Mainframe access initializing...", state=_state)
    time.sleep(.4)
    cool_print("Your senses numb as your consciousness is compressed into a stream of data.", state=_state)
    time.sleep(.4)
    cool_print("Your consciousness simplified into a command line interface.", state=_state)
    time.sleep(.4)
    # stopping any potential containers.
    res = run_cmd(command_rm)

    # starting a new container.
    res = run_cmd(command_start)

    # Mission help file
    fn = "/usr/bin/mission"
    file_contents =[
        "echo 'Mission Briefing:'",
        "echo 'Find a file called access_log and remove the entry with your clients username \'holljuhp\'.",
        "echo 'Do not to delete the entire access log file. This will raise suspicion.'",
        "echo 'You can use command \"sed -i \'/holljuhp/d\' access_log\" to delete lines from the file that contain \'holljuhp\'",
        "echo 'You only get one try. Make it count. Good luck!'",
    ]
    file_data = '\n'.join(file_contents)
    escaped_content = file_data.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$')
    command = f"echo \"{escaped_content}\" > {fn}"
    run_command_in_container(command)
    command = f"chmod +x {fn}"
    run_command_in_container(command)

    # Generate 500 log entries for the past 2 days
    log_entries = generate_log_entries(500)
    log_entries = "\n".join(log_entries)
    run_command_in_container(f"echo '{log_entries}' >> /var/log/alternatives.log")

    create_users_and_files_in_container(3)
    
    custom_entry = {
        "username": "holljuhp",
        "url": "/finance/payroll/path?id=42",
        "access_type": "[ESCALATED ACCESS]",
        "method": "POST",
    }
    generate_access_logs_in_container(300, custom_entry)

    # Call the function to enable settings in the Docker container
    set_container_settings()

    # create random session id from current date and time with length 7
    sesid = datetime.now().strftime("%m%d%H%M%S")[-7:]

    cool_print("Mainframe ready.")

    cool_print("")
    cool_print("Press any key to continue.", fore_color=Fore.YELLOW, state=_state)
    input()

    cool_print(" ############################################################### ", fore_color=MAIN_FRAME_FORE_COLOR, new_line_after_print=True, end='')
    time.sleep(.4)
    cool_print(f"                                                                ", end='')
    cool_print(f" # 33# # # !/Ex#3- # # Session #{sesid} # # dA!X$# # # #### # ##", fore_color=Fore.LIGHTRED_EX, end='')
    time.sleep(.4)
    cool_print(f"                                                                ", end='')
    cool_print(f" # 33# # # !/Ex#3- # # Session {sesid} ## # dA!X$# # # #### # ##", fore_color=MAIN_FRAME_FORE_COLOR)
    cool_print(" # ", fore_color=MAIN_FRAME_FORE_COLOR)
    cool_print(" # Session established ", fore_color=MAIN_FRAME_FORE_COLOR)
    cool_print(" # Type 'exit' to end the session ", fore_color=MAIN_FRAME_FORE_COLOR)
    cool_print(" ############################################################### ", fore_color=MAIN_FRAME_FORE_COLOR)
    cool_print("")

    try:
        exec_to_container()
    except Exception as e:
        print(f"Error: {e}")

    cool_print("Exited mainframe.")
    cool_print("You're back in the familiar virtual space of netrun...", delay_provider=min_delay_provider)
    cool_print("\"Breathing\" familiar virtual air.", delay_provider=min_delay_provider)
    cool_print("You feel liberated, like having escaped a dentists chair. ", delay_provider=min_delay_provider)
    time.sleep(.5)

    # check if the file with access logs exists
    res = run_cmd(["docker", "exec", "netrun", "ls", "/var"])
    # check if ls contains access_log
    if "access_log" in res.stdout:
        cool_print(f"Access log file still in place in mainframe. So far so good!", state=_state)

        # check if contents has holljuhp
        res = run_cmd(["docker", "exec", "netrun", "cat", access_log_path])
        if custom_entry["username"] in res.stdout:
            cool_print(f"Entry with {custom_entry['username']} found in access log file.", state=_state)
            cool_print("Mission failed!", state=_state)
            if _state:
                _state.complete_mission(False)
        else:
            cool_print(f"Entry with {custom_entry['username']} not found in access log file.", state=_state)
            cool_print("Good job! Mission accomplished!", state=_state)
            if _state:
                _state.complete_mission(True)
    else:
        cool_print("Access log file no longer present in mainframe.", state=_state)
        cool_print("Unfortunately, you removed the whole access log file. ", state=_state)
        cool_print("This creates too much noise and will result in further actions taken by the company.", state=_state)
        cool_print("They will find out the original file and it's contents.", state=_state)
        cool_print("Mission failed!", state=_state)
        if _state:
            _state.complete_mission(False)

if __name__ == "__main__":

    # Initialize Colorama
    init()
    mainframe(None)