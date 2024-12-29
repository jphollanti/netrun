import random
from . import black_ice

white_ice_programs = [
    {
        "id": "netwatch_scout",
        "name": "Netwatch Scout",
        "effect": "Detects unauthorized activity and raises an alarm.",
        "damage": "None",
        "special": "Summons Black ICE or alerts defenders",
        "health": 10, 
        "action": lambda _state: netwatch_scout_action(_state)
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

def netwatch_scout_action(_state):
    print("The Netwatch Scout tries to detect your intrusion.")
    print("Roll a 1d6 to determine the outcome. On 5 and 6 you are detected.")
    print("Press any key to continue.")
    input()
    print("")
    roll = random.randint(1, 6)
    print("You rolled a " + str(roll) + ".")
    print("")
    if roll > 4:
      print("The Netwatch Scout detects your intrusion and raises an alarm.")
      print("Black ICE programs are summoned to your location.")
      print("Press any key to continue.")
      input()
      print("")
      black_ice.black_ice(_state)
    else:
      print("The Netwatch Scout fails to detect your intrusion.")
      print("You proceed further in your mission.")
      _state.complete_node()
      print("Press any key to continue.")
      input()

def gatekeeper_action(_state):
    print("The Gatekeeper program imposes additional checks and encryption layers.")
    print("You must navigate through the additional security measures.")
    print("Roll a 1d6. If you roll 6 you are slowed down.")
    print("Press any key to continue.")
    input()
    print("")
    roll = random.randint(1, 6)
    print("You rolled a " + str(roll) + ".")

    if roll == 6:
        print("The Gatekeeper program slows down your actions.")
        print("You must spend additional time to complete your tasks.")
        print("You are slowed down by 1d6 turns.")
        print("")
        roll = random.randint(1, 6)
        print("You are slowed down by " + str(roll) + " turns but you complete the node.")
        _state.slow_down(roll)
        _state.complete_node()
        print("Press any key to continue.")
        input()
    else:
        print("The Gatekeeper program does not slow you down.")
        print("You proceed further in your mission.")
        _state.complete_node()
        print("Press any key to continue.")
        input()

def watchdog_action(_state):
    print("The Watchdog program tracks your actions and monitors your intrusion attempt.")
    print("Roll a 1d6 to determine the outcome. On 6 the watchdog catches your scent and follows you around, jumping to assist any Black ICE programs you may encounter.")
    print("Press any key to continue.")
    input()
    print("")
    roll = random.randint(1, 6)
    print("You rolled a " + str(roll) + ".")
    print("")
    if roll == 6:
        print("The Watchdog program catches your scent and follows you around.")
        print("It jumps to assist any Black ICE programs you may encounter.")
        _state.watch_dogged()
        print("You have passed this node.")
        print("Press any key to continue.")
        input()
    else:
        print("The Watchdog program fails to catch your scent.")
        print("You proceed further in your mission.")
        _state.complete_node()
        print("Press any key to continue.")
        input()

def warden_action(_state):
    print("The Warden program locks down specific parts of the system to prevent further intrusion.")
    print("Roll a 1d6 to determine the outcome. On 6 you must deal with the locked nodes and barriers.")
    print("Press any key to continue.")
    input()
    print("")
    roll = random.randint(1, 6)
    print("You rolled a " + str(roll) + ".")
    print("")
    if roll == 6:
        print("The Warden program locks down specific parts of the system.")
        print("You are slowed down by 1d6 turns.")
        print("")
        roll = random.randint(1, 6)
        print("You are slowed down by " + str(roll) + " turns but you complete the node.")
        _state.slow_down(roll)
        _state.complete_node()
        print("Press any key to continue.")
        input()
    else: 
        print("The Warden program does not lock down the system.")
        print("You proceed further in your mission.")
        _state.complete_node()
        print("Press any key to continue.")
        input()

def logger_action(_state):
    print("The Logger program records all actions within the system.")
    print("Your intrusion attempts are logged and stored for post-intrusion analysis.")
    print("Roll a 1d6 to determine the outcome. On 5 and 6 you are logged.")
    print("Press any key to continue.")
    input()
    roll = random.randint(1, 6)
    print("You rolled a " + str(roll) + ".")
    print("")
    if roll > 4:
        print("The Logger program logs your intrusion attempts.")
        print("Your actions are now under scrutiny by the system defenders.")
        print("You have cleared this node.")
        _state.logged()
        _state.complete_node()
        print("Press any key to continue.")
        input()
    else:
        print("The Logger program fails to log your intrusion attempts.")
        print("You proceed further in your mission.")
        _state.complete_node()
        print("Press any key to continue.")
        input()


def tracer_action(_state):
    print("The Tracer program attempts to locate your physical location.")
    print("You must evade the tracking attempt.")
    print("")
    print("You have a chance to avoid detection.")
    print("Roll a 1d6 to determine the outcome. On 4, 5, and 6 you successfully evade the Tracer program.")
    print("")

    roll = random.randint(1, 6)
    print("You rolled a " + str(roll) + ".")

    if roll > 3:
        print("You successfully evade the Tracer program.")
        _state.complete_node()
        print("Press any key to continue.")
        input()
    else:
        print("The Tracer program successfully locates your physical location.")
        print("You must deal with the consequences in the physical world. But for now you have cleared this node and can continue with your mission.")
        print("")
        _state.logged()
        _state.complete_node()
        print("Press any key to continue.")
        input()


## main function
def white_ice(_state):
    print("You arrive at a node. Steam hisses in the empty virtual space as intrusion countermeasures begin to activate.")
    print("")

    ice = random.choice(white_ice_programs)

    print("You encounter a " + ice['name'] + " - a White ICE program.")
    print("Effect: " + ice['effect'])

    print("")
    ice['action'](_state)
