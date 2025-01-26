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
    cool_print("You have encountered another netrunner.", new_line_after_print=True)
    gender = random.choice(['Male', 'Female'])
    cool_print("It starts as whisper in the void of cyberspace.")
    cool_print("A faint transparent cloud on a clear sky.")
    cool_print("Then it begins to grow... and grow.")
    cool_print("It takes form in a split second. You see another netrunner.")
    heshe = 'He' if gender == 'male' else 'She'
    cool_print(f"{heshe} gives you a short smile. ")
    cool_print("You both understand the dilemma and you cannot help but return the smile.")
    cool_print("Either you can ignore each other or if you find yourselves on the same mission...")
    cool_print("Only one can carry out the mission.")
    cool_print("You have seen each other. You cannot ignore each other.")
    cool_print("")
    cool_print(f"{heshe} turns to you. 'Your job ID?'")
    if gender == 'female':
        cool_print("This is not her real appearance. But it is a good approximation of her.")
        cool_print("You identify a person here, you identify a person outside.")
        cool_print("She's pretty. Young. Maybe 20s. Maybe 30s. Short blonde hair with neon highlights.")
        cool_print("She's wearing a black leather jacket. Blue eyes. A bit of a smirk.")
        cool_print("")
    if gender == 'male':
        cool_print("This is not his real appearance. But it is a good approximation of him.")
        cool_print("You identify a person here, you identify a person outside.")
        cool_print("He's tall. Maybe 30s. Maybe 40s. Black hair with neon highlights.")
        cool_print("He's wearing a black long sleeve shirt with matching neon lights. Brown eyes. A bit of a smirk.")
        cool_print("")
    
    cool_print("")
    cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
    input()
    cool_print("You breath in the virtual air. ")
    cool_print("And exhale.")
    cool_print("Per netrunner etiquette, you don't have a choice.")
    cool_print("You give your job ID.")
    cool_print("")
    cool_print("")

    # is he/she friendly?
    friendly = random.choice([True, False])
    if friendly:
        cool_print("Good news. You are not on the same job.")
        cool_print("You both nod at each other.")
        cool_print(f"{heshe} smiles a crooked smile. 'Good luck. Here, have this.'")
        cool_print(f"{heshe} sends you a file. It's a program.")
        cool_print("You nod back. 'Thanks. Take this.'")
        himher = 'him' if gender == 'male' else 'her'
        cool_print(f"You send one of your program's back to {himher}.")
        cool_print("Another netrunner protocol. If you part as friends, share your programs.")
        cool_print("This way, if either of you rat the other one out,")
        cool_print("the other one is carrying a program with past posession linking back to the other.")
        _state.receive_program()
        _state.lose_program()
        _state.complete_node()
    else: 
        cool_print("Bad news. You are on the same job.")
        cool_print("You both curse your employer as you scramble to your deck.")
        cool_print("")
        cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
        input()
        cool_print("")
        cool_print("TBD: Implement competing netrunner actions.")
        cool_print("Press any key to continue.")
        input()
        cool_print("You have dealt with the threat.")
        _state.complete_node()