

def jack_in(_state):
    print("You are at the Jack-In point. You must make a choice:")
    print("1. Jack-In")
    print("2. Leave")
    choice = input("Enter your choice: ")
    if choice == '1':
        print("You jack into the system.")
        _state.complete_node()
    elif choice == '2':
        print("You leave the Jack-In point.")
        exit(0)
    else:
        print("Invalid choice. Please try again.")
        jack_in(_state)