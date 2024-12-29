import random

def firewall(_state): 
    print("You encounter a corporate Firewall. You must make a choice:")
    print("1. Attempt to hack the firewall")
    print("2. Fleee.... eeeee.... eeeee....")

    choice = input("Enter your choice: ")
    if choice == '1':
        print("You attempt to hack the firewall.")
        print("Roll a 1d6 to determine the outcome. On 6 the firewall ends your mission here and now.")
        print("Press any key to continue.")
        input()
        print("")
        roll = random.randint(1, 6)
        print("You rolled a " + str(roll) + ".")
        print("")
        if roll == 6:
            print("The firewall ends your mission here and now.")
            print("You have failed.")
            exit(0)
        else:
            print("The firewall fails to stop you.")
            print("You proceed further in your mission.")
            _state.complete_node()
            print("Press any key to continue.")
            input
    elif choice == '2':
        print("You successfully escape.")
        exit(0)
    else:
        print("Invalid choice. Please try again.")
        firewall(_state)

