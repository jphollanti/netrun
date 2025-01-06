import sys
import os

# Import cool_print from parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the parent directory at the beginning of sys.path
sys.path.insert(0, parent_dir)
from cool_print import cool_print

def data_core(state):
    cool_print("You are at the Data Core. ")
    cool_print("Still to implement.")
    state.complete_mission(True)