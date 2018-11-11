import sys


from Searcher import BFS, AStar, IDS
from State import State


input_file_name = sys.argv[1]
with open(input_file_name) as input_file:
    lines = input_file.readlines()
    search_algorithm = lines[0].strip()
    board_size = int(lines[1].strip())
    init_state = lines[2].strip()

root = State(board_size, init_state)
goal = State(board_size, '1-2-3-4-5-6-7-8-0')

with open('output.txt', 'w') as output_file:
    if search_algorithm == '1':
        action_path, developed_nodes, depth = IDS().search(root, goal, 10)
        output_file.write(''.join(action_path) + ' ' + str(developed_nodes) + ' ' + str(depth))
    elif search_algorithm == '2':
        action_path, developed_nodes = BFS().search(root, goal)
        output_file.write(''.join(action_path) + ' ' + str(developed_nodes) + ' ' + str(0))
    elif search_algorithm == '3':
        action_path, developed_nodes, cost = AStar().search(root, goal)
        output_file.write(''.join(action_path) + ' ' + str(developed_nodes) + ' ' + str(cost))
