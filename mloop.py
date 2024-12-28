import os
import json
import levelgen
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

WIDTH = 10
HEIGHT = 10
WAYPOINTS = 3

state = {
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
        'path': {
            "4,8": [
                "\u2192"
            ],
            "5,8": [
                "\u2192"
            ],
        }
    }]
}


def initialize():
    global state

    # check if state file exists
    fn = "state.json"
    if os.path.exists(fn):
        logging.info("Loading state from file")
        with open(fn, "r") as f:
            state = json.load(f)
    else:
        logging.info("Generating new state")
        route = levelgen.generate_new_state(WIDTH, HEIGHT, WAYPOINTS)
        state['route'] = route

        with open(fn, "w") as f:
            json.dump(state, f)


def main():
    initialize()

    #print("state", json.dumps(state, indent=4))
    logging.info("Current state: ")
    logging.info("")
    levelgen.visualize(WIDTH, HEIGHT, state['route'])

    # play = True
    # while (play):
    #     print("You are at location: " + state['location'])
    #     is_moving = state['location'] == 'S': 
    #     print("Possible moves: " + ", ".join(state['paths'][state['location']]))
    #     print("Enter your move: ")
    #     move = input()
    #     if move == "exit":
    #         play = False
    #     elif move in state['paths']:
    #         state['location'] = move
    #     else:
    #         logging.info("Invalid move, try again")



if __name__ == "__main__":
    main()