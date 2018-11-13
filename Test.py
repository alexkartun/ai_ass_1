import sys

from Searcher import BFS, AStar, IDS
from State import State


def build_goal_state(size):
    """
    Creating goal state representation by size
    :param size: Size of the board
    :return: String representation of goal state
    """
    goal_state = list()
    for i in range(1, size * size):
        goal_state.append(str(i))
    goal_state.append('0')
    return '-'.join(goal_state)


# parse data from file
input_file_name = sys.argv[1]
with open(input_file_name) as input_file:
    lines = input_file.readlines()
    search_algorithm = lines[0].strip()
    board_size = int(lines[1].strip())
    init_state = lines[2].strip()

# create root and goal state of 'X puzzle'
root = State(board_size, init_state)
goal = State(board_size, build_goal_state(board_size))

# activate search algorithm depends on user's input.
with open('output.txt', 'w') as output_file:
    if search_algorithm == '1':
        action_path, developed_nodes, depth = IDS().search(root, goal)
        output_file.write(''.join(action_path) + ' ' + str(developed_nodes) + ' ' + str(depth))
    elif search_algorithm == '2':
        action_path, developed_nodes = BFS().search(root, goal)
        output_file.write(''.join(action_path) + ' ' + str(developed_nodes) + ' ' + str(0))
    elif search_algorithm == '3':
        action_path, developed_nodes, cost = AStar().search(root, goal)
        output_file.write(''.join(action_path) + ' ' + str(developed_nodes) + ' ' + str(cost))
