import random


deck_options = [
    {
      "id": "armor",
      "name": "Armor",
      "effect": "Reduces damage from ICE attacks.",
      "capability": "Reduces damage by 2d6"
    },
    {
      "id": "shield",
      "name": "Shield",
      "effect": "Blocks or deflects certain ICE attacks.",
      "capability": "Negates specific attacks"
    },
    {
      "id": "flak",
      "name": "Flak",
      "effect": "Destroys incoming Black ICE programs before they can strike.",
      "capability": "Preemptively neutralizes Black ICE"
    },
    {
      "id": "mirror",
      "name": "Mirror",
      "effect": "Reflects attacks back at the Black ICE, damaging or disabling it.",
      "capability": "Reflects damage or effects"
    },
    {
      "id": "cloak",
      "name": "Cloak",
      "effect": "Prevents detection by ICE, allowing the netrunner to sneak past.",
      "capability": "Stealth and evasion"
    },
    {
      "id": "zap",
      "name": "Zap",
      "effect": "Attacks and damages Black ICE programs.",
      "capability": "1d6 damage to Black ICE"
    },
    {
      "id": "speedy_gonzalvez",
      "name": "Speedy Gonzalvez",
      "effect": "Enhances the netrunner’s speed, enabling them to evade ICE.",
      "capability": "Improves action priority"
    },
    {
      "id": "neural_buffers",
      "name": "Neural Buffers",
      "effect": "Absorbs damage from Black ICE programs, protecting the netrunner.",
      "capability": "Damage reduction for physical harm"
    },
    {
      "id": "pain_editors",
      "name": "Pain Editors",
      "effect": "Suppresses pain caused by Black ICE, allowing continued functionality.",
      "capability": "Negates physical pain effects"
    },
    {
      "id": "allied_netrunners",
      "name": "Allied Netrunners",
      "effect": "Provides distraction or support during ICE encounters.",
      "capability": "Splits ICE attention or counters attacks"
    },
    {
      "id": "decryption_software",
      "name": "Decryption Software",
      "effect": "Quickly cracks ICE defenses to reduce exposure time.",
      "capability": "Bypasses defenses faster"
    },
    {
      "id": "recon_programs",
      "name": "Recon Programs",
      "effect": "Scans the network for potential threats before entering.",
      "capability": "Identifies Black ICE and other obstacles"
    },
    {
      "id": "high_quality_cyberdeck",
      "name": "High-Quality Cyberdeck",
      "effect": "Improves resilience against ICE and enhances performance.",
      "capability": "Better damage mitigation and program execution"
    },
    {
      "id": "cut_and_run",
      "name": "Cut and Run",
      "effect": "Quickly logs the netrunner out of the system to avoid further harm.",
      "capability": "Emergency exit"
    },
    {
      "id": "ai_assistance",
      "name": "AI Assistance",
      "effect": "Provides automated support for managing ICE encounters.",
      "capability": "Handles ICE interactions efficiently"
    }
  ]


def new_player():
    player = {
        'health': 10,
        'deck': [
            random.choice(deck_options),
            random.choice(deck_options),
            random.choice(deck_options),
            random.choice(deck_options),
            random.choice(deck_options),
        ]
    }
    return player

def slow_down(by):
    print("You are slowed down by " + str(by) + " turns.")
    return by

def logged():
    print("Your actions are now under scrutiny by the system defenders.")
    print("The intrusion attempt is logged and stored for post-intrusion analysis.")
    print("You are being monitored by the system defenders.")
    return

def watch_dogged():
    print("Your actions are being monitored by the Watchdog program.")
    print("It does not immediately attack, but it assists other ICE programs.")
    print("You are being tracked by the system defenders.")
    return
