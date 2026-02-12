import time
import random
from colorama import Fore
from cool_print import cool_print

from . import battle

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
          "type": "damage",
          "description": """Deals 2d6 physical damage directly to the Netrunner. 
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
        Attacks the netrunner's programs, destroying or disabling them.
      """,
      "health": 25,
      "initiative": lambda: random.randint(1, 100) + 5,
      "actions": [
        {
          "name": "Corrupt",
          "type": "damage",
          "description": """Deals 2d6 damage to the Netrunner's. Additionally may destroy netrunners programs.""",
          "roll": lambda: random.randint(1, 6) + random.randint(1, 6),
          "on_hit": lambda state: state.destroy_programs() if random.choice([True, False]) else None,
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
          "type": "damage",
          "description": """Deals damage in the virtual world, resulting in 1d6 physical damage.""",
          "roll": lambda: random.randint(1, 6),
          "special": "Stuns the netrunner"
        },
      ]
    },
    {
      "id": "kraken",
      "name": "Kraken",
      "greeting": lambda _player: f"""
        The virtual space around you ripples. Thick, ink-black tendrils
        emerge from every surface -- walls, floor, ceiling -- coiling and
        writhing with predatory patience. At the center of the mass, a
        single eye opens. It sees you, {_player['name']}. It has always
        seen you. The tendrils tighten.
        """,
      "health": 40,
      "initiative": lambda: random.randint(1, 100) + 20,
      "actions": [
        {
          "name": "Constrict",
          "type": "damage",
          "description": """The Kraken's tendrils wrap around your avatar,
          crushing and squeezing. Deals 1d6 damage and slows you down.""",
          "roll": lambda: random.randint(1, 6),
          "on_hit": lambda state: state.slow_down(random.randint(1, 3)),
          "special": "Immobilization"
        },
        {
          "name": "Drag Down",
          "type": "damage",
          "description": """The Kraken yanks you into the depths of the system.
          Layers of virtual reality close over you like dark water. Deals 2d6 damage.""",
          "roll": lambda: random.randint(1, 6) + random.randint(1, 6),
          "special": "High damage"
        },
        {
          "name": "Ink Cloud",
          "type": "damage",
          "description": """A burst of corrupted data blinds your interface.
          You struggle to make sense of anything. Deals 1d4 damage and stuns you.""",
          "roll": lambda: random.randint(1, 4),
          "special": "Stuns the netrunner"
        },
      ]
    },
    {
      "id": "scorpion",
      "name": "Scorpion",
      "greeting": lambda _player: f"""
        A segmented construct skitters across the data plane, its chrome
        carapace reflecting distorted images of your own face back at you.
        Its tail arcs overhead -- a syringe-like stinger dripping with
        luminous green code. It knows your deck, {_player['name']}. It
        wants what's inside.
        """,
      "health": 20,
      "initiative": lambda: random.randint(1, 100) + 8,
      "actions": [
        {
          "name": "Sting",
          "type": "damage",
          "description": """The Scorpion's tail whips forward, injecting corrupted
          code directly into your cyberdeck. Deals 1d6 damage and may corrupt
          one of your programs.""",
          "roll": lambda: random.randint(1, 6),
          "on_hit": lambda state: state.lose_program() if random.randint(1, 6) >= 4 else None,
          "special": "Program corruption"
        },
        {
          "name": "Malware Injection",
          "type": "damage",
          "description": """The Scorpion latches onto your data stream and pumps
          in a payload of self-replicating malware. Deals 1d4 damage now and
          1 damage per turn as the malware spreads.""",
          "roll": lambda: random.randint(1, 4),
          "residual": lambda _state: 1,
          "special": "Spreading malware"
        },
        {
          "name": "Tail Swipe",
          "type": "damage",
          "description": """A vicious sweep of the Scorpion's armored tail.
          Raw kinetic force in cyberspace. Deals 2d4 damage.""",
          "roll": lambda: random.randint(1, 4) + random.randint(1, 4),
          "special": "Physical damage"
        },
      ]
    },
    {
      "id": "brainworm",
      "name": "Brainworm",
      "greeting": lambda _player: f"""
        You feel it before you see it -- a pressure behind your eyes, a
        whisper in a language that isn't language. A thin, translucent worm
        of light coils through the data around you, phasing in and out of
        visibility. It's already in your interface, {_player['name']}.
        It's reading your thoughts. Or trying to.
        """,
      "health": 25,
      "initiative": lambda: random.randint(1, 100) + 5,
      "actions": [
        {
          "name": "Neural Drill",
          "type": "damage",
          "description": """The Brainworm burrows into your neural interface,
          scrambling your reflexes and motor control. Deals 1d8 damage and
          slows your reactions.""",
          "roll": lambda: random.randint(1, 8),
          "on_hit": lambda state: state.slow_down(1),
          "special": "Skill reduction"
        },
        {
          "name": "Mind Leech",
          "type": "damage",
          "description": """The Brainworm siphons processing power from your
          cyberdeck, feeding on your own computational resources.
          Deals 1d4 damage and stuns you.""",
          "roll": lambda: random.randint(1, 4),
          "special": "Stuns the netrunner"
        },
        {
          "name": "Synaptic Feedback",
          "type": "damage",
          "description": """The Brainworm redirects your own neural signals back
          at you in a cascading loop. Your body twitches in the real world.
          Deals 1d6 damage with residual echo damage.""",
          "roll": lambda: random.randint(1, 6),
          "residual": lambda _state: 1,
          "special": "Feedback loop"
        },
      ]
    },
    {
      "id": "bloodhound",
      "name": "Bloodhound",
      "greeting": lambda _player: f"""
        A low, digital growl reverberates through the node. A sleek canine
        form materializes, built from interlocking red polygons. It lowers
        its head, sniffing at the data trail you've left behind. It's not
        here to fight you, {_player['name']}. It's here to find you.
        The real you. The meat you.
        """,
      "health": 20,
      "initiative": lambda: random.randint(1, 100),
      "actions": [
        {
          "name": "Trace Signal",
          "type": "alert",
          "description": """The Bloodhound locks onto your connection signal
          and begins tracing it back to your physical location.""",
          "attempt": lambda _state: random.randint(1, 6) >= 4,
          "action_txt": """
          The Bloodhound's eyes flash red. It has your signal.
          Your physical location is being transmitted to corporate security.
          """,
          "fail_txt": """
          The Bloodhound sniffs at your data trail but loses the scent.
          Your signal masking holds -- for now.
          """,
          "effect": lambda _state: _state.tracered(),
        },
        {
          "name": "Bite",
          "type": "damage",
          "description": """The Bloodhound lunges, sinking polygon teeth into
          your avatar. It's not its primary function, but it still hurts.
          Deals 1d6 damage.""",
          "roll": lambda: random.randint(1, 6),
          "special": "Physical damage"
        },
        {
          "name": "Howl",
          "type": "alert",
          "description": """The Bloodhound throws back its head and emits a
          piercing digital howl, alerting every security system in the network
          to your presence.""",
          "attempt": lambda _state: random.randint(1, 6) >= 5,
          "action_txt": """
          The howl echoes through the network. Your intrusion has been logged.
          System defenders are now aware of your presence.
          """,
          "fail_txt": """
          The howl dissipates into the noise floor.
          The network didn't register it.
          """,
          "effect": lambda _state: _state.logged(),
        },
      ]
    },
    {
      "id": "doppelganger",
      "name": "Doppelganger",
      "greeting": lambda _player: f"""
        You see yourself. An exact copy of your avatar stands before you,
        mirroring your stance, your posture, even the micro-expressions
        of your digital face. It smiles when you don't. It speaks with
        your voice: "Hello, {_player['name']}. Which one of us is real?"
        """,
      "health": 10,
      "initiative": lambda: random.randint(1, 100) + 15,
      "actions": [
        {
          "name": "Mirror Image",
          "type": "damage",
          "description": """The Doppelganger creates multiple copies of itself,
          disorienting you. You strike at the wrong one and the feedback
          damages your own interface. Deals 1d4 damage and stuns you.""",
          "roll": lambda: random.randint(1, 4),
          "special": "Stuns the netrunner"
        },
        {
          "name": "Misdirect",
          "type": "damage",
          "description": """The Doppelganger rearranges the virtual architecture
          around you. Corridors twist, nodes swap places. You lose your
          bearings. Deals 1d4 damage and slows you.""",
          "roll": lambda: random.randint(1, 4),
          "on_hit": lambda state: state.slow_down(random.randint(1, 2)),
          "special": "Misdirection"
        },
        {
          "name": "Identity Theft",
          "type": "damage",
          "description": """The Doppelganger reaches into your data stream and
          copies one of your programs for itself, corrupting the original.
          Deals 1d4 damage and may destroy a program.""",
          "roll": lambda: random.randint(1, 4),
          "on_hit": lambda state: state.lose_program() if random.randint(1, 4) == 4 else None,
          "special": "Program theft"
        },
      ]
    },
  ]


def black_ice(_state):
    cool_print("You arrive at a node. Steam hisses in the empty virtual space as intrusion countermeasures begin to activate.")
    cool_print("")

    ice = {**random.choice(black_ice_programs)}

    battle.battle(_state.player, ice, _state)