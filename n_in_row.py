import random
import copy
from cool_print import cool_print
from cool_print import linear_speed_up_delay_provider
from cool_print import min_delay_provider

# Define a symbol for highlighting patterns
HIGHLIGHT_SYMBOL = "*"

ALL_SYMBOLS = {
    "A": {"color": "red"},
    "B": {"color": "blue"},
    "C": {"color": "green"},
    "D": {"color": "yellow"},
    "E": {"color": "purple"},
}

# Initialize the board with random pieces
def initialize_board(rows, cols, pieces, all_symbols, wander):

    board = [["_" for _ in range(cols)] for _ in range(rows)]
    taken = set()
    piece_locs = {}

    def fill_taken_indices(r, c):
        taken.add((r, c))
        taken.add((r, c - 1))
        taken.add((r, c + 1))
        taken.add((r - 1, c))
        taken.add((r + 1, c))
        taken.add((r - 1, c - 1))
        taken.add((r + 1, c + 1))
        taken.add((r - 1, c + 1))
        taken.add((r + 1, c - 1))
    
    def check_if_is_taken(r, c, vertical, length):
        if r is None or c is None:
            return True
        if vertical:
            for i in range(length):
                if (r + i, c) in taken:
                    return True
        else:
            for i in range(length):
                if (r, c + i) in taken:
                    return True
        return False

    # place pieces on the board randomly so they don't overlap
    for piece in pieces:
        piece_locs[piece["symbol"]] = []
        length = piece["length"]

        # find a random starting point that allows the piece to fit in the board
        vertical = random.choice([True, False])
        piece["vertical"] = vertical
        if vertical:
            r = None
            c = None
            while check_if_is_taken(r, c, vertical, length):
                r = random.randint(0, rows - (length+1))
                c = random.randint(0, cols - 1)
            
            for _ in range(length):
                r = r + 1
                board[r][c] = piece
                piece_locs[piece["symbol"]].append((r, c))
                # print("filling ", piece['symbol'], " r", r, "c", c)
                # fill taken indices so we don't overlap pieces
                fill_taken_indices(r, c)
        else:
            r = None
            c = None
            while check_if_is_taken(r, c, vertical, length):
                r = random.randint(0, rows - 1)
                c = random.randint(0, cols - (length+1))
            
            for _ in range(length):
                c = c + 1
                board[r][c] = piece
                piece_locs[piece["symbol"]].append((r, c))
                #print("filling ", piece['symbol'], " r", r, "c", c)
                # fill taken indices so we don't overlap pieces
                fill_taken_indices(r, c)
    
    # print original board
    original_board = copy.deepcopy(board)
    return [original_board, do_wander(board, pieces, piece_locs, wander)]


