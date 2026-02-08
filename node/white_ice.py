import random
from colorama import Fore
from cool_print import cool_print

from . import black_ice
from . import battle

white_ice_programs = [
    {
        "id": "netwatch_scout",
        "name": "Netwatch Scout",
        "greeting": lambda _player: f"""
        Detects unauthorized activity and raises an alarm.
        You need to eliminate it before it alerts the defenders. 
        """, 
        "damage": lambda: 0,
        "special": "Summons Black ICE or alerts defenders",
        "health": 10, 
        "initiative": lambda: random.randint(1, 100) - 30,
        "actions": [
          {
            "name": "Raise Alarm",
            "type": "alert",
            "description": """Raises an alarm and summons Black ICE or alerts defenders.""",
            "attempt": lambda _state: random.randint(1, 100) > 75,
            "action_txt": """
            The Netwatch Scout detects your intrusion and raises an alarm.
            Black ICE programs are summoned to your location.
            """,
            "fail_txt": """
            The Netwatch Scout looks confused.
            It fails to detect your intrusion in this turn.
            """,
            "effect": lambda _state: black_ice.black_ice(_state),
            "ends_battle": True,
          }
        ]
    },
    {
      "id": "gatekeeper",
      "name": "Gatekeeper",
      "effect": "Slows down netrunners by imposing additional checks and encryption layers.",
      "damage": "None",
      "special": "Increases time required to complete actions",
      "health": 15,
        "action": lambda _state: gatekeeper_action(_state)
    },
    {
      "id": "watchdog",
      "name": "Watchdog",
      "effect": "Tracks netrunners and monitors their actions without immediately attacking.",
      "damage": "None",
      "special": "Logs netrunner activities and assists Black ICE",
      "health": 20,
        "action": lambda _state: watchdog_action(_state)
    },
    {
      "id": "warden",
      "name": "Warden",
      "effect": "Locks down specific parts of the system to prevent further intrusion.",
      "damage": "None",
      "special": "Creates barriers or locked nodes",
      "health": 25,
        "action": lambda _state: warden_action(_state)
    },
    {
      "id": "logger",
      "name": "Logger",
      "effect": "Records all actions within a system for post-intrusion analysis.",
      "damage": "None",
      "special": "Creates evidence trails of intrusion attempts",
      "health": 10,
        "action": lambda _state: logger_action(_state)
    },
    {
      "id": "tracer",
      "name": "Tracer",
      "effect": "Attempts to locate the physical location of the netrunner.",
      "damage": "None",
      "special": "Provides coordinates for physical retaliation",
      "health": 15,
        "action": lambda _state: tracer_action(_state)
    }
  ]

def gatekeeper_action(_state):
    cool_print("The Gatekeeper program imposes additional checks and encryption layers.")
    cool_print("You must navigate through the additional security measures.")
    cool_print("Roll a 1d6. If you roll 6 you are slowed down.")
    cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
    input()
    roll = random.randint(1, 6)
    cool_print("You rolled a " + str(roll) + ".")

    if roll == 6:
        cool_print("The Gatekeeper program slows down your actions.")
        cool_print("You must spend additional time to complete your tasks.")
        cool_print("You are slowed down by 1d6 turns.")
        cool_print("")
        roll = random.randint(1, 6)
        cool_print("You are slowed down by " + str(roll) + " turns but you complete the node.")
        _state.slow_down(roll)
        _state.complete_node()
        cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
        input()
    else:
        cool_print("The Gatekeeper program does not slow you down.")
        cool_print("You proceed further in your mission.")
        _state.complete_node()
        cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
        input()

def watchdog_action(_state):
    cool_print("The Watchdog program tracks your actions and monitors your intrusion attempt.")
    cool_print("Roll a 1d6 to determine the outcome. On 6 the watchdog catches your scent and follows you around, jumping to assist any Black ICE programs you may encounter.")
    cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
    input()
    roll = random.randint(1, 6)
    cool_print("You rolled a " + str(roll) + ".")
    cool_print("")
    if roll == 6:
        cool_print("The Watchdog program catches your scent and follows you around.")
        cool_print("It jumps to assist any Black ICE programs you may encounter.")
        _state.watch_dogged()
        _state.complete_node()
        cool_print("You have passed this node.")
        cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
        input()
    else:
        cool_print("The Watchdog program fails to catch your scent.")
        cool_print("You proceed further in your mission.")
        _state.complete_node()
        cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
        input()

def warden_action(_state):
    cool_print("The Warden program locks down specific parts of the system to prevent further intrusion.")
    cool_print("Roll a 1d6 to determine the outcome. On 6 you must deal with the locked nodes and barriers.")
    cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
    input()
    roll = random.randint(1, 6)
    cool_print("You rolled a " + str(roll) + ".")
    cool_print("")
    if roll == 6:
        cool_print("The Warden program locks down specific parts of the system.")
        cool_print("You are slowed down by 1d6 turns.")
        cool_print("")
        roll = random.randint(1, 6)
        cool_print("You are slowed down by " + str(roll) + " turns but you complete the node.")
        _state.slow_down(roll)
        _state.complete_node()
        cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
        input()
    else: 
        cool_print("The Warden program does not lock down the system.")
        cool_print("You proceed further in your mission.")
        _state.complete_node()
        cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
        input()

def logger_action(_state):
    cool_print("The Logger program records all actions within the system.")
    cool_print("Your intrusion attempts are logged and stored for post-intrusion analysis.")
    cool_print("Roll a 1d6 to determine the outcome. On 5 and 6 you are logged.")
    cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
    input()
    roll = random.randint(1, 6)
    cool_print("You rolled a " + str(roll) + ".")
    cool_print("")
    if roll > 4:
        cool_print("The Logger program logs your intrusion attempts.")
        cool_print("Your actions are now under scrutiny by the system defenders.")
        cool_print("You have cleared this node.")
        _state.logged()
        _state.complete_node()
        cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
        input()
    else:
        cool_print("The Logger program fails to log your intrusion attempts.")
        cool_print("You proceed further in your mission.")
        _state.complete_node()
        cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
        input()


def tracer_action(_state):
    cool_print("The Tracer program attempts to locate your physical location.")
    cool_print("You must evade the tracking attempt.")
    cool_print("")
    cool_print("You have a chance to avoid detection.")
    cool_print("Roll a 1d6 to determine the outcome. On 4, 5, and 6 you successfully evade the Tracer program.")
    cool_print("")

    roll = random.randint(1, 6)
    cool_print("You rolled a " + str(roll) + ".")

    if roll > 3:
        cool_print("You successfully evade the Tracer program.")
        _state.complete_node()
        cool_print("Press any key to continue.")
        input()
    else:
        cool_print("The Tracer program successfully locates your physical location.")
        cool_print("You must deal with the consequences in the physical world. But for now you have cleared this node and can continue with your mission.")
        cool_print("")
        _state.tracered()
        _state.complete_node()
        cool_print("Press any key to continue.")
        input()


## main function
def white_ice(_state):
    cool_print("You arrive at a node. Steam hisses in the empty virtual space as intrusion countermeasures begin to activate.")
    cool_print("")

    ice = random.choice(white_ice_programs)

    # Netwatch Scout uses the battle system; all others use direct action handlers
    if 'actions' in ice:
        battle.battle(_state._state['player'], ice, _state)
    else:
        cool_print(f"You encounter a {ice['name']}.")
        cool_print(ice['effect'])
        cool_print("")
        ice['action'](_state)
