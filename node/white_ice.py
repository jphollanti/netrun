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
    print("The Netwatch Scout detects your intrusion and raises an alarm.")
    print("Black ICE programs are summoned to your location.")
    print("You must deal with the incoming threat.")
    print("")
    black_ice.black_ice(_state)

def gatekeeper_action(_state):
    print("The Gatekeeper program imposes additional checks and encryption layers.")
    print("You must navigate through the additional security measures.")
    print("")
    print("The Gatekeeper program slows down your actions.")
    print("You must spend additional time to complete your tasks.")
    print("You are slowed down by 1d6 turns.")
    print("")
    roll = random.randint(1, 6)
    _state.slow_down(roll)
    print("")

def watchdog_action(_state):
    print("The Watchdog program tracks your actions and monitors your intrusion attempt.")
    print("It does not immediately attack, but it assists other ICE programs.")
    print("Your actions are being monitored.")
    _state.watch_dogged()
    print("")

def warden_action(_state):
    print("The Warden program locks down specific parts of the system to prevent further intrusion.")
    print("You must deal with the locked nodes and barriers.")
    print("")
    print("The Warden program creates barriers and locked nodes.")
    print("You must find a way to bypass or unlock them.")
    print("")

    roll = random.randint(1, 6)
    _state.slow_down(roll)

def logger_action(_state):
    print("The Logger program records all actions within the system.")
    print("Your intrusion attempt is logged and stored for post-intrusion analysis.")
    print("Your actions are now under scrutiny by the system defenders.")
    
    _state.logged()

def tracer_action(_state):
    print("The Tracer program attempts to locate your physical location.")
    print("You must evade the tracking attempt.")
    print("")
    print("You have a chance to avoid detection.")
    print("Roll a 1d6 to determine the outcome.")
    print("")

    roll = random.randint(1, 6)
    print("You rolled a " + str(roll) + ".")

    if roll > 3:
        print("You successfully evade the Tracer program.")
    else:
        print("The Tracer program successfully locates your physical location.")
        print("You must deal with the consequences.")
        print("")

        print("The Tracer program has alerted the system defenders to your location.")
        print(" ---- TODO: This should do something different ---- ")
        print("Black ICE programs are summoned to your location.")
        print("You must deal with the incoming threat.")
        print("")
        black_ice.black_ice(_state)


## main function
def white_ice(_state):
    print("You arrive at a node. Steam hisses in the empty virtual space as intrusion countermeasures begin to activate.")
    print("")

    ice = random.choice(white_ice_programs)

    print("You encounter a " + ice['name'] + " - a White ICE program.")
    print("Effect: " + ice['effect'])

    print("")
    ice['action'](_state)
