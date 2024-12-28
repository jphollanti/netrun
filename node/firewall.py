

def firewall(_state): 
    print("You encounter a corporate Firewall. You must make a choice:")
    print("1. Attempt to hack the firewall")
    print("2. Fleee")

    choice = input("Enter your choice: ")
    if choice == '1':
        print("You attempt to hack the firewall.")
        print("You successfully bypass the firewall.")
    elif choice == '2':
        print("You attempt to flee.")
        print("You successfully escape.")
        exit(0)
    else:
        print("Invalid choice. Please try again.")
        firewall(_state)

