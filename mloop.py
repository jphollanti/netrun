import json
import levelgen
import logging
from node import node
import time
import state
import cc
from cool_print import cool_print
from colorama import Fore, Back, Style, init

def main():
    _state = state.MainState()
    _state.initialize()
    cool_print("")
    play = True
    while (play):
        rloc = levelgen.get_current_route_loc(_state._state['route'])
        cool_print("Progress: ")
        print("")
        levelgen.visualize(state.WIDTH, state.HEIGHT, _state._state['route'], rloc['node']['location'])
        cool_print("You are at location: ", rloc['node']['location'])

        if not rloc['completed']['node']:
            n = node.generate_node(rloc['node']['type'])
            n(_state)
        elif not rloc['completed']['path']:
            cool_print("You are at a path and you must choose to cross it or to escape.")
            color_map = {}
            txt = "Enter 'c' to cross the path or 'e' to escape: "
            for i in range(len(txt)):
                color_map[i] = Fore.YELLOW
            cool_print("Enter 'c' to cross the path or 'e' to escape: ", color_map=color_map)

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

                cool_print("To cross the path you must align the symbols on the following table in such a way:")
                cool_print("")
                for p in pieces:
                    example = p['symbol'] * p['length']
                    cool_print(p['symbol'] + ": " + str(p['length']) + " (example: " + example + ")")

                if cc.play_game(width, height, pieces, wander):
                    _state.complete_path()
                else:
                    cool_print("You dead, try again")
                    play = False
        else:
            # should not happen, die
            logging.error("Invalid state, exiting")
            exit(1)
        

    #     is_moving = state['location'] == 'S': 
    #     cool_print("Possible moves: " + ", ".join(state['paths'][state['location']]))
    #     cool_print("Enter your move: ")
    #     move = input()
    #     if move == "exit":
    #         play = False
    #     elif move in state['paths']:
    #         state['location'] = move
    #     else:
    #         cool_print("Invalid move, try again")



if __name__ == "__main__":
    main()