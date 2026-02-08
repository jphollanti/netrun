import json
import levelgen
import logging
from node import node
import time
import state
import n_in_row
from cool_print import cool_print
from colorama import Fore

TRACE_COUNTDOWN = 10  # turns before kill team arrives when traced

def main():
    _state = state.MainState()
    _state.initialize()
    cool_print("")
    play = True
    trace_turns_left = None
    while (play):
        # Traced countdown: once traced, the clock is ticking
        if trace_turns_left is None and _state._state['player'].get('traced', False):
            trace_turns_left = TRACE_COUNTDOWN
            cool_print("")
            cool_print("WARNING: A kill team has been dispatched to your physical location.", fore_color=Fore.RED)
            cool_print(f"You have {trace_turns_left} turns to complete the mission or jack out.", fore_color=Fore.RED)
            cool_print("")

        if trace_turns_left is not None:
            trace_turns_left -= 1
            if trace_turns_left <= 0:
                # Check if player has Cut and Run
                deck = _state._state['player'].get('deck', [])
                has_cut_and_run = any(c.get('id') == 'cut_and_run' for c in deck)
                cool_print("")
                cool_print("Time's up. The kill team has arrived at your physical location.", fore_color=Fore.RED)
                if has_cut_and_run:
                    cool_print("Your Cut and Run program activates -- emergency jack-out!", fore_color=Fore.YELLOW)
                    cool_print("You barely escape with your life. Your body is gone from the chair by the time they breach the door.")
                    cool_print("Mission failed, but you live to run another day.")
                else:
                    cool_print("You feel a searing pain as your body is disconnected from the real world.")
                    cool_print("The kill team found your meat. Game over.")
                play = False
                continue
            elif trace_turns_left <= 3:
                cool_print(f"TRACE WARNING: {trace_turns_left} turns remaining!", fore_color=Fore.RED)

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
        cool_print("Progress: ", state=_state)
        print("")
        levelgen.visualize(state.WIDTH, state.HEIGHT, _state._state['route'], rloc['node']['location'], state=_state)
        cool_print("You are at location: ", rloc['node']['location'], state=_state)
        cool_print("")

        if not rloc['completed']['node']:
            n = node.generate_node(rloc['node']['type'])
            n(_state)
        elif not rloc['completed']['path']:
            cool_print("You are at a path and you must choose to cross it or to escape.", state=_state)
            cool_print("Enter 'c' to cross the path or 'e' to escape: ", fore_color=Fore.YELLOW)

            choice = input()

            if choice == 'e':
                cool_print("You escaped the challenge and live to see another day.", state=_state)
                play = False
            elif choice == 'c':
                # get from path length of two continuous sections of the path
                path = rloc['path']
                sections = levelgen.get_sections_of_path(path)
                
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
                slowed = _state._state['player'].get('slowed', 0)
                if slowed > 0:
                    wander = max(1, wander - slowed)
                    cool_print(f"You are slowed! Your movements are reduced to {wander} (normally 4).", fore_color=Fore.RED)
                    cool_print("")

                cool_print("To cross the path you must align the symbols either horizontally or vertially so they form continous lines:", state=_state)
                cool_print("")
                for p in pieces:
                    example = p['symbol'] * p['length']
                    cool_print(p['symbol'] + ": " + str(p['length']) + " (example: " + example + ")")

                if n_in_row.play_game(width, height, pieces, wander, state=_state):
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