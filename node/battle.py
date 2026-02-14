import random
from colorama import Fore, Back, Style, init
from enum import Enum, auto
from cool_print import cool_print


# 
# Logic:
# 
# Player and opponent have actions that they play on their turn. Player has a deck of additional
# actions. 
# 
# Player and opponent have health. Player and opponent have initiative.
#
# When an action is taken against a player or opponent, the action will be added to 
# the effects log. The effects log is processed in order when it's player's turn. 
# 
# Some actions need to be immediate, like damage. 
#
# All actions need to have a type because some actions can be counteracted by other actions.
#
# For example, if a player is struck by a worm, they can use an antivirus action to remove the worm.
# The end result is that the effect of the worm is nullified. 
# 
# The effect log is ordered based on turns. For example, if a player is struck by an action
# that causes damage over time, the effect will be added to the effect log and processed on 
# the player's turn.
#
# If the action is stun instead of damage, the player will lose their next turn.
# 

class ActionType(Enum):
    DAMAGE = auto()
    ALERT = auto()
    HEAL = auto()
    STUN = auto()


class Action:
    def __init__(self, whodunnit, type, description, roll, attempt, effect, action_txt, fail_txt):
        self.whodunnit = whodunnit
        self.type = type
        self.description = description
        self.roll = roll
        self.attempt = attempt
        self.effect = effect
        self.action_txt = action_txt
        self.fail_txt = fail_txt


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

    cool_print("")
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

        # Watchdog assist: +15 initiative for opponent
        watch_dogged = player.get('watch_dogged', False)
        if watch_dogged:
            opponent_initiative += 15
            cool_print("The Watchdog program assists your opponent!", fore_color=Fore.RED)
            cool_print(f"{opponent['name']} gains +15 initiative from the Watchdog.")

        cool_print("Player Initiative: ", player_initiative, f', {opponent["name"]} Initiative: ', opponent_initiative)

        if player_initiative > opponent_initiative:
            cool_print("You have the initiative.")
            cool_print("You attack first.")
        else:
            cool_print(f"{opponent['name']} has the initiative.")
            cool_print("You attack second.")

        # Watchdog assist: 10% chance of a free opening attack
        if watch_dogged and random.random() < 0.1:
            cool_print("")
            cool_print("The Watchdog lunges at you, giving the ICE an opening!", fore_color=Fore.RED)
            action = random.choice(opponent['actions'])
            if action['type'] == 'damage':
                damage = action['roll']()
                cool_print(f"Watchdog-assisted strike deals {damage} bonus damage!")
                player['health'] -= damage

        # Track ongoing residual damage effects: list of (damage_per_turn, turns_remaining, source_name)
        residual_effects = []
        player_stunned = False

        def apply_residual_damage(player):
            """Apply all active residual damage effects and decrement their counters."""
            still_active = []
            for dmg, turns, source in residual_effects:
                cool_print(f"Residual effect from {source}: {dmg} damage.")
                player['health'] -= dmg
                if turns - 1 > 0:
                    still_active.append((dmg, turns - 1, source))
                else:
                    cool_print(f"Residual effect from {source} has worn off.")
            residual_effects.clear()
            residual_effects.extend(still_active)

        def player_turn(player, opponent):
            nonlocal player_stunned
            if player_stunned:
                cool_print("You are stunned and cannot act this turn!")
                player_stunned = False
                return
            cool_print(f"Your turn to attack the {opponent['name']}.")
            cool_print("roll 3d10 damage.")
            cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
            input()
            damage = random.randint(1, 10) + random.randint(1, 10) + random.randint(1, 10)
            cool_print("You deal " + str(damage) + " damage to the " + opponent['name'] + ".")
            opponent['health'] -= damage

        def opponent_turn(player, opponent):
            nonlocal player_stunned
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

                # Handle on-hit effects (e.g., Raven's program destruction)
                if 'on_hit' in action:
                    action['on_hit'](state)

                # Handle residual damage (e.g., Hellhound's burn, Payload Injection)
                if 'residual' in action:
                    residual_dmg = action['residual'](state)
                    if isinstance(residual_dmg, int) and residual_dmg > 0:
                        turns = 3  # residual effects last 3 turns
                        residual_effects.append((residual_dmg, turns, action['name']))
                        cool_print(f"{action['name']} applies {residual_dmg} residual damage per turn for {turns} turns.")

                # Handle special effects like stun
                if action.get('special') and 'stun' in action['special'].lower():
                    if random.randint(1, 6) >= 4:
                        cool_print("The attack stuns you!")
                        player_stunned = True
                        state.stun()

            elif action['type'] == 'alert':
                succ = action['attempt'](state)
                if succ:
                    cool_print(action['action_txt'])
                    cool_print("")
                    cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
                    input()
                    action['effect'](state)
                    # Some alerts end the fight (e.g., Netwatch Scout summons Black ICE)
                    if action.get('ends_battle', False):
                        opponent['health'] = 0
                else:
                    cool_print(action['fail_txt'])
                    cool_print("")
                    cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
                    input()

            elif action['type'] == 'debuff':
                cool_print(f"{opponent['name']} uses {action['name']}!")
                if action.get('special'):
                    cool_print(f"Effect: {action['special']}")
                cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
                input()

            elif action['type'] == 'buff':
                cool_print(f"{opponent['name']} uses {action['name']}!")
                if action.get('special'):
                    cool_print(f"Effect: {action['special']}")
                cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
                input()

            elif action['type'] == 'defensive':
                cool_print(f"{opponent['name']} uses {action['name']}!")
                if action.get('special'):
                    cool_print(f"Effect: {action['special']}")
                cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
                input()

            elif action['type'] == 'utility':
                cool_print(f"{opponent['name']} uses {action['name']}!")
                if action.get('special'):
                    cool_print(f"Effect: {action['special']}")
                cool_print("Press any key to continue.", fore_color=Fore.YELLOW)
                input()

        def game_over(opponent):
            cool_print(f"You are defeated by the {opponent['name']}.")
            cool_print("Game Over.")
            exit()

        while True:
            if player['health'] <= 0:
                game_over(opponent)
            if opponent['health'] <= 0:
                break

            # Apply residual damage at the start of each round
            if residual_effects:
                apply_residual_damage(player)
                if player['health'] <= 0:
                    game_over(opponent)

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
            