def do_wander(board, pieces, piece_locs, wander):
    """
    Break the current indices of piece_locs, make them wander around the board
    in random directions (one tile at a time), ensuring that:
      1. No symbol goes off the board.
      2. No symbol overlaps another.
      3. A cell does not immediately reverse its last move.
      4. Each symbol (A, B, etc.) is moved at least once (if possible).

    :param board: 2D list (board[y][x]) of size [height][width].
    :param pieces: List of dicts, e.g. [{"symbol": "A", "length": 2}, ...].
    :param piece_locs: Dict { symbol: [(x1,y1), (x2,y2), ...], ... }.
    :param wander: Integer number of single-cell random moves to perform overall.
    :return: Modified board (2D list) with the symbols after wandering.
    """
    # 1) Flatten all piece positions: [("A", (x1, y1)), ("B", (x2, y2)), ...]
    #    We'll keep track of them by index so we can choose random cells.
    all_coords = []
    symbol_indices = {}  # e.g. { "A": [0, 1, 5], "B": [2,3,4], ... }
    index = 0
    for symbol, coords in piece_locs.items():
        for (x, y) in coords:
            all_coords.append((symbol, (x, y)))
            symbol_indices.setdefault(symbol, []).append(index)
            index += 1

    # 2) Clear the board so we can re-place symbols after wandering
    height = len(board)
    width  = len(board[0]) if height > 0 else 0
    for row in range(height):
        for col in range(width):
            board[row][col] = "."

    # 3) Keep track of which cells are occupied to prevent overlap
    occupied_positions = set((x, y) for _, (x, y) in all_coords)

    # 4) Possible single-step directions
    directions = [(0, 1),   # down
                  (0, -1),  # up
                  (1, 0),   # right
                  (-1, 0)]  # left
    
    # 5) Track each cell's last direction; None means no previous move
    last_moves = [None] * len(all_coords)

    # ---------------------------------------------------------------
    # 6) FORCE each symbol to move at least once (if wander allows it)
    # ---------------------------------------------------------------
    # If we have fewer total wander steps than the number of symbols,
    # we can't guarantee *every* symbol moves. But we can still try.
    forced_moves_count = 0
    distinct_symbols = list(symbol_indices.keys())
    random.shuffle(distinct_symbols)  # randomize order of forced moves

    for sym in distinct_symbols:
        # If we've used up all our moves, stop trying
        if forced_moves_count >= wander:
            break

        # Attempt to move one random cell from this symbol
        indices_of_sym = symbol_indices[sym]
        random.shuffle(indices_of_sym)  # pick a random cell of that symbol
        did_move_symbol = False

        for i in indices_of_sym:
            symbol, (x, y) = all_coords[i]
            last_dir = last_moves[i]

            # Shuffle directions so we pick a random valid one
            random.shuffle(directions)
            for dx, dy in directions:
                # Skip if this direction is the exact opposite of the last move
                if last_dir is not None and (dx, dy) == (-last_dir[0], -last_dir[1]):
                    continue

                nx, ny = x + dx, y + dy
                # Check bounds + occupancy
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in occupied_positions:
                    # Valid move
                    occupied_positions.remove((x, y))
                    occupied_positions.add((nx, ny))
                    all_coords[i] = (symbol, (nx, ny))
                    last_moves[i] = (dx, dy)
                    forced_moves_count += 1
                    did_move_symbol = True
                    break

            if did_move_symbol:
                # We successfully moved a cell for this symbol, break from indices
                break

    # -----------------------------------------------------
    # 7) Perform the REMAINING random moves (if any left)
    # -----------------------------------------------------
    remaining_moves = max(0, wander - forced_moves_count)
    for _ in range(remaining_moves):
        # Pick one random cell to try to move
        i = random.randrange(len(all_coords))
        symbol, (x, y) = all_coords[i]
        last_dir = last_moves[i]

        # Shuffle directions to pick a random valid one
        random.shuffle(directions)
        for dx, dy in directions:
            # Skip if this direction reverses the last move
            if last_dir is not None and (dx, dy) == (-last_dir[0], -last_dir[1]):
                continue

            nx, ny = x + dx, y + dy
            # Check if in-bounds and not occupied
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in occupied_positions:
                # Valid move
                occupied_positions.remove((x, y))
                occupied_positions.add((nx, ny))
                all_coords[i] = (symbol, (nx, ny))
                last_moves[i] = (dx, dy)
                break
        # If no direction is valid, the cell doesn't move

    # 8) Place the symbols at their final positions on the board
    for symbol, (x, y) in all_coords:
        board[y][x] = symbol

    return board

# Print the board to the console
def print_board(board, highlights=None):
    # Print a header with column indices
    txt = "   "
    for c in range(len(board[0])):
        txt += str(c) + " "
    cool_print(txt, delay_provider=(lambda x, y: linear_speed_up_delay_provider(0.05, 0.1, x, y)))
    
    # Print each row with its index
    for r in range(len(board)):
        txt = f"{r:<3}" # Print row index (left-aligned with width 3)
        for c in range(len(board[0])):
            if highlights and (r, c) in highlights:
                txt += HIGHLIGHT_SYMBOL + " "
            else:
                cell = board[r][c]
                if isinstance(cell, dict):
                    txt += cell['symbol'] + " "
                else:
                    txt += cell + " "
        delay_provider = min_delay_provider #lambda x, y: linear_speed_up_delay_provider(0.05, 0.1, x, y)
        # if r > 1:
        #     delay_provider = min_delay_provider
        cool_print(txt, delay_provider=delay_provider)

