import time
import random
import random
import sys
import os
from colorama import Fore

# Import cool_print from parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the parent directory at the beginning of sys.path
sys.path.insert(0, parent_dir)
from cool_print import cool_print

def competing_netrunner(_state):
    cool_print("You have encountered a competing netrunner.", new_line_after_print=True)

    # is he/she friendly?
    friendly = random.choice([True, False])
    if friendly:
        cool_print("The netrunner is friendly and offers to help you.")
        cool_print("TBD: Implement competing netrunner actions.")
        _state.complete_node()
    else: 
        cool_print("The netrunner is hostile and attempts to hack you.")
        cool_print("You must deal with the threat.")
        cool_print("TBD: Implement competing netrunner actions.")
        cool_print("Press any key to continue.")
        input()
        cool_print("You have dealt with the threat.")
        _state.complete_node()