import os
import levelgen
import json
import player 

WIDTH = 10
HEIGHT = 10
WAYPOINTS = 3

# state template
state = {
    'player': {
        'health': 10,
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
            print("Loading existing game")
            with open(fn, "r") as f:
                self._state = json.load(f)
        else:
            print("Creating new game")
            route = levelgen.generate_new_state(WIDTH, HEIGHT, WAYPOINTS)
            _player = player.new_player()
            self._state = {
                'player': _player,
                'route': route
            }

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
        print("Actions are being logged")
    
    def slow_down(self, roll):
        print("Slowed down")
    
    def watch_dogged(self):
        print("Watch dogged")


def get_sections_of_path(path):
    """
    Since paths are always at max a set of two blocks, get from path length two continuous sections of the path
    """
    sections = []
    direction = None
    count = 0
    for step in path:
        if direction is None:
            direction = step['direction']
            count = 1
        elif step['direction'] == direction:
            count += 1
        elif step['direction'] != direction:
            sections.append(count)
            direction = step['direction']
            count = 0
    
    if count > 0:
        sections.append(count)
    
    return sections