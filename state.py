import os
import levelgen
import json
import player 
from cool_print import cool_print
from cool_print import fixed_time_linear_speed_up_provider
from colorama import Fore
import time

WIDTH = 10
HEIGHT = 10
WAYPOINTS = 3

# state template
state = {
    'player': {
        'health': 50,
        'deck': [
            ''
        ],
    },
    'route': [{
        'node': {
            'label': 'S',
            'type': 'Jack-In',
            'location': [0, 0],
        },
        'next': {
            'label': '1',
            'type': 'Black ICE',
            'location': [0, 0],
        },
        'completed': {
            'node': False,
            'path': False,
        },
        'path': [
            {
                "location": [
                    3,
                    8
                ],
                "direction": [
                    -1,
                    0
                ]
            },
            {
                "location": [
                    2,
                    8
                ],
                "direction": [
                    0,
                    -1
                ]
            },
            {
                "location": [
                    2,
                    7
                ],
                "direction": [
                    0,
                    -1
                ]
            }
        ]
    }]
}


class MainState:
    _instance = None
    _state = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Create a new instance
        return cls._instance
    
    def initialize(self):
        # check if state file exists
        fn = "state.json"
        if os.path.exists(fn):
            cool_print("Loading existing game...", delay_provider=(lambda x, y: fixed_time_linear_speed_up_provider(3.5, x, y)), end='')
            time.sleep(1)
            # TODO: Add logic to replace only parts of existing line
            cool_print("Game loaded!            ")
            with open(fn, "r") as f:
                self._state = json.load(f)
        else:
            cool_print("Creating new game and character")
            cool_print("Enter your character name: ", fore_color=Fore.YELLOW)
            name = None
            while not name and name != "":
                name = input()
                if name == "":
                    cool_print("Name cannot be empty. Enter your character name: ", fore_color=Fore.YELLOW)
            route = levelgen.generate_new_state(WIDTH, HEIGHT, WAYPOINTS)
            _player = player.new_player(name)
            self._state = {
                'player': _player,
                'route': route
            }

            self.store()
    
    def delete_state(self):
        os.remove("state.json")

    def change_health(self, amount):
        self._state['player']['health'] += amount
        self.store()
    
    def stun(self):
        self._state['player']['stunned'] = 1
        self.store()
    
    def unstun(self):
        self._state['player']['stunned'] = 0
        self.store()

    def store(self):
        with open("state.json", "w") as f:
            json.dump(self._state, f)

    def complete_node(self):
        rloc = levelgen.get_current_route_loc(self._state['route'])
        rloc['completed']['node'] = True
        self.store()

    def complete_path(self):
        rloc = levelgen.get_current_route_loc(self._state['route'])
        rloc['completed']['path'] = True
        self.store()
    
    def logged(self):
        self._state['player']['logged'] = True
        self.store()
        cool_print("Your actions are now under scrutiny by the system defenders.")
        cool_print("The intrusion attempt is logged and stored for post-intrusion analysis.")

    def slow_down(self, turns):
        self._state['player']['slowed'] = self._state['player'].get('slowed', 0) + turns
        self.store()
        cool_print(f"You are slowed down by {turns} turns.")

    def watch_dogged(self):
        self._state['player']['watch_dogged'] = True
        self.store()
        cool_print("The Watchdog program catches your scent and follows you around.")
        cool_print("It will assist any Black ICE programs you encounter.")

    def tracered(self):
        self._state['player']['traced'] = True
        self.store()
        cool_print("The Tracer program has located your physical position.")
        cool_print("You must deal with the consequences in the physical world.")

    def destroy_programs(self):
        self._state['player']['deck'] = []
        self.store()
        cool_print("All your programs have been destroyed!")

    def complete_mission(self, success):
        rloc = levelgen.get_current_route_loc(self._state['route'])
        rloc['completed']['node'] = True
        rloc['completed']['path'] = True
        self.store()
        cool_print("Mission complete!")
        if success:
            if self._state['player'].get('logged', False):
                cool_print("You completed the run... but your intrusion was logged.")
                cool_print("The corp knows someone was in their system.")
                cool_print("They'll be tightening security. And looking for you.")
                cool_print("Not a clean run, but you got the data. Partial success.")
            else:
                cool_print("Clean run. No traces, no logs. Ghost in the machine.")
                cool_print("You successfully completed the run. Well done, netrunner.")
        else:
            cool_print("The mission was a failure. Better luck next time.")

    def receive_program(self):
        import random as _random
        program = _random.choice(player.deck_options)
        self._state['player']['deck'].append(program)
        self.store()
        cool_print(f"You received a new program: {program['name']}.")
        cool_print(f"  {program['effect']}")

    def lose_program(self):
        deck = self._state['player']['deck']
        if deck:
            import random as _random
            lost = _random.choice(deck)
            deck.remove(lost)
            self.store()
            cool_print(f"You lost the program: {lost['name']}.")
        else:
            cool_print("You have no programs to lose.")