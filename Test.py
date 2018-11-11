import sys

from BFS import BFS
from Problem import Problem
from State import State


input_file_name = sys.argv[1]
with open(input_file_name) as input_file:
    lines = input_file.readlines()
    search_algorithm = lines[0].strip()
    board_size = int(lines[1].strip())
    init_state = lines[2].strip()

root = State(board_size, init_state)
goal = State(board_size, '1-2-3-4-5-6-7-8-0')

if search_algorithm == '2':
    action_path, developed_nodes = BFS().search(Problem(root, goal))
print developed_nodes
for v in action_path:
    print v

