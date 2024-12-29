import os
import json
import levelgen
import logging
from node import node
import player 
import time
import state
import cc

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
            print("You are at a path and you must choose to cross it or to escape.")

            choice = input("Enter 'c' to cross the path or 'e' to escape: ")

            if choice == 'e':
                print("You escaped the challenge and live to see another day.")
                play = False
            elif choice == 'c':
                # get from path length of two continuous sections of the path
                path = rloc['path']
                sections = state.get_sections_of_path(path)
                
                # remove sections with length less than 2
                sections = [s for s in sections if s > 1]
                #print("Sections: ", sections)
                
                width = 10
                height = 10

                pieces = []
                symbols = ['A', 'B',]
                for s in sections: 
                    pieces.append({
                        'symbol': symbols.pop(0),
                        'length': s
                    })
                
                wander = 4

                print("To cross the path you must align the symbols on the following table in such a way:")
                print("")
                for p in pieces:
                    example = p['symbol'] * p['length']
                    print(p['symbol'] + ": " + str(p['length']) + " (example: " + example + ")")

                if cc.play_game(width, height, pieces, wander):
                    _state.complete_path()
                else:
                    logging.info("You dead, try again")
                    play = False
        else:
            # should not happen, die
            logging.error("Invalid state, exiting")
            exit(1)
        

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