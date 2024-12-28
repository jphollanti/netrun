import os
import json
import levelgen
import logging
from node import node
import player 
import time
import state

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


def main():
    logging.info("Loading game... ")
    time.sleep(.5)
    _state = state.MainState()
    _state.initialize()
    logging.info("Game ready.")

    #print("state", json.dumps(state, indent=4))
    logging.info("Current state: ")
    logging.info("")
    levelgen.visualize(state.WIDTH, state.HEIGHT, _state._state['route'])
    print("")
    logging.info("Player: ")
    logging.info(json.dumps(_state._state['player'], indent=4))
    print("")

    play = True
    while (play):
        rloc = levelgen.get_current_route_loc(_state._state['route'])
        print("You are at location: ", rloc['node']['location'])

        if not rloc['completed']['node']:
            n = node.generate_node(rloc['node']['type'])
            n(_state)
        elif not rloc['completed']['path']:
            print("You are at a path")
        else:
            # should not happen, die
            logging.error("Invalid state, exiting")
            exit(1)
        
        play = False
        

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