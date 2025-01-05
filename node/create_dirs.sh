#!/usr/bin/env bash
#
# create_fake_root_with_users_fixed_small.sh
#
# Creates a fake Linux-like directory structure and generates 20 random users,
# each with a Documents & Downloads folder containing ~20 files. 
#
# Key fixes to avoid "Created directory:" becoming part of the path:
#   - We strip newlines/carriage returns from function arguments.
#   - We do not embed "Created directory:" in the path itself.
#   - We reduce user count and file count as requested.

set -e  # Exit on error

###############################################################################
# 1. PARSE ARGUMENT
###############################################################################
TARGET_DIR="$1"

if [ -z "$TARGET_DIR" ]; then
  echo "Usage: $0 /path/to/target"
  exit 1
fi

# Ensure the target directory exists
mkdir -p "$TARGET_DIR"

###############################################################################
# 2. HELPER FUNCTIONS
###############################################################################

# Safely combine TARGET_DIR + relative path, stripping any extra whitespace.
make_full_path() {
  # $1 is the relative path (e.g. "/home/username")
  # 1) Strip possible newlines from $1.
  local relpath
  relpath="$(echo "$1" | tr -d '\r\n')"
  
  # 2) Combine with TARGET_DIR
  echo "${TARGET_DIR}${relpath}"
}

# Create a directory
create_dir() {
  local fullpath
  fullpath="$(make_full_path "$1")"
  mkdir -p "$fullpath"
  echo "Created directory: $fullpath"
}

# Create/overwrite a file with content
create_file() {
  local filepath
  filepath="$(make_full_path "$1")"
  
  # The rest of the args go into the file content
  shift
  # Ensure parent directory
  mkdir -p "$(dirname "$filepath")"
  
  # -e interprets backslashes for newlines
  echo -e "$@" > "$filepath"
  echo "Created file: $filepath"
}

# Append lines to a file
append_to_file() {
  local filepath
  filepath="$(make_full_path "$1")"
  
  local text="$2"
  
  mkdir -p "$(dirname "$filepath")"
  echo "$text" >> "$filepath"
}

# Generate an alphanumeric random string (default length=8), 
# forcing a simple locale and ignoring invalid bytes.
rand_string() {
  local length="${1:-8}"
  # Force ASCII-only, ignoring locale issues
  local result
  result="$(LC_ALL=C tr -dc 'a-zA-Z0-9' < /dev/urandom 2>/dev/null | head -c "$length")"
  # Strip any stray newlines or carriage returns
  result="$(echo "$result" | tr -d '\n\r')"
  echo "$result"
}

# Create a minimal stub “executable”
create_stub_executable() {
  local path="$1"
  local content="${2:-"#!/usr/bin/env bash\necho 'Stub command.'"}"
  create_file "$path" "$content"
  
  local fullpath
  fullpath="$(make_full_path "$1")"
  chmod +x "$fullpath"
}

###############################################################################
# 3. CREATE THE CORE DIRECTORY STRUCTURE
###############################################################################

echo "=== Creating directory structure under: $TARGET_DIR ==="

create_dir "/bin"
create_dir "/boot"
create_dir "/dev"
create_dir "/etc"
create_dir "/home"
create_dir "/lib"
create_dir "/lib64"
create_dir "/media"
create_dir "/mnt"
create_dir "/opt"
create_dir "/proc"
create_dir "/root"
create_dir "/run"
create_dir "/sbin"
create_dir "/srv"
create_dir "/sys"
create_dir "/tmp"
create_dir "/usr"
create_dir "/var"

# Subdirectories under /usr
create_dir "/usr/bin"
create_dir "/usr/include"
create_dir "/usr/lib"
create_dir "/usr/local"
create_dir "/usr/sbin"
create_dir "/usr/share"
create_dir "/usr/src"

# Subdirectories under /var
create_dir "/var/cache"
create_dir "/var/lib"
create_dir "/var/lock"
create_dir "/var/log"
create_dir "/var/run"
create_dir "/var/spool"
create_dir "/var/tmp"

# Fake libraries
create_file "/lib/libc.so.6" "Fake C library - demonstration only"
create_file "/lib/libm.so.6" "Fake math library - demonstration only"
create_file "/lib64/ld-linux-x86-64.so.2" "Fake dynamic linker - demonstration only"

# Minimal stub executables
create_stub_executable "/bin/bash"     "#!/usr/bin/env bash\necho 'Stub Bash shell.'"
create_stub_executable "/bin/ls"       "#!/usr/bin/env bash\necho 'Stub ls command.'"
create_stub_executable "/sbin/ifconfig" "#!/usr/bin/env bash\necho 'Stub ifconfig command.'"
create_stub_executable "/usr/bin/hello" "#!/usr/bin/env bash\necho 'Hello from this environment!'"

###############################################################################
# 4. SYSTEM CONFIG FILES IN /etc
###############################################################################

echo "=== Creating system config files in /etc ==="

