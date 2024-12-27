import random

width = 10
height = 10
waypoints_number = 3

# Generate a random level with paths between waypoints

# first generate starting position and ending position

def get_random_position():
    return (random.randint(0, width-1), random.randint(0, height-1))

def near(a, b):
    if b == None:
        return True
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) < 3


def near_any(_l, b):
    if b == None:
        return True
    for a in _l:
        if near(a, b):
            return True
    return False

start = get_random_position()
end = None
while near(start, end):
    end = get_random_position()

#print("start", start, "end", end)

# generate waypoints
waypoints = []
for i in range(waypoints_number):
    wp = None
    while near_any(waypoints, wp) or near(start, wp) or near(end, wp):
        wp = get_random_position()
    waypoints.append(wp)

#print("waypoints", waypoints)

# Generate paths between start, waypoints and end
paths = {}  # (x, y) -> index
wps2 = [start] 
wps2.extend(waypoints)
wps2.append(end)

for i in range(len(wps2) - 1):
    start_wp = wps2[i]
    end_wp = wps2[i + 1]
    x, y = start_wp
    while (x, y) != end_wp:
        if x < end_wp[0]:
            next_step = (x + 1, y)
            direction = "→"
        elif x > end_wp[0]:
            next_step = (x - 1, y)
            direction = "←"
        elif y < end_wp[1]:
            next_step = (x, y + 1)
            direction = "↓"
        else:
            next_step = (x, y - 1)
            direction = "↑"
        
        # Add direction to the paths dictionary
        if (x, y) not in paths:
            paths[(x, y)] = set()
        paths[(x, y)].add(direction)
        
        x, y = next_step

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

# visualize start, end, waypoints and paths
for y in range(height):
    for x in range(width):
        if (x, y) == start:
            print("S", end="")
        elif (x, y) == end:
            print("E", end="")
        elif (x, y) in waypoints:
            wp_idx = waypoints.index((x, y))
            print("" + str(wp_idx), end="")
        elif (x, y) in paths:
            #idx = paths[(x, y)]
            #print("P" + str(idx), end="")
            print(visualize_cell(paths[(x, y)]), end="")
        else:
            print(".", end="")
    print()