"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
"""

import sys
import json


def get_adjacent(pos, adj_dict):
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

        pos_val.append(next_pos)

    adj_dict[pos] = pos_val
    for val in pos_val:
        get_adjacent(val, adj_dict)

    return adj_dict


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


def distance_fill(dist_dict, adj_dict, pos, dist, blockers):
    dist += 1
    if dist_dict[pos] == '###':
        dist_dict[pos] = dist
    elif dist > dist_dict[pos]:
        return 0
    elif dist < dist_dict[pos]:
        dist_dict[pos] = dist
    next_jump = ()
    for next_pos in adj_dict[pos]:
        movable = True
        jumpable = True
        if next_pos in blockers:
            movable = False

        if not movable:
            q_move = (next_pos[0] - pos[0])*2
            r_move = (next_pos[1] - pos[1])*2
            next_jump = (pos[0] + q_move, pos[1] + r_move)
            if next_jump not in adj_dict[next_pos] or next_jump in blockers:
                jumpable = False
        if movable:
            distance_fill(dist_dict, adj_dict, next_pos, dist, blockers)
        elif jumpable:
            distance_fill(dist_dict, adj_dict, next_jump, dist, blockers)
    return 0


def get_moves(dist_dict, adj_dict, pieces, blockers):
    best_moves = {}
    for piece in pieces:
        movement = []
        shortest_dist = 0
        best_move = ()
        for next_move in adj_dict[piece]:
            if next_move in pieces or next_move in blockers:
                continue
            if shortest_dist == 0:
                shortest_dist = dist_dict[next_move]
                best_move = next_move
            elif dist_dict[next_move] < shortest_dist:
                shortest_dist = dist_dict[next_move]
                best_move = next_move
        print(best_move)
        if best_move != () and dist_dict[piece] <= dist_dict[best_move]:
            best_move = ()
        movement.append(piece)
        movement.append(best_move)
        best_moves[piece] = movement
    return best_moves


def get_jumps(dist_dict, adj_dict, blockers, pieces):
    best_jumps = {}
    for piece in pieces:
        shortest_dist = 0
        jumping = []
        best_jump = ()
        for next_move in adj_dict[piece]:
            if next_move not in blockers and next_move not in pieces:
                continue
            q_move = (next_move[0] - piece[0])*2
            r_move = (next_move[1] - piece[1])*2
            next_jump = (piece[0] + q_move, piece[1] + r_move)
            if next_jump not in adj_dict[next_move] or next_jump in pieces or next_jump in blockers:
                continue
            if shortest_dist == 0:
                shortest_dist = dist_dict[next_jump]
                best_jump = next_jump
            elif dist_dict[next_jump] < shortest_dist:
                shortest_dist = dist_dict[next_jump]
                best_jump = next_jump
        if best_jump != () and dist_dict[piece] <= dist_dict[best_jump]:
            best_jump = ()
        jumping.append(piece)
        jumping.append(best_jump)
        best_jumps[piece] = jumping

    return best_jumps


def final_movements(dist_dict, best_moves, best_jumps):
    final_moves = {}
    for piece in best_moves:
        move = best_moves[piece][1]
        if best_jumps[piece][1] == ():
            final_moves[piece] = best_moves[piece]
            final_moves[piece].append('move')
            print('this is final moves' +str(final_moves[piece]))
            continue
        if move == ():
            final_moves[piece] = best_jumps[piece]
            final_moves[piece].append('jump')
            print('this is final moves' +str(final_moves[piece]))
            continue
        jump = best_jumps[piece][1]
        if dist_dict[move] < dist_dict[jump]:
            final_moves[piece] = best_moves[piece]
            final_moves[piece].append('move')
        else:
            final_moves[piece] = best_jumps[piece]
            final_moves[piece].append('jump')

        print('this is final moves' +str(final_moves[piece]))
    return final_moves


def get_piece(dist_dict, final_moves):
    final_move = []
    dist = 0
    for piece in final_moves:
        if final_moves[piece][1] == ():
            continue
        if dist == 0:
            dist = dist_dict[piece]
            final_move = final_moves[piece]
        elif dist_dict[piece] == dist:
            if final_moves[piece][2] == 'jump':
                final_move = final_moves[piece]
        elif dist_dict[piece] > dist:
            dist = dist_dict[piece]
            final_move = final_moves[piece]

    return final_move


def play_game(board_dict, dist_dict, adj_dict, blockers, pieces, goals, colour):
    while pieces:
        print('IMPLEMENT IF TWO OR MORE PIECES SAME DIST PICK JUMP')
        # exits move
        exit_move = False
        for piece in pieces:
            if piece in goals:
                print("EXIT from " + str(piece) + ".")
                del board_dict[piece]
                pieces.remove(piece)
                exit_move = True
                break
        print('EXIT MOVE IS = ' + str(exit_move))
        # move normally
        if not exit_move:
            best_moves = get_moves(dist_dict, adj_dict, pieces, blockers)
            best_jumps = get_jumps(dist_dict, adj_dict, blockers, pieces)
            final_moves = final_movements(dist_dict, best_moves, best_jumps)
            final_move = get_piece(dist_dict, final_moves)
            pieces.append(final_move[1])
            board_dict[final_move[1]] = colour
            pieces.remove(final_move[0])
            del board_dict[final_move[0]]
            if final_move[2] == 'move':
                print("MOVE from " + str(final_move[0]) + " to " + str(final_move[1]) + ".")
            else:
                print("JUMP from " + str(final_move[0]) + " to " + str(final_move[1]) + ".")
        print_board(board_dict)


def create_dist_dict():
    dist_dict = {}
    ran = range(-3, +3 + 1)
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        dist_dict[qr] = '###'
    return dist_dict


def main():
    with open(sys.argv[1]) as test1:
        data = json.load(test1)
    # TODO: Search for and output winning sequence of moves
    # ...
    # fill board with -1 values for unfilled distance
    dist_dict = create_dist_dict()

    # empty board dictionary
    board_dict = {}

    # import data to three lists
    colour = data['colour']
    piece_data = data['pieces']
    blocks_data = data['blocks']

    # make a list of tuples of blockers
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
    empty_dict = {}
    adj_dict = get_adjacent(goals[0], empty_dict)

    for goal in goals:
        distance = 0
        distance_fill(dist_dict, adj_dict, goal, distance, blockers)
    print_board(dist_dict, 'Distance board')
    print_board(board_dict, 'Starting State of the Board', False)
    play_game(board_dict, dist_dict, adj_dict, blockers, pieces, goals, colour)


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
