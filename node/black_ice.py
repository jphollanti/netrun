import time
import random
import node
import sys
import os
from colorama import Fore

from . import battle

# Import cool_print from parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the parent directory at the beginning of sys.path
sys.path.insert(0, parent_dir)
from cool_print import cool_print

black_ice_programs = [
    {
      "id": "hellhound",
      "name": "Hellhound",
      "greeting": lambda _player: f"""
        A towering, jet-black construct shaped like a wolf, 
        its obsidian plating catching flickers of fire that 
        ripple across its form. Its eyes emit a cold, white 
        glare. In a harsh, mechanical rasp, it endlessly 
        echoes {_player['name']}, {_player['name']}, {_player['name']}...
        """, 
      "health": 30,
      "initiative": lambda: random.randint(1, 100) + 10,
      "actions": [
        {
          "name": "Fry",
          "effect": """Deals 2d6 physical damage directly to the Netrunner. 
          They also take additional 2 damage per turn until the end of the encounter.""",
          "roll": lambda: random.randint(1, 6) + random.randint(1, 6),
          "residual": lambda _state: 2,
          "special": "Additional physical damage"
        },
      ]
    },
    {
      "id": "raven",
      "name": "Raven",
      "greeting": lambda _player: f"""
        Attacks the netrunner’s programs, destroying or disabling them.
      """,
      "health": 25,
      "actions": [
        {
          "name": "Corrupt",
          "effect": """Deals 2d6 damage to the Netrunner's. Additionally may destroy netrunners programs.""",
          "roll": lambda: random.randint(1, 6) + random.randint(1, 6),
          "residual": lambda state: state.destroy_programs() if random.choice([True, False]) else 0,
          "special": "Program destruction"
        },
      ]
    },
    {
      "id": "wisp",
      "name": "Wisp",
      "greeting": lambda _player: f"""
        Stuns or slows the netrunner, reducing their speed and effectiveness.
      """,
      "health": 15,
      "initiative": lambda: random.randint(1, 100) - 10,
      "actions": [
        {
          "name": "Stun",
          "effect": """Deals damage in the virtual world, resulting in 1d6 physical damage.""",
          "roll": lambda: random.randint(1, 6),
          "residual": lambda state: state.stun() if random.choice([True, False]) else 0,
          "special": "Stuns the netrunner"
        },
      ]
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


def black_ice(_state):
    cool_print("You arrive at a node. Steam hisses in the empty virtual space as intrusion countermeasures begin to activate.")
    cool_print("")

    ice = random.choice(black_ice_programs)

    battle.battle(_state._state['player'], ice, _state)