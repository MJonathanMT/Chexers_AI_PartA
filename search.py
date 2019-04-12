"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
"""

import sys
import json


def get_adjacent(pos, adj_dict):
    """
    This function returns all the adjacent hexes of each hex within the board
    :param pos: Position/coordinate of the current hex
    :param adj_dict: Dictionary with each hex being the key and all the adjacent
     hexes of the hex as the value
    :return: adj_dict: Complete dictionary of the adjacent hexes of all hex
     within the board
    """
    # If the current position is already a key in adj_dict, exit the recursion
    if pos in adj_dict:
        return adj_dict

    all_moves = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
    pos_val = []
    # Iterate through all moves to check if its within the board
    for move in all_moves:
        q = pos[0] + move[0]
        r = pos[1] + move[1]
        # If it is not within the board range, skip this move (continue)
        if not (abs(q) <= 3 and abs(r) <= 3 and abs(q+r) <= 3):
            continue

        # next_pos is the current position + the move
        next_pos = (q, r)

        # add the next position to the value of the current position
        pos_val.append(next_pos)

    # pass the list of all possible moves to the dictionary with the key as the
    # current position
    adj_dict[pos] = pos_val

    # Recurse through each adjacent hex of the current hex
    for val in pos_val:
        get_adjacent(val, adj_dict)

    # returns final dictionary of all adjacent hexes
    return adj_dict


def get_goals(colour, blockers):
    """
    This function returns a list of all the available goals
     that the pieces can exit from
    :param colour: The colour of the player's pieces given by the json file
    :param blockers: A list of blocked hexes
    :return: A list of all the available goals
    """
    end_points = []
    if colour == 'red':
        end_points = [(3, -3), (3, -2), (3, -1), (3, 0)]
    elif colour == 'blue':
        end_points = [(0, -3), (-1, -2), (-2, -1), (-3, 0)]
    elif colour == 'green':
        end_points = [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
    final_end_points = []

    # If the end points are not in blockers, append to the final list
    for loc in end_points:
        if loc not in blockers:
            final_end_points.append(loc)

    # Returns the final list of end_points/goals
    return final_end_points


def distance_fill(dist_dict, adj_dict, pos, dist, blockers):
    """
    This function creates a dictionary which has values of the shortest
     distance to the nearest goal
    :param dist_dict: Dictionary containing the distance to the nearest goal
    :param adj_dict: Dictionary of all adjacent hexes
    :param pos: Current position on the board
    :param dist: Current distance from the goal
    :param blockers: A list of blocked hexes
    :return: A complete dictionary with coordinates/positions as key
     and the distance to the nearest goal as the value
    """
    dist += 1
    # These '###' represents an unvisited hex
    if dist_dict[pos] == '###':
        dist_dict[pos] = dist
    # If distance is bigger than the distance in the dictionary,
    # exit from the recursion
    elif dist > dist_dict[pos]:
        return 0
    # If distance is less, change the value in the dictionary
    elif dist < dist_dict[pos]:
        dist_dict[pos] = dist

    next_jump = ()
    for next_pos in adj_dict[pos]:
        movable = True
        jumpable = True

        # Set movable to False if it is blocked
        if next_pos in blockers:
            movable = False

        # Check if can jump over the blocked piece, only happens when
        # the next piece is a blocked piece
        if not movable:
            q_move = (next_pos[0] - pos[0])*2
            r_move = (next_pos[1] - pos[1])*2
            next_jump = (pos[0] + q_move, pos[1] + r_move)
            if next_jump not in adj_dict[next_pos] or next_jump in blockers:
                jumpable = False

        # Recurse through the appropriate movement: move or jump
        if movable:
            distance_fill(dist_dict, adj_dict, next_pos, dist, blockers)
        elif jumpable:
            distance_fill(dist_dict, adj_dict, next_jump, dist, blockers)

    return dist_dict


def get_moves(dist_dict, adj_dict, pieces, blockers):
    """
    This function gets the best move for each of the pieces on the board
    :param dist_dict: Dictionary containing the distance to the nearest goal
    :param adj_dict: Dictionary of all adjacent hexes
    :param pieces: List of all the existing pieces on the board
    :param blockers: A list of blocked hexes
    :return: Returns the best move of each piece on the board
    """
    best_moves = {}
    for piece in pieces:
        movement = []
        shortest_dist = 0
        best_move = ()
        for next_move in adj_dict[piece]:
            # Skips move if there is another piece in front of it or
            # if there is a blocked hex
            if next_move in pieces or next_move in blockers:
                continue

            # the best move is where the distance of the next
            # location is the closest to the goal
            if shortest_dist == 0:
                shortest_dist = dist_dict[next_move]
                best_move = next_move
            elif dist_dict[next_move] < shortest_dist:
                shortest_dist = dist_dict[next_move]
                best_move = next_move

        # if the best move makes the piece go backward
        # (Worsen the piece condition) remove the best move instead
        if best_move != () and dist_dict[piece] <= dist_dict[best_move]:
            best_move = ()

        # Each value of the position contains the current position
        # and next position
        movement.append(piece)
        movement.append(best_move)
        best_moves[piece] = movement

    return best_moves


def get_jumps(dist_dict, adj_dict, blockers, pieces):
    """
    This function gets the best jump for each of the pieces on the board
    :param dist_dict: Dictionary containing the distance to the nearest goal
    :param adj_dict: Dictionary of all adjacent hexes
    :param blockers: A list of blocked hexes
    :param pieces: List of all the existing pieces on the board
    :return: Returns the best jump of each piece on the board
    """
    best_jumps = {}
    for piece in pieces:
        shortest_dist = 0
        jumping = []
        best_jump = ()
        for next_move in adj_dict[piece]:
            # Skips if the next move is an empty hex,
            # this means its not jumpable
            if next_move not in blockers and next_move not in pieces:
                continue
            q_move = (next_move[0] - piece[0])*2
            r_move = (next_move[1] - piece[1])*2
            next_jump = (piece[0] + q_move, piece[1] + r_move)
            # Skips the next jump if the next jump location is
            # another piece, a block or it isn't within the board
            if (next_jump not in adj_dict[next_move]
                    or next_jump in pieces
                    or next_jump in blockers):
                continue

            # the best jump is where the distance of the next
            # location is the closest to the goal
            if shortest_dist == 0:
                shortest_dist = dist_dict[next_jump]
                best_jump = next_jump
            elif dist_dict[next_jump] < shortest_dist:
                shortest_dist = dist_dict[next_jump]
                best_jump = next_jump

        # if the best jump makes the piece go backward
        # (Worsen the piece condition) remove the best jump instead
        if best_jump != () and dist_dict[piece] <= dist_dict[best_jump]:
            best_jump = ()

        # Each value of the position contains the current position
        # and next position
        jumping.append(piece)
        jumping.append(best_jump)
        best_jumps[piece] = jumping

    return best_jumps


def final_movements(dist_dict, best_moves, best_jumps):
    """
    This function chooses whether each piece should do a move or jump action
    :param dist_dict: Dictionary containing the distance to the nearest goal
    :param best_moves: Dictionary containing the best move of each piece
    :param best_jumps: Dictionary containing the best jump of each piece
    :return: The best action each piece should take whether its a move or a jump
    """
    final_moves = {}
    for piece in best_moves:
        move = best_moves[piece][1]
        # If there are no jump action, make the best action the move action
        if best_jumps[piece][1] == ():
            final_moves[piece] = best_moves[piece]
            final_moves[piece].append('move')
            continue

        # If there are no move action, make the best action the jump action
        if move == ():
            final_moves[piece] = best_jumps[piece]
            final_moves[piece].append('jump')
            continue

        # Choose the action based on the next location the piece lands in.
        # Choose the action that pushes the piece closer to the goal
        jump = best_jumps[piece][1]
        if dist_dict[move] < dist_dict[jump]:
            final_moves[piece] = best_moves[piece]
            final_moves[piece].append('move')
        else:
            final_moves[piece] = best_jumps[piece]
            final_moves[piece].append('jump')

    return final_moves


def get_piece(dist_dict, final_moves):
    """
    This function choose the best piece to move amongst the piece on the board
    :param dist_dict: Dictionary containing the distance to the nearest goal
    :param final_moves: Dictionary containing the best action for each piece
    :return: The piece that is best to move given the current board position
    """
    final_move = []
    dist = 0
    for piece in final_moves:
        # Skip this piece if there aren't any good action available
        if final_moves[piece][1] == ():
            continue

        if dist == 0:
            dist = dist_dict[piece]
            final_move = final_moves[piece]

        # Choose the piece that is further away from the goal
        elif dist_dict[piece] > dist:
            dist = dist_dict[piece]
            final_move = final_moves[piece]

        # If the same distance away from the goal,
        # choose piece with the jump action
        elif dist_dict[piece] == dist:
            if final_moves[piece][2] == 'jump':
                final_move = final_moves[piece]

    return final_move


def play_game(board_dict, dist_dict, adj_dict, blockers, pieces, goals, colour):
    """
    This function is the main game play function where it loops until
     there are no more remaining piece on the board
    :param board_dict: A dictionary containing the items on the
     board including player's 'coloured' pieces and blacked hexes
    :param dist_dict: Dictionary containing the distance to the nearest goal
    :param adj_dict: Dictionary of all adjacent hexes
    :param blockers: A list of blocked hexes
    :param pieces: A list of coordinates of the pieces on the board
    :param goals: A list of available exits for the player's coloured pieces
    :param colour: The colour of the player's pieces
    """
    # Maintains looping as long as there are pieces on the board
    while pieces:
        # If any of the pieces are on the goals/end_points, exit them out
        exit_move = False
        for piece in pieces:
            if piece in goals:
                print("EXIT from " + str(piece) + ".")
                del board_dict[piece]
                pieces.remove(piece)
                exit_move = True
                break
        # If none of the pieces exited this turn, do an action
        if not exit_move:
            # Get the best move possible for each piece
            best_moves = get_moves(dist_dict, adj_dict, pieces, blockers)

            # Get the best jump possible for each piece
            best_jumps = get_jumps(dist_dict, adj_dict, blockers, pieces)

            # Get the best action possible for each piece
            final_moves = final_movements(dist_dict, best_moves, best_jumps)

            # Choose the best piece to move
            final_move = get_piece(dist_dict, final_moves)
            pieces.append(final_move[1])
            board_dict[final_move[1]] = colour
            pieces.remove(final_move[0])
            del board_dict[final_move[0]]

            # Print action based on assignment specification
            if final_move[2] == 'move':
                print("MOVE from " + str(final_move[0])
                      + " to " + str(final_move[1]) + ".")
            else:
                print("JUMP from " + str(final_move[0])
                      + " to " + str(final_move[1]) + ".")


def create_dist_dict():
    """
    This function creates an unvisited distance dictionary filled with '###'
    :return: Returns unvisited distance dictionary
    """
    dist_dict = {}
    ran = range(-3, +3 + 1)
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        dist_dict[qr] = '###'
    return dist_dict


def main():
    """
    Main function called to import json file and play the game
    """
    # Importing data from json file
    with open(sys.argv[1]) as test1:
        data = json.load(test1)

    # Create an unvisited distance dictionary
    dist_dict = create_dist_dict()

    # Empty board dictionary
    board_dict = {}

    # Split imported data to three lists
    colour = data['colour']
    piece_data = data['pieces']
    blocks_data = data['blocks']

    # Data is a list of list
    # Change to a list of tuples
    blockers = []
    for blocks in blocks_data:
        blocks = tuple(blocks)
        blockers.append(blocks)
        board_dict[blocks] = '###'

    # Change pieces to list of tuples
    pieces = []
    for piece in piece_data:
        piece = tuple(piece)
        pieces.append(piece)
        board_dict[piece] = colour

    # Get a list of available exits/end_points
    goals = get_goals(colour, blockers)

    # Get all available adjacent hexes within the board range
    empty_dict = {}
    adj_dict = get_adjacent(goals[0], empty_dict)

    # Fill distance dictionary with the least distance from each goal
    for goal in goals:
        distance = 0
        dist_dict = distance_fill(dist_dict, adj_dict, goal, distance, blockers)

    # Play Single-player Chexers
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