create_file "/etc/hostname" "test-host"
create_file "/etc/issue" "Welcome to ExampleOS 1.0\nKernel \\r on an \\m\n"
create_file "/etc/hosts" "127.0.0.1\tlocalhost\n::1\tlocalhost\n127.0.1.1\ttest-host\n"
create_file "/etc/resolv.conf" "# Sample resolv.conf\nnameserver 8.8.8.8\nnameserver 8.8.4.4\n"
create_file "/etc/fstab" \
"# <file system> <dir> <type> <options> <dump> <pass>\n"\
"proc\t/proc\tproc\tdefaults\t0\t0\n"\
"sysfs\t/sys\tsysfs\tdefaults\t0\t0\n"\
"tmpfs\t/tmp\ttmpfs\tdefaults\t0\t0\n"

create_file "/etc/network/interfaces" \
"auto lo\niface lo inet loopback\n\n"\
"allow-hotplug eth0\niface eth0 inet dhcp\n"

# Minimal base passwd/shadow/group
create_file "/etc/passwd" \
"root:x:0:0:root:/root:/bin/bash\n"\
"daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\n"\
"bin:x:2:2:bin:/bin:/usr/sbin/nologin\n"\
"sys:x:3:3:sys:/dev:/usr/sbin/nologin\n"\
"www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin\n"\
"nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin\n"

create_file "/etc/shadow" \
"root:\$6\$rootFAKE:18732:0:99999:7:::\n"\
"daemon:*:18732:0:99999:7:::\n"\
"bin:*:18732:0:99999:7:::\n"\
"sys:*:18732:0:99999:7:::\n"\
"www-data:*:18732:0:99999:7:::\n"\
"nobody:*:18732:0:99999:7:::\n"

create_file "/etc/group" \
"root:x:0:\n"\
"daemon:x:1:\n"\
"bin:x:2:\n"\
"sys:x:3:\n"\
"adm:x:4:\n"\
"www-data:x:33:\n"\
"nobody:x:65534:\n"

###############################################################################
# 5. GENERATE 20 RANDOM USERS
###############################################################################

USER_COUNT=20
START_UID=1001  # first generated user UID

echo "=== Generating $USER_COUNT random users (UID=$START_UID ..) ==="

create_random_user() {
  local uid="$1"

  # e.g. user + 4 random chars => userA1b2
  local random_suffix
  random_suffix="$(rand_string 4)"

  local uname="user${random_suffix}"
  # strip any leftover newline
  uname="$(echo "$uname" | tr -d '\n\r')"

  local gid="$uid"
  local home="/home/$uname"
  local shell="/bin/bash"

  # Add to /etc/passwd
  append_to_file "/etc/passwd" \
    "${uname}:x:${uid}:${gid}:${uname}:${home}:${shell}"

  # Add to /etc/group
  append_to_file "/etc/group" \
    "${uname}:x:${gid}:"

  # Fake password hash for /etc/shadow
  local fake_salt
  fake_salt="$(rand_string 8)"
  local fake_hash
  fake_hash="\$6\$$fake_salt\$$(rand_string 12)"

  append_to_file "/etc/shadow" \
    "${uname}:${fake_hash}:18732:0:99999:7:::"

  # Create the user's home directory
  create_dir "$home"

  echo "$uname"
}

###############################################################################
# 6. GENERATE DOCUMENTS & DOWNLOADS WITH 20 FILES EACH
###############################################################################

# We'll create 20 files in each directory, not 50 or 400
FILE_COUNT=20

generate_random_files_for_user() {
  local user_home="$1"
  local docs_dir="$user_home/Documents"
  local dwnl_dir="$user_home/Downloads"

  create_dir "$docs_dir"
  create_dir "$dwnl_dir"

  for i in $(seq 1 "$FILE_COUNT"); do
    # Random file names
    local fname_docs="doc_$(rand_string 6).txt"
    local fname_dwnl="download_$(rand_string 6).txt"

    # Random content
    local content_docs="DOC FILE #$i\nCreated: $(date -R)\nRandom: $(rand_string 12)"
    local content_dwnl="DOWNLOAD FILE #$i\nCreated: $(date -R)\nRandom: $(rand_string 12)"

    create_file "$docs_dir/$fname_docs" "$content_docs"
    create_file "$dwnl_dir/$fname_dwnl" "$content_dwnl"
  done
}

###############################################################################
# 7. MAIN LOOP: CREATE USERS & THEIR FILES
###############################################################################

CURRENT_UID="$START_UID"

for i in $(seq 1 "$USER_COUNT"); do
  new_user="$(create_random_user "$CURRENT_UID")"
  generate_random_files_for_user "/home/$new_user"
  CURRENT_UID=$(( CURRENT_UID + 1 ))
done

###############################################################################
# 8. FINISH UP
###############################################################################

echo
echo "=== Created $USER_COUNT users and their Documents/Downloads with $FILE_COUNT files each. ==="

echo
echo "Directory tree (if 'tree' is installed):"
tree "$TARGET_DIR" || echo "Install 'tree' to see the structure in a nice format."