# Find patterns based on the rules
def find_patterns(board, pieces):
    highlights = set()
    rows, cols = len(board), len(board[0])
    found = 0

    for r in range(rows):
        c = 0
        while c < cols:
            cell_symbol = board[r][c]  # e.g. "A" or "B" or "."
            # Find the piece dictionary whose "symbol" matches cell_symbol
            piece_dict = next((p for p in pieces if p["symbol"] == cell_symbol), None)
            if piece_dict:
                length = piece_dict["length"]
                # Check horizontally in row r
                if c + length <= cols and all(board[r][c + i] == cell_symbol for i in range(length)):
                    # Mark these cells as part of a highlight
                    highlights.update((r, c + i) for i in range(length))
                    # Increment the number of patterns found
                    found += 1
                    c += length
                else:
                    c += 1
            else:
                c += 1

    # Check columns for patterns
    for c in range(cols):
        r = 0
        while r < rows:
            cell_symbol = board[r][c]
            piece_dict = next((p for p in pieces if p["symbol"] == cell_symbol), None)
            if piece_dict:
                length = piece_dict["length"]
                # Check vertically in column c
                if r + length <= rows and all(board[r + i][c] == cell_symbol for i in range(length)):
                    highlights.update((r + i, c) for i in range(length))
                    found += 1
                    r += length
                else:
                    r += 1
            else:
                r += 1

    return highlights, found

def swap_cells(board, pos1, pos2):
    """
    Swap the contents of board at pos1 and pos2 if they are adjacent.
    
    :param board: 2D list (board[y][x]) of symbols.
    :param pos1: (x1, y1) - first cell coordinates.
    :param pos2: (x2, y2) - second cell coordinates.
    """
    (x1, y1) = pos1
    (x2, y2) = pos2

    # Check adjacency (Manhattan distance == 1)
    if abs(x2 - x1) + abs(y2 - y1) != 1:
        cool_print("Cells are not adjacent; swap canceled.")
        return

    # Swap the two cells on the board
    board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]


def prompt_and_swap(board):
    """
    Ask the user for two sets of coordinates (x1, y1) and (x2, y2),
    then call swap_cells to swap those positions on the board.
    """
    # 1) Prompt user for the first cell (x1, y1)
    cool_print("Enter coordinates of the first cell (x1 y1):", delay_provider=min_delay_provider)
    inp = input()
    x1_str, y1_str = inp.split()
    x1, y1 = int(x1_str), int(y1_str)

    # 2) Prompt user for the second cell (x2, y2)
    cool_print("Enter coordinates of the second cell (x2 y2):", delay_provider=min_delay_provider)
    inp = input()
    x2_str, y2_str = inp.split()
    x2, y2 = int(x2_str), int(y2_str)

    # 3) Call your swap function (make sure to import or include swap_cells)
    swap_cells(board, (x1, y1), (x2, y2))


def play_game(width, height, pieces, wander):
    _, board = initialize_board(width, height, pieces, ALL_SYMBOLS, wander)
    #print("Initial Board:")
    #print_board(original_board)

    cool_print("Board to solve:")
    print_board(board)

    while wander > 0:
        cool_print(f"Moves left: {wander}")
        # Pick two cells to swap
        prompt_and_swap(board)

        highlights = find_patterns(board, pieces)
        cool_print("Board to solve:")
        print_board(board, highlights)

        wander -= 1
    
        highlights, found = find_patterns(board, pieces)
        # check if highlights equals pieces
        #print("highlights", highlights, "found", found, "pieces", len(pieces), "pieces", pieces)
        if found == len(pieces):
            cool_print("You won!")
            return True
    
    cool_print("You lost!")
    return False


# Main game logic
def main():

    # Define the board size
    rows = 8
    cols = 8

    # Define possible pieces and their colors
    pieces = [
        {"symbol": "A", "length": 2},
        {"symbol": "B", "length": 4},
    ]

    wander = 4

    play_game(rows, cols, pieces, wander)


if __name__ == "__main__":
    main()
