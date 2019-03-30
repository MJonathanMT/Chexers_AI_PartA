"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
"""

import sys
import json
import operator


def get_adjacent(pos, adj_dict, blockers):
    if pos in adj_dict:
        return adj_dict

    all_moves = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
    pos_val = []
    for move in all_moves:
        q = pos[0] + move[0]
        r = pos[1] + move[1]
        if not (abs(q) <= 3 and abs(r) <= 3 and abs(q+r) <= 3):
            continue

        next_pos = (q, r)
        if next_pos in blockers:
            continue

        pos_val.append(next_pos)

    adj_dict[pos] = pos_val
    for val in pos_val:
        get_adjacent(val, adj_dict, blockers)

    return adj_dict


def get_z(x, y):
    z = (x + y) * -1
    return z


def manhattan(piece, goals):
    int_x = piece[0]
    int_y = piece[1]
    int_z = get_z(int_x, int_y)

    distance = []

    for goal in goals:
        end_x = goal[0]
        end_y = goal[1]
        end_z = get_z(end_x, end_y)
        diff_x = int_x - end_x
        diff_y = int_y - end_y
        diff_z = int_z - end_z
        curr_dist = max(abs(diff_x), abs(diff_y), abs(diff_z))
        distance.append(curr_dist)

    counter = 0
    total = 0
    for val in distance:
        counter += 1
        total += val

    avg_dist = total/counter
    return avg_dist


def get_goals(colour, blockers):
    end_points = []
    if colour == 'red':
        end_points = [(3, -3), (3, -2), (3, -1), (3, 0)]
    elif colour == 'blue':
        end_points = [(0, -3), (-1, -2), (-2, -1), (-3, 0)]
    elif colour == 'green':
        end_points = [(-3, 3), (-2, 3), (-1, 3), (0, 3)]

    final_end_points = []
    for loc in end_points:
        if loc not in blockers:
            final_end_points.append(loc)
    return final_end_points


def applicable(board_dict, piece, ):

    moves = ()
    all_moves = ((0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0))
    for move in all_moves:
        next_loc = tuple(map(operator.add, piece, move))


def distance_fill(board_dict, adj_dict, pos, dist):
    dist += 1
    if board_dict[pos] < 0:
        board_dict[pos] = dist
    elif dist > board_dict[pos]:
        return 0
    board_dict[pos] = dist
    for next_pos in adj_dict[pos]:
        distance_fill(board_dict, adj_dict, next_pos, dist)
    return 0


def play_game(board_dict, dist_dict, adj_dict, pieces, goals, colour):
    while pieces:
        piece = pieces[0]
        # exits move
        if piece in goals:
            print(str(piece) + " exits board")
            print ("curr pieces = " + str(pieces))
            print(board_dict)
            del board_dict[piece]
            pieces.remove(piece)
            print ("after pieces = " + str(pieces))

        # move normally
        else:
            best_move = ()
            shortest_dist = 0
            for next_move in adj_dict[piece]:
                if shortest_dist == 0:
                    shortest_dist = dist_dict[next_move]
                    best_move = next_move
                elif dist_dict[next_move] < shortest_dist:
                    shortest_dist = dist_dict[next_move]
                    best_move = next_move
            initial = piece
            pieces[0] = best_move
            board_dict[best_move] = colour
            del board_dict[initial]
            print("piece move from " + str(initial) + " to " + str(best_move))
        print_board(board_dict, message="Testing Board Condition", debug=False)
        print(board_dict)


def main():
    with open(sys.argv[1]) as test1:
        data = json.load(test1)
    # TODO: Search for and output winning sequence of moves
    # ...
    # fill board with -1 values
    ran = range(-3, +3 + 1)
    board_dict = {}
    dist_dict = {}
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        dist_dict[qr] = -1

    # import data to three lists
    colour = data['colour']
    piece_data = data['pieces']
    blocks_data = data['blocks']

    # make a list of tuples
    blockers = []
    for blocks in blocks_data:
        blocks = tuple(blocks)
        blockers.append(blocks)
        board_dict[blocks] = '###'

    pieces = []
    for piece in piece_data:
        piece = tuple(piece)
        pieces.append(piece)
        board_dict[piece] = colour

    goals = get_goals(colour, blockers)
    print ("goals = " + str(goals))

    for piece in pieces:
        manhattan(piece, goals)

    empty_dict = {}
    start = (0, 0)
    adj_dict = get_adjacent(start, empty_dict, blockers)

    for goal in goals:
        distance = 0
        distance_fill(dist_dict, adj_dict, goal, distance)
    print_board(dist_dict, message="Printing Distance Board", debug=False)

    play_game(board_dict, dist_dict, adj_dict, pieces, goals, colour)



def print_board(board_dict, message="Testing Board Condition", debug=False):
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
    ran = range(-3, +3 + 1)
    cells = []
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     "  # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
