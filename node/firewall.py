import random
from colorama import Fore
from cool_print import cool_print

def firewall(_state):
    while True:
        cool_print("You encounter a corporate Firewall. You must make a choice:", new_line_after_print=True)
        cool_print("1. Attempt to hack the firewall")
        cool_print("2. Fleee.... eeeee.... eeeee....")

        choice = input("Enter your choice: ")
        if choice == '1':
            cool_print("You attempt to hack the firewall.")
            cool_print("Roll a 1d6 to determine the outcome. On 6 the firewall ends your mission here and now.")
            cool_print("Press any key to continue.")
            input()
            cool_print("")
            roll = random.randint(1, 6)
            cool_print("You rolled a " + str(roll) + ".")
            cool_print("")
            if roll == 6:
                cool_print("The firewall ends your mission here and now.")
                cool_print("You have failed.")
                _state.change_health(-_state.player['health'])
            else:
                cool_print("The firewall fails to stop you.")
                cool_print("You proceed further in your mission.")
                _state.complete_node()
                cool_print("Press any key to continue.")
                input()
            return
        elif choice == '2':
            cool_print("You successfully escape.")
            _state.jack_out()
            return
        else:
            cool_print("Invalid choice. Please try again.")
