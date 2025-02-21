import time
import random
import random
import sys
import os
from colorama import Fore
from . import battle

# Import cool_print from parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the parent directory at the beginning of sys.path
sys.path.insert(0, parent_dir)
from cool_print import cool_print


netrunner = {
    "id": "netrunner",
    "name": "Netrunner",
    "greeting": lambda _player: f"""
        A faint flicker in the data stream reveals a hooded figure formed from pixelated static. 
        Their visage morphs with each passing millisecond, like a glitch in reality. 
        Cipher’s disembodied voice crackles into your feed: "Hello, {_player['name']}... 
        Ready to dance with the devil in the data?"
    """,
    "health": 30,
    "initiative": lambda: random.randint(1, 100) + 12,
    "actions": [
        {
            "name": "Phantom Ping",
            "type": "damage",
            "description": """A barrage of lethal pings that slip through firewalls 
            to strike directly at the target’s neural link. Deals 2d6 damage.""",
            "roll": lambda: random.randint(1, 6) + random.randint(1, 6)
        },
        {
            "name": "Neural Surge",
            "type": "damage",
            "description": """Overloads the target’s nerve impulses with code-laced shock. 
            Deals 1d10 damage and stuns the target if a resistance check fails.""",
            "roll": lambda: random.randint(1, 10),
            "special": "Potential stun"
        },
        {
            "name": "Glitch Grenade",
            "type": "debuff",
            "description": """A digital distortion bomb that scrambles vision and aim. 
            The target takes a -2 penalty on all attack rolls for 2 turns.""",
            "roll": lambda: 0,
            "special": "-2 to attack for 2 turns"
        },
        {
            "name": "Stack Overflow",
            "type": "damage",
            "description": """Bombards the target’s system with junk data, dealing 1d8 damage 
            and forcing them to lose their next action if they roll under 4 on a d10.""",
            "roll": lambda: random.randint(1, 8),
            "special": "Chance to lose next action"
        },
        {
            "name": "Blackout",
            "type": "debuff",
            "description": """A cunning virus that shuts down sensory feeds. 
            The target’s chance to dodge is reduced by 3 for the next 2 rounds.""",
            "roll": lambda: 0,
            "special": "Dodge penalty"
        },
        {
            "name": "Payload Injection",
            "type": "damage",
            "description": """Plants malicious code, dealing 1d6 damage immediately 
            and 2 additional damage each turn for 3 turns.""",
            "roll": lambda: random.randint(1, 6),
            "residual": lambda _state: 2,
            "special": "Ongoing 2 damage (3 turns)"
        },
        {
            "name": "ICEbreaker",
            "type": "utility",
            "description": """Nullifies the target’s next defensive action 
            by bypassing their ICE protocols.""",
            "roll": lambda: 0,
            "special": "Negates next defense"
        },
        {
            "name": "Overclock",
            "type": "buff",
            "description": """Pushes Cipher’s rig to the limit, granting +5 Initiative 
            for the remainder of the encounter.""",
            "roll": lambda: 0,
            "special": "+5 Initiative"
        },
        {
            "name": "Reflective Shield",
            "type": "defensive",
            "description": """Cipher erects a protective code barrier. 
            The next attack targeting them is bounced back, dealing half damage 
            to the attacker.""",
            "roll": lambda: 0,
            "special": "Reflects half damage"
        },
        {
            "name": "Core Breach",
            "type": "damage",
            "description": """A cataclysmic hack that tears through the target’s operating core, 
            dealing 3d4 damage. Additional effect: temporary system shutdown if target’s health 
            is reduced below 5.""",
            "roll": lambda: random.randint(1, 4) + random.randint(1, 4) + random.randint(1, 4),
            "special": "Potential system shutdown"
        },
    ]
}

def competing_netrunner(_state):
    cool_print("You have encountered another netrunner.", new_line_after_print=True)
    gender = random.choice(['Male', 'Female'])
    cool_print("It starts as whisper in the void of cyberspace.")
    cool_print("A faint transparent cloud on a clear sky.")
    cool_print("Then it begins to grow... and grow.")
    cool_print("It takes form in a split second. You see another netrunner.")
    heshe = 'He' if gender == 'male' else 'She'
    cool_print(f"{heshe} gives you a short smile. ")
    cool_print("You both understand what's about to transpire.")
    cool_print("With luck you can ignore each other. But, if you're on the same mission...")
    cool_print("Only one can carry out the mission.")
    cool_print("And the other one must bow out.")
    cool_print("You have seen each other. You cannot ignore each other.")
    cool_print("")
    if gender == 'female':
        cool_print("This is not her real appearance. But it is a good approximation of her.")
        cool_print("You identify a person here, you identify a person outside.")
        cool_print("She's pretty. Young. Maybe 20s. Maybe 30s. Short blonde hair with neon highlights.")
        cool_print("She's wearing a black leather jacket. Blue eyes. A bit of a smirk.")
    if gender == 'male':
        cool_print("This is not his real appearance. But it is a good approximation of him.")
        cool_print("You identify a person here, you identify a person outside.")
        cool_print("He's tall. Maybe 30s. Maybe 40s. Black hair with neon highlights.")
        cool_print("He's wearing a black long sleeve shirt with matching neon lights. Brown eyes. A bit of a smirk.")
    
    cool_print("")
    cool_print(f"{heshe} turns to you. 'Your job ID?'")
    
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
    friendly = False
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
        cool_print("Makes it that much harder to turn the other one in.")
        _state.receive_program()
        _state.lose_program()
        _state.complete_node()
    else: 
        cool_print("Bad news. You are on the same job.")
        cool_print("You both curse your employer as you scramble to your decks.")
        cool_print("")
        cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
        input()
        cool_print("")
        battle.battle(_state._state['player'], netrunner, _state)
        
        cool_print("Press any key to continue.")
        input()
        cool_print("You have dealt with the threat.")
        _state.complete_node()