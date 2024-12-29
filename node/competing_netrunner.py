import time
import random

def competing_netrunner(_state):
    print("You have encountered a competing netrunner.")

    # is he/she friendly?
    friendly = random.choice([True, False])
    if friendly:
        print("The netrunner is friendly and offers to help you.")
    else: 
        print("The netrunner is hostile and attempts to hack you.")
        print("You must deal with the threat.")
        print("TBD: Implement competing netrunner actions.")
        print("Press any key to continue.")
        input()
        print("You have dealt with the threat.")
        _state.complete_node()