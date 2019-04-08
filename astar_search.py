"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
"""

import sys
import json
import heapq

# Constants
BOARD_DIM_BOUNDS = 3
BLOCK_HEXTYPE = 'block'
COLOUR_PIECE_HEXTYPE = 'colour_piece'
EXITPOINT_HEXTYPE = 'exitpoint'

##################################### CLASS FOR GAME BOARD START #####################################
class GameBoard:
    def __init__(self):

        # A dictionary of key:value format -> 'coordinate':'hextype'
        # hextype can be 'block', 'exitpoint', 'colour_piece'
        # if coordinate is not in self.hexes, it means that it's empty
        self.hexes = {}

    # Check if coordinate is a block or not
    def isSteppable(self, current_hex):
        return (not "block" in self.hexes[current_hex])
    
    # Check if it's possible for colour piece to jump over current coordinate or not
    def isJumpable(self, current_hex, from_hex):
        (q_current, r_current) = current_hex
        (q_from, r_from) = from_hex

        q_move = q_current - q_from
        r_move = r_current - r_from
        
        q_next = q_current + q_move
        r_next = r_current + r_move

        next_hex = (q_next, r_next)

        # returns a tuple (boolean on whether it is possible to jump or not, hex to land on after jumping)
        return ((not 'block' in self.hexes[next_hex]) and (not 'colour_piece' in self.hexes[next_hex]) and (self.in_bounds, self, next_hex), next_hex)


    # Check if coordinate is within the bounds of the game board or not
    def in_bounds(self, current_hex):
        (q, r) = current_hex
        return (abs(q)<=3 and abs(r)<=3 and abs(q+r)<=3)

    # Returns a list of hex coordinates that can be the next move
    # Includes jump moves
    def next_possible_moves(self, current_hex):
        (q, r) = current_hex
        results = [(q, r-1), (q+1, r-1), (q+1, r), (q, r+1), (q-1, r+1), (q-1, r)]

        for step in results:
            if not self.isSteppable(self, step):
                is_jumpable_result = self.isJumpable(self, step, current_hex)
                if self.is_jumpable_result[0]:
                    results.append(is_jumpable_result[1])
                else: 
                    results.remove(step)
                    
        results = filter(self.in_bounds, results)
        return results

##################################### CLASS FOR PRIORITYQUEUE #####################################
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

##################################### OTHER HELPER FUNCTIONS #####################################

# Convert axial coordinates to cube coordinates
def axial_to_cube(hex):
    x = hex(0)
    z = hex(1)
    y = -x-z
    return (x, y, z) 

# Returns a list of endpoints in tuple/coordinate format depending on which colour is in play
def get_goals(colour, board):
    if colour == 'red':
        end_points = [(3, -3), (3, -2), (3, -1), (3, 0)]
    elif colour == 'blue':
        end_points = [(0, -3), (-1, -2), (-2, -1), (-3, 0)]
    elif colour == 'green':
        end_points = [(-3, 3), (-2, 3), (-1, 3), (0, 3)]

    exit_points = []
    for location in end_points:
        if (not location in board.hexes.keys()):
            exit_points.append(location)
        elif board.hexes[location] != BLOCK_HEXTYPE:
            exit_points.append(location)

    return exit_points

def a_star_search(board, start):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if (current in board.hexes.keys()) and (board.hexes[current] == EXITPOINT_HEXTYPE):
            break
    
        for next_move in board.next_possible_moves:
            new_cost = cost_so_far[current] + 


##################################### MAIN AND PRINT HELPER #####################################

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # fill board with -1 values
    ran = range(-3, +3 + 1)
    board_dict = {}

    for q in ran:
        for r in ran:
            if -q-r in ran:
                cost_so_far[(q, r)] = -1
    
    # for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
    #     cost_so_far[qr] = -1

    # Initiate Game Board
    game_board = GameBoard()

    # import data to three lists
    colour_in_play = data['colour']

    # Update game_board hexes with blocks coordinates
    for block in data['blocks']:
        block = tuple(block)
        game_board.hexes[block] = BLOCK_HEXTYPE
        board_dict[block] = '###'

    # Update game_board hexes with colour_pieces coordinates
    for piece in data['pieces']:
        piece = tuple(piece)
        game_board.hexes[piece] = COLOUR_PIECE_HEXTYPE
        board_dict[piece] = colour_in_play
         
    for goal in get_goals(colour_in_play, game_board):
        game_board.hexes[goal] = EXITPOINT_HEXTYPE

    



def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.
    
    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using 
    the axial coordinate system outlined in the project specification) and the 
    values are formatted as strings and placed in the drawing at the corres- 
    ponding location (only the first 5 characters of each string are used, to 
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the 
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates 
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}| 
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}| 
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}| 
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} | 
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
