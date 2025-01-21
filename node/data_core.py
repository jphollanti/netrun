import random
import os
from colorama import Fore, Back, Style, init
import getch
import subprocess
import sys
import os
import time

DATA_CORE_COLOR = Fore.RED

# Import cool_print from parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the parent directory at the beginning of sys.path
sys.path.insert(0, parent_dir)
from cool_print import cool_print
from cool_print import min_delay_provider

# Initialize Colorama
init(autoreset=True)

##############################################################################
# Flatten / Unflatten Utilities
##############################################################################
def flatten_table(table):
    """
    Flatten an R x C table into a single list of length R*C.
    In this version, table[r] is a list of length C. (No ID column.)
    """
    flat = []
    for row in table:
        flat.extend(row)
    return flat

def unflatten_table(table, flat):
    """
    Take a 'flat' list of length R*C and copy it back
    into the table, row by row.
    """
    rows = len(table)
    cols = len(table[0]) if rows > 0 else 0
    idx = 0
    for r in range(rows):
        for c in range(cols):
            table[r][c] = flat[idx]
            idx += 1

##############################################################################
# Main Game Functions
##############################################################################
def generate_table(rows, cols):
    """
    Generate a 2D table with `rows` rows and `cols` columns,
    all filled with random hex (like 0x12).
    (No ID column.)
    """
    table = []
    for _ in range(rows):
        row_data = [f"0x{random.randint(0, 255):02X}" for _ in range(cols)]
        table.append(row_data)
    return table

def place_pattern_plus_key(table, pattern, key):
    """
    Place `pattern` (4 chars => 4 hex cells) + `key` (4 chars => 4 hex cells)
    consecutively in the flattened table, possibly wrapping to the next row.
    No trimming: we assume there is enough space.
    """
    pattern_hex = [f"0x{ord(c):02X}" for c in pattern]  # 4 hex
    key_hex     = [f"0x{ord(c):02X}" for c in key]       # 4 hex
    combined = pattern_hex + key_hex                     # total 8 cells

    flat = flatten_table(table)
    n = len(flat)  # total cells
    needed = len(combined)  # 8 if pattern=PUZZ and key=XXXX

    if needed > n:
        raise ValueError("Pattern+Key require more cells than the table has!")

    max_start = n - needed
    start_index = random.randint(0, max_start)  # place at a random start

    # Insert them
    flat[start_index : start_index + needed] = combined
    unflatten_table(table, flat)

    return table

def print_table(table, sel_row, sel_col, 
                color_normal, color_selected, color_search,
                highlights=None):
    """
    Print the table with row coloring.  
    - We have `rows` x `cols` cells, no ID column.  
    - `highlights` is a set of (row, col) to color differently.  
    - If (r,c) == (sel_row, sel_col), we highlight as 'selected'.  
    - Otherwise, base row color is color_normal.  
    - After printing the cell, we re-apply color_normal to keep the row color for subsequent cells.
    """
    highlights = highlights or set()

    rows = len(table)
    cols = len(table[0]) if rows else 0

    header = "       "
    for c in range(cols):
        header += f"{c:^10}"
    cool_print(header, fore_color=DATA_CORE_COLOR, delay_provider=min_delay_provider)

    # Print each row
    for r in range(rows):
        # Start a new line; label the row index:
        row_str = f"{r:<6}"
        color_map = {}

        # For each column in that row
        for c in range(cols):
            cell_val = table[r][c]

            # If in highlights => color_search
            if (r, c) in highlights:
                # row_str += f"{Back.RED}{Fore.WHITE}{cell_val:^10}{Style.RESET_ALL}{color_normal}"
                row_str += f"{cell_val:^10}"
                st = c * 10 + 6
                for i in range(10):
                    color_map[st + i] = color_search
            # If this is the selected cell => color_selected
            elif r == sel_row and c == sel_col:
                #row_str += f"{color_selected}{cell_val:^10}{Style.RESET_ALL}{color_normal}"
                row_str += f"{cell_val:^10}"
                st = c * 10 + 6
                for i in range(10):
                    color_map[st + i] = color_selected
            else:
                #row_str += f"{color_normal}{cell_val:^10}{Style.RESET_ALL}"
                row_str += f"{cell_val:^10}"

        cool_print(row_str, color_map=color_map, fore_color=DATA_CORE_COLOR, delay_provider=min_delay_provider)
    cool_print()

def hex_to_ascii(hex_value):
    """
    Convert a hex string like '0x41' to its ASCII character if printable.
    """
    try:
        ascii_value = chr(int(hex_value, 16))
        if ascii_value.isprintable():
            return f"{Fore.GREEN}ASCII: {ascii_value} (decimal {ord(ascii_value)})"
        else:
            return f"{Fore.RED}Value is not a printable ASCII character."
    except ValueError:
        return f"{Fore.RED}Invalid hex value."

