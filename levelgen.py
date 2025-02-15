import random
import json
from colorama import Fore, Back, Style, init
import node.node as node
from cool_print import cool_print
from cool_print import linear_speed_up_delay_provider
from cool_print import min_delay_provider

# Initialize colorama
init()

def get_random_position(width, height):
    return [random.randint(0, width-1), random.randint(0, height-1)]

def near(a, b):
    if b == None or b['location'] == None:
        return True
    al = a['location']
    bl = b['location']
    return abs(al[0] - bl[0]) + abs(al[1] - bl[1]) < 3


def near_any(_l, b):
    if b == None:
        return True
    for a in _l:
        if near(a, b):
            return True
    return False

# Visualization: Handle conflicting directions
def visualize_cell(directions):
    if len(directions) == 1:
        return next(iter(directions))  # Single direction
    elif "→" in directions and "←" in directions:
        return "↔"  # Conflicting horizontal directions
    elif "↑" in directions and "↓" in directions:
        return "↕"  # Conflicting vertical directions
    else:
        return "+"  # General conflict (diagonal or more complex)


def get_current_route_loc(route):
    for r in route:
        if not r['completed']['node'] or not r['completed']['path']:
            return r
    return None


def visualize(width, height, route, current_loc, state=None):

    #print(json.dumps(route, indent=4))  
    paths = {}
    nodes = {}
    for r in route:
        loc = r['node']['location']
        nodes[str(loc[0]) + "," + str(loc[1])] = r['node']

        for p in r['path']:
            loc = p['location']
            key = str(loc[0]) + "," + str(loc[1])
            if key not in paths:
                paths[key] = set()
            
            # map direction to symbol

            # Possible single-step directions
            # directions = [(0, 1),   # down
            #               (0, -1),  # up
            #               (1, 0),   # right
            #               (-1, 0)]  # left

            symbol = ''
            if p['direction'] == [1, 0]:
                symbol = '→'
            elif p['direction'] == [-1, 0]:
                symbol = '←'
            elif p['direction'] == [0, 1]:
                symbol = '↓'
            elif p['direction'] == [0, -1]:
                symbol = '↑'
            paths[key].add(symbol)

    # visualize progress with different color
    leg = set()
    for r in route:
        if r['completed']['node'] and r['completed']['path']:
            continue

        dobreak = False
        if not r['completed']['node'] or not r['completed']['path']:
            dobreak = True

        # if not r['completed']['node']:
        
        if not r['completed']['path']:
            for p in r['path']:
                loc = p['location']
                key = str(loc[0]) + "," + str(loc[1])
                leg.add(key)
        
        if not r['completed']['node']:
            loc = r['node']['location']
            key = str(loc[0]) + "," + str(loc[1])
            leg.add(key)
        
        next = r['next']
        if next != None:
            loc = next['location']
            key = str(loc[0]) + "," + str(loc[1])
            leg.add(key)
        
        if dobreak:
            break
    
    current_loc_key = str(current_loc[0]) + "," + str(current_loc[1])

    # Print a header with column indices
    txt = "   "
    for c in range(width):
        txt += str(c) + " "
    cool_print(txt, delay_provider=(lambda x, y: linear_speed_up_delay_provider(0.1, 0.2, x, y)), state=state)

    # visualize start, end, waypoints and paths
    for y in range(height):
        txt = f"{y:<3}"

        color_map = {}
        for x in range(width):
            key = str(x) + "," + str(y)
            text_x = 3 + 2 * x
            
            if key in leg:
                color_map[text_x] = Fore.YELLOW
            if key == current_loc_key:
                color_map[text_x] = Fore.RED
            if key in nodes:
                node = nodes[key]
                txt += node['label'] + " "
            elif key in paths:
                txt += visualize_cell(paths[key]) + " "
            else:
                txt += ". "
        
        delay_provider = min_delay_provider
        # delay_provider = lambda x, y: linear_speed_up_delay_provider(0.1, 0.2, x, y)
        # if y > 1:
        #     delay_provider = min_delay_provider
        cool_print(txt, color_map=color_map, delay_provider=delay_provider, state=state)

def generate_new_state(width, height, waypoints_number):
    start = {
        'label': 'S',
        'type': 'Jack-In', 
        'location': get_random_position(width, height),
    }
    
    end = {
        'label': 'E',
        'type': random.choice(node.end_node_types),
        'location': None
    }
    while near(start, end):
        end['location'] = get_random_position(width, height)

    #print("start", start, "end", end)

    # generate nodes
    nodes = []
    for i in range(waypoints_number):
        wp = {
            'label': str(i),
            'type': random.choice(node.node_types),
            'location': get_random_position(width, height)
        }
        while near_any(nodes, wp) or near(start, wp) or near(end, wp):
            wp['location'] = get_random_position(width, height)
        nodes.append(wp)

    #print("nodes", nodes)

    # Generate paths between start, nodes and end
    nodes2 = [start] 
    nodes2.extend(nodes)
    nodes2.append(end)

    route = []

    for i in range(len(nodes2)):
        next = None
        if i < len(nodes2) - 1:
            next = nodes2[i + 1]
        r = {
            'node': nodes2[i],
            'next': next,
            'completed': {
                'node': False,
                'path': False,
            },
            'path': []
        }

        # Possible single-step directions
        # directions = [(0, 1),   # down
        #               (0, -1),  # up
        #               (1, 0),   # right
        #               (-1, 0)]  # left
        if i == len(nodes2) - 1:
            route.append(r)
            break
        
        start_wp = nodes2[i]
        end_wp = nodes2[i + 1]
        x1, y1 = start_wp['location']
        x2, y2 = end_wp['location']
        while (x1, y1) != (x2, y2):
            if x1 < x2:
                next_step = (x1 + 1, y1)
                direction = [1, 0]
            elif x1 > x2:
                next_step = (x1 - 1, y1)
                direction = [-1, 0]
            elif y1 < y2:
                next_step = (x1, y1 + 1)
                direction = [0, 1]
            else:
                next_step = (x1, y1 - 1)
                direction = [0, -1]
            
            # Add direction to the paths dictionary
            p = {
                'location': [x1, y1],
                'direction': direction
            }
            r['path'].append(p)
            x1, y1 = next_step
        
        route.append(r)
    
    return route


def main():
    width = 10
    height = 10
    waypoints_number = 3

    route = generate_new_state(width, height, waypoints_number)
    visualize(width, height, route)


if __name__ == "__main__":
    main()
