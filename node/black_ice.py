import time
import random
import node
import sys
import os
from colorama import Fore

# Import cool_print from parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the parent directory at the beginning of sys.path
sys.path.insert(0, parent_dir)
from cool_print import cool_print

black_ice_programs = [
    {
      "id": "hellhound",
      "name": "Hellhound",
      "effect": "Tracks and burns the netrunner, causing real physical damage by overheating their neural link.",
      "damage": "2d6",
      "special": "Physical damage",
      "health": 30,
      "action": lambda _state: hellhound_action(_state)
    },
    {
      "id": "raven",
      "name": "Raven",
      "effect": "Attacks the netrunner’s programs, destroying or disabling them.",
      "damage": "Targets installed programs",
      "special": "Program destruction",
      "health": 25,
      "action": lambda _state: raven_action(_state)
    },
    {
      "id": "wisp",
      "name": "Wisp",
      "effect": "Stuns or slows the netrunner, reducing their speed and effectiveness.",
      "damage": "1d6",
      "special": "Reduces actions for a few turns",
      "health": 15,
      "action": lambda _state: wisp_action(_state)
    },
    # {
    #   "id": "kraken",
    #   "name": "Kraken",
    #   "effect": "Traps the netrunner in the system, making it difficult to log out or escape.",
    #   "damage": "1d6 per turn",
    #   "special": "Immobilization",
    #   "health": 40,
    #   "action": lambda _state: kraken_action(_state)
    # },
    # {
    #   "id": "scorpion",
    #   "name": "Scorpion",
    #   "effect": "Infects the netrunner’s cyberdeck with malware, causing corrupted data or disabled programs.",
    #   "damage": "1d6",
    #   "special": "Cyberdeck malfunction",
    #   "health": 20,
    #   "action": lambda _state: scorpion_action(_state)
    # },
    # {
    #   "id": "brainworm",
    #   "name": "Brainworm",
    #   "effect": "Attacks the netrunner’s interface, reducing their overall ability to interact with the system.",
    #   "damage": "Temporary reduction in Interface skill",
    #   "special": "Skill reduction",
    #   "health": 25,
    #   "action": lambda _state: brainworm_action(_state)
    # },
    # {
    #   "id": "bloodhound",
    #   "name": "Bloodhound",
    #   "effect": "Tracks the netrunner’s real-world location, often leading to physical confrontation.",
    #   "damage": "None",
    #   "special": "Physical location trace",
    #   "health": 20,
    #   "action": lambda _state: bloodhound_action(_state)
    # },
    # {
    #   "id": "doppelganger",
    #   "name": "Doppelganger",
    #   "effect": "Creates a fake system that mirrors the real one, causing the netrunner to waste time and resources.",
    #   "damage": "None (psychological confusion)",
    #   "special": "Decoy and misdirection",
    #   "health": 10,
    #   "action": lambda _state: doppleganger_action(_state)
    # }
  ]


def hellhound_action(_state):
    cool_print("You are being tracked by a Hellhound. You must make a choice:")
    cool_print("1. Face the hell hound")
    cool_print("2. Jack-out and escape. Continue to fight another day.")

    cool_print("Enter your choice: ", fore_color=Fore.YELLOW)
    choice = input()
    if choice == '2':
        cool_print("You escape just in time to evade the Hellhound.")
        cool_print("You live to fight another day.")
        exit()
    if choice == '1':
        cool_print("You face the Hellhound.")

        hh = black_ice_programs[0]
        player = _state._state['player']

        while (True): 
            if player['health'] <= 0:
                cool_print("You are defeated by the Hellhound.")
                cool_print("Game Over.")
                exit()
            if hh['health'] <= 0:
                break
            
            cool_print("Player Health: ", player['health'])
            cool_print("Hellhound Health: ", hh['health'])
            
            cool_print("Your turn to attack the Hellhound.")
            cool_print("roll 3d10 damage.")
            cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
            input()
            damage = random.randint(1, 10) + random.randint(1, 10) + random.randint(1, 10)
            cool_print("You deal " + str(damage) + " damage to the Hellhound.")
            hh['health'] -= damage
            cool_print("")
            cool_print("Hellhound attacks you.")
            cool_print("roll 2d6 damage.")
            cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
            input()
            damage = random.randint(1, 6) + random.randint(1, 6)
            cool_print("Hellhound deals " + str(damage) + " damage to you.", fore_color=Fore.RED)
            _state.change_health(-damage)
            cool_print("")
            cool_print("Press any key to continue.")
            input()
            cool_print("")
        
        cool_print("You defeated the Hellhound. This node is now secure and you can continue your mission.")

        _state.complete_node()

def raven_action(_state):
    cool_print("You are being attacked by a Raven. You must make a choice:")
    cool_print("1. Face the Raven")
    cool_print("2. Jack-out and escape. Continue to fight another day.")

    cool_print("Enter your choice: ", fore_color=Fore.YELLOW)
    choice = input()
    if choice == '2':
        cool_print("You escape just in time to evade the Raven.")
        cool_print("You live to fight another day.")
        exit()
    if choice == '1':
        cool_print("You face the Raven.")

        raven = black_ice_programs[1]
        player = _state._state['player']

        while (True): 
            if player['health'] <= 0:
                cool_print("You are defeated by the Raven.")
                cool_print("Game Over.")
                exit()
            if raven['health'] <= 0:
                break
            
            cool_print("Player Health: ", player['health'])
            cool_print("Raven Health: ", raven['health'])
            
            cool_print("Your turn to attack the Raven.")
            cool_print("roll 3d10 damage.")
            cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
            input()
            damage = random.randint(1, 10) + random.randint(1, 10) + random.randint(1, 10)
            cool_print("You deal " + str(damage) + " damage to the Hellhound.")
            raven['health'] -= damage
            cool_print("")
            cool_print("Raven attacks you and your installed programs.")
            cool_print("It rolls 1d6. On 5 and 6 your programs are destroyed.")
            cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
            input()
            roll = random.randint(1, 6)
            cool_print("Raven rolled a " + str(roll) + ".")
            if roll > 4:
                cool_print("Raven destroys your installed programs.", fore_color=Fore.RED)
                _state.destroy_programs()
                cool_print("But, you have now cleared this node.")
                break
            else:
                cool_print("Raven failed to destroy your installed programs.")
                cool_print("Press any key to continue.")
                input()
        
        cool_print("You defeated the Raven. This node is now secure and you can continue your mission.")

        _state.complete_node()