def validate_key(key_str):
    """
    Validate a 4-char uppercase/digit key.
    """
    if len(key_str) != 4:
        return False
    for ch in key_str:
        if not (ch.isdigit() or (ch.isalpha() and ch.isupper())):
            return False
    return True

##############################################################################
# Attempt to capture/restore console output (partial / not guaranteed)
##############################################################################
def capture_console_buffer_unix():
    """
    A naive attempt to capture current terminal contents on Unix systems:
      - uses 'tput' or 'clear' or 'stty' is not guaranteed to exist in all shells
      - for real solution, consider 'curses' or 'script' usage.
    Returns: (string) which hopefully contains something from screen
    """
    try:
        # 'reset' or 'clear' might do partial stuff, we try 'cat /dev/vcs' (on Linux console) 
        # or 'xtermcontrol' for xterm-based. This is not guaranteed to work everywhere.
        # Often you'd need sudo for /dev/vcsX. We'll just disclaim this is a hack.
        buffer_text = subprocess.check_output(["clear"]).decode()
        return buffer_text
    except Exception:
        return ""

def capture_console_buffer_windows():
    """
    A naive attempt on Windows. 
    Could call 'doskey /history' or use win32console. We'll disclaim partial success.
    """
    try:
        # This won't capture everything either.
        # We disclaim: there's no trivial way in standard Python to do so for the entire screen.
        buffer_text = subprocess.check_output("doskey /history", shell=True).decode()
        return buffer_text
    except Exception:
        return ""

def restore_console_output(saved_text):
    """
    Just re-print the saved_text. This doesn't truly restore the buffer,
    but attempts to re-display what was captured.
    """
    print(saved_text, end="")


