import time
import random
import node

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
    {
      "id": "kraken",
      "name": "Kraken",
      "effect": "Traps the netrunner in the system, making it difficult to log out or escape.",
      "damage": "1d6 per turn",
      "special": "Immobilization",
      "health": 40,
      "action": lambda _state: kraken_action(_state)
    },
    {
      "id": "scorpion",
      "name": "Scorpion",
      "effect": "Infects the netrunner’s cyberdeck with malware, causing corrupted data or disabled programs.",
      "damage": "1d6",
      "special": "Cyberdeck malfunction",
      "health": 20,
      "action": lambda _state: scorpion_action(_state)
    },
    {
      "id": "brainworm",
      "name": "Brainworm",
      "effect": "Attacks the netrunner’s interface, reducing their overall ability to interact with the system.",
      "damage": "Temporary reduction in Interface skill",
      "special": "Skill reduction",
      "health": 25,
      "action": lambda _state: brainworm_action(_state)
    },
    {
      "id": "bloodhound",
      "name": "Bloodhound",
      "effect": "Tracks the netrunner’s real-world location, often leading to physical confrontation.",
      "damage": "None",
      "special": "Physical location trace",
      "health": 20,
      "action": lambda _state: bloodhound_action(_state)
    },
    {
      "id": "doppelganger",
      "name": "Doppelganger",
      "effect": "Creates a fake system that mirrors the real one, causing the netrunner to waste time and resources.",
      "damage": "None (psychological confusion)",
      "special": "Decoy and misdirection",
      "health": 10,
      "action": lambda _state: doppleganger_action(_state)
    }
  ]


def hellhound_action(_state):
    print("You are being tracked by a Hellhound. You must make a choice:")
    print("1. Attempt to evade the trace")
    print("2. Confront the tracker")

    choice = input("Enter your choice: ")
    if choice == '1':
        print("You attempt to evade the trace.")

def raven_action(_state):
    print("You are being attacked by a Raven. You must make a choice:")
    print("1. Attempt to evade the attack")
    print("2. Confront the attacker")

    choice = input("Enter your choice: ")
    if choice == '1':
        print("You attempt to evade the attack.")

def wisp_action(_state):
    print("You are being attacked by a Wisp. You must make a choice:")
    print("1. Attempt to evade the attack")
    print("2. Confront the attacker")

    choice = input("Enter your choice: ")
    if choice == '1':
        print("You attempt to evade the attack.")

def kraken_action(_state):
    print("You are trapped by a Kraken. You must make a choice:")
    print("1. Attempt to escape the trap")
    print("2. Confront the Kraken")

    choice = input("Enter your choice: ")
    if choice == '1':
        print("You attempt to escape the trap.")
        time.sleep(1)
        print("The Kraken tightens its grip, making it difficult to escape.")
        time.sleep(1)
        print("You struggle against the trap, but it seems to be getting stronger.")
        time.sleep(1)
        print("You are immobilized by the Kraken.")
        time.sleep(1)
        print("You are trapped in the system.")
        time.sleep(1)
        print("Game Over.")
        exit()

def scorpion_action(_state):
    print("You are being attacked by a Scorpion. You must make a choice:")
    print("1. Attempt to evade the attack")
    print("2. Confront the attacker")

    choice = input("Enter your choice: ")
    if choice == '1':
        print("You attempt to evade the attack.")

def brainworm_action(_state):
    print("You are being attacked by a Brainworm. You must make a choice:")
    print("1. Attempt to evade the attack")
    print("2. Confront the attacker")

    choice = input("Enter your choice: ")
    if choice == '1':
        print("You attempt to evade the attack.")

def bloodhound_action(_state):
    print("You are being tracked by a Bloodhound. You must make a choice:")
    print("1. Attempt to evade the trace")
    print("2. Confront the tracker")

def doppleganger_action(_state):
    print("You are being attacked by a Doppelganger. You must make a choice:")
    print("1. Attempt to evade the attack")
    print("2. Confront the attacker")

    choice = input("Enter your choice: ")
    if choice == '1':
        print("You attempt to evade the attack.")

## main function
def black_ice(_state):
    print("You arrive at a node. Steam hisses in the empty virtual space as intrusion countermeasures begin to activate.")
    print("")

    ice = random.choice(black_ice_programs)

    print("You encounter a " + ice['name'] + " - a Black ICE program.")
    print("Effect: " + ice['effect'])

    print("")
    ice['action'](_state)
