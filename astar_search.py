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
BLOCK_HEXTYPE = 'blocks'
COLOUR_PIECE_HEXTYPE = 'colour_pieces'
EXITPOINT_HEXTYPE = 'exitpoint'

##################################### CLASS FOR GAME BOARD START #####################################
class GameBoard:
  def __init__(self):

    # A dictionary of key:value format -> 'hextype':[list of coordinates]
    # hextype can be 'blocks', 'colour_pieces'
    # if coordinate is not in self.hexes, it means that it's an empty hex
    self.hexes = {}
    self.colour_in_play = ''
    self.exitpoints = []
    # Board dictionary for visualisation purposes
    self.board_dict = {}

  # Check if coordinate is a block or not
  def isSteppable(self, current_hex):
    return (not current_hex in self.hexes.get(BLOCK_HEXTYPE))
  
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
    return ((not next_hex in self.hexes.get(BLOCK_HEXTYPE)) and (not next_hex in self.hexes.get(COLOUR_PIECE_HEXTYPE)) and (self.in_bounds(next_hex)), next_hex)


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
      if not self.isSteppable(step):
        is_jumpable_result = self.isJumpable(step, current_hex)
        if is_jumpable_result[0]:
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
  x = hex[0]
  z = hex[1]
  y = -x-z
  return (x, y, z) 

def hex_distance(a, b):
  a_cube = axial_to_cube(a)
  b_cube = axial_to_cube(b)
  return cube_distance(a_cube, b_cube)

def cube_distance(a, b):
  return (abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])) / 2

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
    if (not location in board.hexes.get(BLOCK_HEXTYPE)):
      exit_points.append(location)

  return exit_points

# Heuristic function for a_star_search
# Currently it's the same as hex_distance function, but can be changed in the future if there are better heuristics
def heuristic(start, end):
  return hex_distance(start, end)

# Returns a tuple in the form: (closest goal from current, heuristic distance)
def find_closest_heuristic_goal(current, goals):
  # Set first goal as standard comparing heuristic
  closest_goal = goals[0]
  shortest_heuristic = heuristic(current, goals[0])
  for goal in goals[1:]: 
    closest_goal = goal
    if heuristic(current, goal) < shortest_heuristic:
      shortest_heuristic = heuristic(current, goal)
      closest_goal = goal

  return (closest_goal, shortest_heuristic)

# Returns came_from, i.e. a dictionary of key-value pair {hex: previous hex}
def a_star_search(board, start):
  frontier = PriorityQueue()
  frontier.put(start, 0)
  came_from = {}
  cost_so_far = {}
  cost_so_far[start] = 0
  goals = board.exitpoints

  while not frontier.empty():
    current = frontier.get()

    if (current in goals):
      break

    for next_move in board.next_possible_moves(current):
      # Every move (either step or jump) has cost 1
      new_cost = cost_so_far[current] + 1
      if next_move not in cost_so_far or new_cost < cost_so_far[next_move]:
        cost_so_far[next_move] = new_cost
        if len(goals) > 1:
          closest_goal = find_closest_heuristic_goal(next_move, goals)
        else:
          closest_goal = (goals[0], heuristic(next_move, goals[0]))
        priority = new_cost + closest_goal[1]
        frontier.put(next_move, priority)
        came_from[next_move] = current

  return came_from

# Playing the game using a_star_search algorithm
def play_game(board, colour):
  all_starting_colour_pieces = board.hexes.get(COLOUR_PIECE_HEXTYPE).copy()
  for colour_piece in all_starting_colour_pieces:
    print("piece in play is")
    print(colour_piece)
    # path is the path that the colour_piece will take to exit the board
    # data structure: stack (first in, last out)
    a_star_search_results = a_star_search(board, colour_piece)
    for hex in a_star_search_results.keys():
      if hex in board.exitpoints:
        exitpoint = hex
    path = get_path(a_star_search_results, colour_piece, exitpoint)
    print("blocks are")
    print(board.hexes.get(BLOCK_HEXTYPE))
    print("\n")
    print("path is")
    print(path)
    current_piece_coordinate = colour_piece
    while path:
      next_in_path = path.pop()
      # Change hex dictionary in game_board to adapt to the new step/jump, i.e. change the colour_piece's coordinates
      colour_piece_list = board.hexes.get(COLOUR_PIECE_HEXTYPE).copy()
      colour_piece_list.remove(current_piece_coordinate)
      colour_piece_list.append(next_in_path)
      board.hexes[COLOUR_PIECE_HEXTYPE] = colour_piece_list

      # Change board dictionary in game_board to adapt as well (visualisation purposes)
      board_dict_copy = board.board_dict.copy()
      board_dict_copy.pop(current_piece_coordinate)
      board_dict_copy.update({next_in_path: board.colour_in_play})
      board.board_dict = board_dict_copy

      current_piece_coordinate = next_in_path

      print_board(board.board_dict, "first a_star test", debug=False)
    
    if next_in_path in board.exitpoints:
      exit_board(next_in_path, board)
    
# When a colour_piece successfully exits the board
def exit_board(colour_piece, board):


  colour_piece_list = board.hexes.get(COLOUR_PIECE_HEXTYPE).copy()
  colour_piece_list.remove(colour_piece)
  board.hexes[COLOUR_PIECE_HEXTYPE] = colour_piece_list

  board_dict_copy = board.board_dict.copy()
  board_dict_copy.pop(colour_piece)
  board.board_dict = board_dict_copy
  print_board(board.board_dict, "first a_star test", debug=False)



# Gets the path for the current colour_piece to exit board based on the a_star_search algorithm
def get_path(came_from_dict, start, end):
  if start == end:
    return []
  path =  [end] + get_path(came_from_dict, start, came_from_dict.get(end))
  return path
      

##################################### MAIN AND PRINT HELPER #####################################

def main():
  with open(sys.argv[1]) as file:
    data = json.load(file)
  
  board_dict = {}
  # Initiate Game Board
  game_board = GameBoard()

  colour_in_play = data['colour']
  game_board.colour_in_play = colour_in_play
  blocks = []
  colour_pieces = []
  exitpoints = []

  # Update game_board hexes with blocks coordinates
  for block in data['blocks']:
    block = tuple(block)
    blocks.append(block)
    board_dict[block] = '###'
  game_board.hexes[BLOCK_HEXTYPE] = blocks

  # Update game_board hexes with colour_pieces coordinates
  for piece in data['pieces']:
    piece = tuple(piece)
    colour_pieces.append(piece)
    board_dict[piece] = colour_in_play
  game_board.hexes[COLOUR_PIECE_HEXTYPE] = colour_pieces

  # Update game_board hexes with exitpoint coordinates     
  for goal in get_goals(colour_in_play, game_board):
    exitpoints.append(goal)
  game_board.exitpoints = exitpoints
  game_board.board_dict = board_dict

  play_game(game_board, colour_in_play)


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
      
  for (q, r) in [(q,r) for q in ran for r in ran if -q-r in ran]:
    if (q, r) in board_dict:
      cell = str(board_dict[(q, r)]).center(5)
    else:
      cell = "     " # 5 spaces will fill a cell
    cells.append(cell)

  # fill in the template to create the board drawing, then print!
  board = template.format(message, *cells)
  print(board, **kwargs)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
  main()