def data_core(state):
    
    def delay_provider(x, y):
        return [0.03, 0.1, 0.003, 0.01]
    
    cool_print("You are at the Data Core!", delay_provider=delay_provider, state=state)
    cool_print("In the empty virtual space air seems to hum contently.", delay_provider=min_delay_provider, state=state)
    cool_print("Trillions inputs per second are carefully archived in the belly of this magnificent beast.", delay_provider=min_delay_provider, state=state)
    cool_print("The Data Core is the heart of the system, where all the information is stored.", delay_provider=min_delay_provider, state=state)
    cool_print("")
    cool_print("As you venture deeper into the empty space, small blinking lights pass you by.", delay_provider=min_delay_provider, state=state)
    cool_print("You know these are access points into specific data shard.", delay_provider=min_delay_provider, state=state)
    cool_print("Your client has equipped you with sensing software to find the right shard.", delay_provider=min_delay_provider, state=state)
    cool_print("The lights are cyan, but one blinks magenta. That's the one!", delay_provider=min_delay_provider, state=state)
    cool_print("You approach the magenta light and touch it.", delay_provider=min_delay_provider, state=state)
    cool_print("You are enveloped in deep magenta space.", delay_provider=min_delay_provider, state=state)
    cool_print("A hex grid appears in front of you.", delay_provider=min_delay_provider, state=state)
    cool_print("")
    cool_print("Your client has equipped you with 3 search string.", delay_provider=min_delay_provider, state=state)
    cool_print("You can use it find starting point for the key you need to extract.", delay_provider=min_delay_provider, state=state)
    cool_print("For example, if the search string is 'PUZ', and the key is 'ABCD',", delay_provider=min_delay_provider, state=state)
    cool_print("you would first find the starting point and then four consecutive cells that comprise the key.", delay_provider=min_delay_provider, state=state)
    cool_print("")
    cool_print("You can move around the hex grid using arrow keys.", delay_provider=min_delay_provider, state=state)
    cool_print("Press Enter to see the ASCII value of the hex cell you are on.", delay_provider=min_delay_provider, state=state)
    cool_print("Press S to search for a pattern.", delay_provider=min_delay_provider, state=state)
    cool_print("Press V to validate the key.", delay_provider=min_delay_provider, state=state)
    cool_print("Press Q to quit the program.", delay_provider=min_delay_provider, state=state)
    cool_print("")
    cool_print("You have 3 tries to validate the key.", delay_provider=delay_provider, state=state)
    cool_print("Good luck!", delay_provider=min_delay_provider, state=state)
    cool_print("")
    cool_print("Press any key to start...", fore_color=Fore.YELLOW)
    getch.getch()

    ROW_COUNT = 15
    COL_COUNT = 8

    color_normal    = Fore.MAGENTA       # normal cell text color
    #color_selected  = Back.YELLOW+Fore.BLACK  # selected cell
    color_selected  = Fore.YELLOW  # selected cell
    #color_search    = Back.RED+Fore.WHITE     # highlight matched search
    color_search    = Fore.CYAN     # highlight matched search
    

    cool_print(" --------------------------------------------------------------- ", fore_color=DATA_CORE_COLOR, new_line_after_print=True, end='')
    time.sleep(.4)
    cool_print(f"                                                                ", fore_color=DATA_CORE_COLOR, end='', delay_provider=min_delay_provider)
    cool_print(f" . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ", fore_color=DATA_CORE_COLOR)
    cool_print(" - ", fore_color=DATA_CORE_COLOR)
    cool_print(" # Press 'Q' to exit data core ", fore_color=DATA_CORE_COLOR, delay_provider=min_delay_provider)
    cool_print(" --------------------------------------------------------------- ", fore_color=DATA_CORE_COLOR)
    cool_print("")

    cool_print("Press any key to continue...", fore_color=Fore.YELLOW)
    getch.getch()

    # "fresh" screen
    os.system("cls" if os.name == "nt" else "clear")

    pattern = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=3))
    key = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4))

    table = generate_table(ROW_COUNT, COL_COUNT)

    # Place pattern+key
    table = place_pattern_plus_key(table, pattern, key)

    tries = 3

    selected_row, selected_col = 0, 0
    highlights = set()

    instructions = f"Press arrow keys to move, Enter=show ASCII, S=search, V=validate key, Q=quit."

    message = ""
    while True:
        # Clear screen each frame
        os.system("cls" if os.name == "nt" else "clear")

        # Print instructions + table
        cool_print(instructions, fore_color=DATA_CORE_COLOR, delay_provider=min_delay_provider)
        cool_print(f"Search pattern: {pattern}", fore_color=DATA_CORE_COLOR, delay_provider=min_delay_provider)
        cool_print("")
        print_table(
            table, selected_row, selected_col,
            color_normal, color_selected, color_search,
            highlights
        )
        if message:
            print(message)

        ch = getch.getch()
        if ch == '\x1b':  # ESC for arrow keys
            ignore = getch.getch()  # usually '['
            arrow = getch.getch()
            if arrow == 'A':  # Up
                selected_row = (selected_row - 1) % ROW_COUNT
            elif arrow == 'B':  # Down
                selected_row = (selected_row + 1) % ROW_COUNT
            elif arrow == 'D':  # Left
                selected_col = (selected_col - 1) % COL_COUNT
            elif arrow == 'C':  # Right
                selected_col = (selected_col + 1) % COL_COUNT

        elif ch in ('\r', '\n'):  # Enter => show ASCII
            hex_val = table[selected_row][selected_col]
            message = hex_to_ascii(hex_val)

        elif ch.lower() == 's':
            print(f"{Fore.CYAN}Enter an ASCII string to search:")
            search_string = input("> ").strip()
            if not search_string:
                message = f"{Fore.RED}Search string cannot be empty!"
            else:
                search_hex = [f"0x{ord(c):02X}" for c in search_string]
                # Flatten the table to find them
                flat = flatten_table(table)
                n = len(flat)
                m = len(search_hex)
                highlights.clear()

                found = False
                for start_i in range(n - m + 1):
                    if flat[start_i : start_i + m] == search_hex:
                        found = True
                        # Mark them in highlights
                        for off in range(m):
                            idx = start_i + off
                            # convert back to (row, col)
                            row_ = idx // COL_COUNT
                            col_ = idx % COL_COUNT
                            highlights.add((row_, col_))
                if found:
                    message = f"{Fore.GREEN}Matches highlighted."
                else:
                    message = f"{Fore.RED}No match found for '{search_string}'."

        elif ch.lower() == 'q':
            print(f"{Fore.RED}Exiting the program. Goodbye!")
            break

        elif ch.lower() == 'v':
            key_str = input(f"{Fore.CYAN}Enter a 4-character uppercase/digit key: ").strip()
            # compare with the current key
            if key_str == key:
                message = f"{Fore.GREEN}Key is correct! Key is: {key}. Remember it!"
                state.complete_mission(False)
                return 1
            else:
                tries -= 1
                if tries == 0:
                    print(f"{Fore.RED}Out of tries. Game over.")
                    state.complete_mission(False)
                    return -1
                message = f"{Fore.RED}Key is incorrect! Try again. Tries remaining: {tries}."
        # else: do nothing for other keys


def main():
    data_core(None)

# Run main if invoked directly
if __name__ == "__main__":
    main()
