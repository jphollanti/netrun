import os
import cmd
import getpass
import socket

try:
    import paramiko
    from scp import SCPClient
except ImportError:
    print("WARNING: paramiko and scp libraries not installed. SCP functionality won't be available.")
    print("Install with: pip install paramiko scp\n")

class MainFrame(cmd.Cmd):
    intro = "Welcome to MyShell! Type ? to list commands.\n"
    prompt = "(myshell) "

    def do_ls(self, arg):
        """List files in the current directory or in the provided path.
        Usage: ls [path]
        """
        path = arg if arg else "."
        try:
            files = os.listdir(path)
            for f in files:
                print(f)
        except OSError as e:
            print(f"Error: {e}")

    def do_cd(self, arg):
        """Change the current working directory.
        Usage: cd <path>
        """
        if not arg:
            print("Usage: cd <path>")
            return
        try:
            os.chdir(arg)
        except OSError as e:
            print(f"Error: {e}")

    def do_pwd(self, arg):
        """Print the current working directory."""
        print(os.getcwd())

    def do_cat(self, arg):
        """Display the contents of a file.
        Usage: cat <filename>
        """
        if not arg:
            print("Usage: cat <filename>")
            return

        try:
            with open(arg, "r") as file:
                print(file.read())
        except OSError as e:
            print(f"Error: {e}")

    def do_ip(self, arg):
        """
        Display the current IP address of this machine.

        By default, this tries to discover the primary outbound IP address by connecting
        a UDP socket to a public DNS server (8.8.8.8). If you have no internet connection
        or are on a private network, you may need to adjust this code or use
        a different approach.
        """
        try:
            # Method: Create a UDP socket to an external address (Google DNS)
            # and then read our own IP.
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                ip_address = s.getsockname()[0]
            print(f"My IP Address: {ip_address}")
        except Exception as e:
            print(f"Could not determine IP address: {e}")

    def do_scp(self, arg):
        """
        Securely copy a file between local and remote systems using SCP.
        Usage:
            scp upload   <local_path>   user@host:<remote_path>
            scp download user@host:<remote_path> <local_path>
        Example:
            scp upload myfile.txt user@192.168.1.10:/home/username/myfile.txt
            scp download user@192.168.1.10:/home/username/myfile.txt myfile.txt

        Note: This command prompts for an SSH password. Key-based auth is also possible
              but would require a more advanced implementation (e.g., setting up Paramiko keys).
        """
        if 'paramiko' not in globals() or 'SCPClient' not in globals():
            print("SCP functionality not available: paramiko/scp not installed.")
            return

        args = arg.split()
        if len(args) != 3:
            print("Usage:\n  scp upload   <local_path>   user@host:<remote_path>")
            print("  scp download user@host:<remote_path> <local_path>")
            return

        direction = args[0].lower()
        path1 = args[1]
        path2 = args[2]

        if direction == "upload":
            local_path = path1
            remote_info = path2
        elif direction == "download":
            remote_info = path1
            local_path = path2
        else:
            print("First argument must be 'upload' or 'download'.")
            return

        # Minimal parsing of user@host:/remote_path
        if "@" not in remote_info or ":" not in remote_info:
            print("Error: remote path must be in user@host:/path form.")
            return

        user_host, remote_path = remote_info.split(":", 1)
        if "@" not in user_host:
            print("Error: remote path must be in user@host:/path form.")
            return

        user, host = user_host.split("@", 1)

        # Prompt for password
        password = getpass.getpass(f"Password for {user}@{host}: ")

        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Accept unknown host keys automatically
        try:
            ssh.connect(hostname=host, username=user, password=password)
        except paramiko.SSHException as e:
            print(f"SSH connection error: {e}")
            return

        # Perform SCP
        with SCPClient(ssh.get_transport()) as scp:
            try:
                if direction == "upload":
                    scp.put(local_path, remote_path)
                    print(f"Uploaded {local_path} to {remote_info}.")
                else:  # download
                    scp.get(remote_path, local_path)
                    print(f"Downloaded {remote_info} to {local_path}.")
            except Exception as e:
                print(f"SCP error: {e}")

        # Close SSH session
        ssh.close()

    def do_exit(self, arg):
        """Exit the shell."""
        print("Goodbye!")
        return True

if __name__ == '__main__':
    MainFrame().cmdloop()
