import sys
import os
from colorama import Fore

# Import cool_print from parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the parent directory at the beginning of sys.path
sys.path.insert(0, parent_dir)
from cool_print import cool_print


def jack_in(_state):
    cool_print("You are at the Jack-In point. You must make a choice:")
    cool_print("1. Jack-In")
    cool_print("2. Leave")
    cool_print("Enter your choice: ", fore_color=Fore.YELLOW)
    choice = input()
    if choice == '1':
        cool_print("You jack into the system.")
        _state.complete_node()
    elif choice == '2':
        cool_print("You leave the Jack-In point.")
        exit(0)
    else:
        cool_print("Invalid choice. Please try again.")
        jack_in(_state)