def wisp_action(_state):
    cool_print("You are being attacked by a Wisp. You must make a choice:")
    cool_print("1. Face the Wisp")
    cool_print("2. Jack-out and escape. Continue to fight another day.")

    cool_print("Enter your choice: ", fore_color=Fore.YELLOW)
    choice = input()
    if choice == '2':
        cool_print("You escape just in time to evade the Wisp.")
        cool_print("You live to fight another day.")
        exit()
    if choice == '1':
        cool_print("You face the Wisp.")

        wisp = black_ice_programs[2]
        player = _state._state['player']
        
        while (True): 
            if player['health'] <= 0:
                cool_print("You are defeated by the Wisp.", Fore.RED)
                cool_print("Game Over.", Fore.RED)
                exit()
            if wisp['health'] <= 0:
                break
            
            cool_print("Player Health: ", player['health'])
            cool_print("Wisp Health: ", wisp['health'])
            
            if player['stunned'] > 0:
                cool_print("You are stunned and miss this turn.")
                cool_print("Press any key to continue.")
                input()
                _state.unstun()
                continue
            else:
                cool_print("Your turn to attack the Wisp.")
                cool_print("roll 3d10 damage.")
                cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
                input()
                damage = random.randint(1, 10) + random.randint(1, 10) + random.randint(1, 10)
                cool_print("You deal " + str(damage) + " damage to the Wisp.")
                wisp['health'] -= damage
            
            cool_print("")
            cool_print("Wisp attacks you.")
            cool_print("Wisp rolls 1d6 damage.")
            cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
            input()
            damage = random.randint(1, 6)
            cool_print("Wisp deals " + str(damage) + " damage to you.", fore_color=Fore.RED)
            _state.change_health(-damage)
            cool_print("")
            cool_print("Wisp tries to stun you.")
            cool_print("It rolls 1d6. On 5 and 6 you are slowed down.")
            cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
            input()
            roll = random.randint(1, 6)
            cool_print("Wisp rolled a " + str(roll) + ".")
            if roll > 4:
                cool_print("Wisp stuns you. You will miss next turn", fore_color=Fore.RED)
                _state.stun(roll)
            cool_print("Press any key to continue.")
            input()
            cool_print("")

        cool_print("You defeated the Wisp. This node is now secure and you can continue your mission.")
        _state.complete_node()



def kraken_action(_state):
    cool_print("You are trapped by a Kraken. You must make a choice:")
    cool_print("1. Attempt to escape the trap")
    cool_print("2. Confront the Kraken")

    cool_print("Enter your choice: ", fore_color=Fore.YELLOW)
    choice = input()
    if choice == '1':
        cool_print("You attempt to escape the trap.")
        time.sleep(1)
        cool_print("The Kraken tightens its grip, making it difficult to escape.")
        time.sleep(1)
        cool_print("You struggle against the trap, but it seems to be getting stronger.")
        time.sleep(1)
        cool_print("You are immobilized by the Kraken.")
        time.sleep(1)
        cool_print("You are trapped in the system.")
        time.sleep(1)
        cool_print("Game Over.")
        exit()

def scorpion_action(_state):
    cool_print("You are being attacked by a Scorpion. You must make a choice:")
    cool_print("1. Attempt to evade the attack")
    cool_print("2. Confront the attacker")

    cool_print("Enter your choice: ", fore_color=Fore.YELLOW)
    choice = input()
    if choice == '1':
        cool_print("You attempt to evade the attack.")

def brainworm_action(_state):
    cool_print("You are being attacked by a Brainworm. You must make a choice:")
    cool_print("1. Attempt to evade the attack")
    cool_print("2. Confront the attacker")

    cool_print("Enter your choice: ", fore_color=Fore.YELLOW)
    choice = input()
    if choice == '1':
        cool_print("You attempt to evade the attack.")

def bloodhound_action(_state):
    cool_print("You are being tracked by a Bloodhound. You must make a choice:")
    cool_print("1. Attempt to evade the trace")
    cool_print("2. Confront the tracker")

def doppleganger_action(_state):
    cool_print("You are being attacked by a Doppelganger. You must make a choice:")
    cool_print("1. Attempt to evade the attack")
    cool_print("2. Confront the attacker")

    cool_print("Enter your choice: ", fore_color=Fore.YELLOW)
    choice = input()
    if choice == '1':
        cool_print("You attempt to evade the attack.")

## main function
def black_ice(_state):
    cool_print("You arrive at a node. Steam hisses in the empty virtual space as intrusion countermeasures begin to activate.")
    cool_print("")

    ice = random.choice(black_ice_programs)

    cool_print("You encounter a " + ice['name'] + " - a Black ICE program.", new_line_after_print=True)
    cool_print("Effect: " + ice['effect'])

    cool_print("")
    ice['action'](_state)
