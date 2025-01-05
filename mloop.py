import json
import levelgen
import logging
from node import node
import time
import state
import cc
from cool_print import cool_print
from colorama import Fore

def main():
    _state = state.MainState()
    _state.initialize()
    cool_print("")
    play = True
    while (play):

        if _state._state['player']['health'] <= 0:
            cool_print(f"Your character {_state._state['player']['name']} is dead.")
            if _state._state['player']['health'] < -9:
                cool_print(f"Like really, really dead (health = {_state._state['player']['health']}).")
            cool_print(f"Game over man. Game over. ")
            time.sleep(1)
            cool_print(f"So sad, sigh.")
            cool_print(f".")
            time.sleep(.5)
            cool_print(f"..")
            time.sleep(.5)
            cool_print(f"...")
            cool_print(f"")
            time.sleep(.5)
            cool_print(f"R.I.P. {_state._state['player']['name']}.")
            cool_print(f"")
            time.sleep(2)
            cool_print("Anyhoo! Start a new game? (y/n): ", fore_color=Fore.YELLOW)
            choice = input()
            if choice == 'y':
                _state.delete_state()
                _state.initialize()
            play = False

        rloc = levelgen.get_current_route_loc(_state._state['route'])
        cool_print("Progress: ")
        print("")
        levelgen.visualize(state.WIDTH, state.HEIGHT, _state._state['route'], rloc['node']['location'])
        cool_print("You are at location: ", rloc['node']['location'])
        cool_print("")

        if not rloc['completed']['node']:
            n = node.generate_node(rloc['node']['type'])
            n(_state)
        elif not rloc['completed']['path']:
            cool_print("You are at a path and you must choose to cross it or to escape.")
            cool_print("Enter 'c' to cross the path or 'e' to escape: ", fore_color=Fore.YELLOW)

            choice = input()

            if choice == 'e':
                cool_print("You escaped the challenge and live to see another day.")
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

                cool_print("To cross the path you must align the symbols either horizontally or vertially so they form continous lines:")
                cool_print("")
                for p in pieces:
                    example = p['symbol'] * p['length']
                    cool_print(p['symbol'] + ": " + str(p['length']) + " (example: " + example + ")")

                if cc.play_game(width, height, pieces, wander):
                    _state.complete_path()
                else:
                    cool_print("You dead, try again", fore_color=Fore.YELLOW)
                    play = False
        else:
            # should not happen, die
            logging.error("-----------------")
            logging.error("Invalid state, exiting")
            logging.error("-----------------")
            exit(1)


if __name__ == "__main__":
    main()