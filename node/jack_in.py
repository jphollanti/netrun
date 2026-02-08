from colorama import Fore
import time
from cool_print import cool_print


def jack_in(_state):
    cool_print("You are at the Jack-In point. You must make a choice:")
    cool_print("1. Jack-In")
    cool_print("2. Leave")
    cool_print("Enter your choice: ", fore_color=Fore.YELLOW)
    choice = input()
    if choice == '1':
        cool_print("You jack into the system...")
        time.sleep(.5)
        cool_print("Your stomach turns as your conscious experience gets reduced to a stream of data.")
        time.sleep(.5)
        cool_print("And turns again as you re-emerge in the sterile virtual space of netrun.")
        time.sleep(.5)
        _state.complete_node()
    elif choice == '2':
        cool_print("You leave the Jack-In point.")
        exit(0)
    else:
        cool_print("Invalid choice. Please try again.")
        jack_in(_state)