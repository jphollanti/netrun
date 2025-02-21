import random
from colorama import Fore, Back, Style, init
import node.node as node
import os
import sys

# Import cool_print from parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the parent directory at the beginning of sys.path
sys.path.insert(0, parent_dir)
from cool_print import cool_print


def break_to_lines(text):
    # Split into lines, removing leading/trailing blank lines:
    lines = text.strip().splitlines()
    # Remove leading spaces from each line:
    lines = [line.lstrip() for line in lines]
    return lines

def battle(player, opponent, state): 
    lines = break_to_lines(opponent['greeting'](player))
    for line in lines:
        cool_print(line)
    
    cool_print("")

    cool_print("You must make a choice:")
    cool_print(f"1. Face the {opponent['name']}.")
    cool_print("2. Jack-out and escape. Continue to fight another day.")

    cool_print("Enter your choice: ", fore_color=Fore.YELLOW)
    choice = input()

    if choice == '2':
        cool_print(f"You escape just in time to evade the {opponent['name']}.")
        cool_print("You live to fight another day.")
        exit()
    elif choice == '1':
        cool_print("You have chosen to face the enemy.")

        player_initiative = random.randint(1, 100)
        opponent_initiative = opponent['initiative']()

        cool_print("Player Initiative: ", player_initiative, f', {opponent['name']} Initiative: ', opponent_initiative)

        if player_initiative > opponent_initiative:
            cool_print("You have the initiative.")
            cool_print("You attack first.")
        else:
            cool_print(f"{opponent['name']} has the initiative.")
            cool_print("You attack second.")

        def player_turn(player, opponent):
            cool_print(f"Your turn to attack the {opponent['name']}.")
            cool_print("roll 3d10 damage.")
            cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
            input()
            damage = random.randint(1, 10) + random.randint(1, 10) + random.randint(1, 10)
            cool_print("You deal " + str(damage) + " damage to the " + opponent['name'] + ".")
            opponent['health'] -= damage
        
        def opponent_turn(player, opponent):
            cool_print(f"It's the {opponent['name']}'s turn.")

            action = random.choice(opponent['actions'])

            lines = break_to_lines(action['description'])
            for line in lines:
                cool_print(line)
            cool_print()

            if action['type'] == 'damage':
                cool_print(f"{opponent['name']} rolls for damage.")
                cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
                input()
                damage = action['roll']()
                cool_print(f"The {opponent['name']} deals " + str(damage) + " damage to you.")
                player['health'] -= damage

                # TODO: cool_print(f"{opponent['name']}'s attack has a special effect.")
            elif action['type'] == 'alert':
                succ = action['attempt'](state)
                if succ:
                    cool_print(action['action_txt'])
                    cool_print("")
                    cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
                    input()
                    action['effect']()
                    opponent['health'] = 0
                else:
                    cool_print(action['fail_txt'])
                    cool_print("")
                    cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
                    input()
        
        def game_over(opponent):
            cool_print(f"You are defeated by the {opponent['name']}.")
            cool_print("Game Over.")
            exit()

        while (True): 
            if player['health'] <= 0:
                game_over(opponent)
            if opponent['health'] <= 0:
                break
            
            cool_print("Player Health: ", player['health'])
            cool_print(opponent['name'] + " Health: ", opponent['health'])

            if player_initiative > opponent_initiative:
                player_turn(player, opponent)
                if opponent['health'] <= 0:
                    break
                opponent_turn(player, opponent)
            else:
                opponent_turn(player, opponent)
                if player['health'] <= 0:
                    game_over(opponent)
                player_turn(player, opponent)
    

    cool_print(f"You defeated the {opponent['name']}. This node is now secure and you can continue your mission.")
    state.complete_node()
            
