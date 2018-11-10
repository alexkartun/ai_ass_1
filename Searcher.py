import sys


def breadth_first_search(problem):
    open_set = list()
    closed_set = set()
    meta = dict()
    root = problem.get_root()
    meta[root] = (None, None)
    open_set.append(root)
    while open_set:

        subtree_root = open_set.pop(0)

        if problem.is_goal(subtree_root):
            return construct_path(subtree_root, meta)

        for (child, action) in problem.get_successors(subtree_root):

            if child in closed_set:
                continue

            if child not in open_set:
                meta[child] = (subtree_root, action)
                open_set.append(child)

        closed_set.add(subtree_root)


def construct_path(state, meta):
    action_list = list()

    while meta[state][0] is not None:
        state, action = meta[state]
        action_list.append(action)

    action_list.reverse()
    return action_list


class State:

    def __init__(self, board_size, state):
        self.board_size = board_size
        self.state = state

    def get_state(self):
        return self.state

    def get_successors(self):
        successors = list()

        tokens = self.state.split('-')
        for index, token in enumerate(tokens):
            if token == '0':
                zero_row = index / self.board_size
                zero_col = index % self.board_size
                break

        if zero_row != self.board_size - 1:
            new_state = self.get_new_state((zero_row, zero_col), (zero_row + 1, zero_col), list(tokens))
            successors.append((State(self.board_size, new_state), 'U'))

        if zero_row != 0:
            new_state = self.get_new_state((zero_row, zero_col), (zero_row - 1, zero_col), list(tokens))
            successors.append((State(self.board_size, new_state), 'D'))

        if zero_col != 0:
            new_state = self.get_new_state((zero_row, zero_col), (zero_row, zero_col - 1), list(tokens))
            successors.append((State(self.board_size, new_state), 'R'))

        if zero_col != self.board_size - 1:
            new_state = self.get_new_state((zero_row, zero_col), (zero_row, zero_col + 1), list(tokens))
            successors.append((State(self.board_size, new_state), 'L'))
        return successors

    def get_new_state(self, zero_place, swap_place, tokens):
        (zero_row, zero_col) = zero_place
        (swap_row, swap_col) = swap_place
        swap_value = tokens[swap_row * self.board_size + swap_col]
        tokens[swap_row * self.board_size + swap_col] = '0'
        tokens[zero_row * self.board_size + zero_col] = swap_value
        new_state = '-'.join(tokens)
        return new_state

    def is_equal(self, state):
        return self.state == state.get_state()


class Problem:

    def __init__(self, board_size, init_state):
        self.root = State(board_size, init_state)
        goal_state = '1-2-3-4-5-6-7-8-0'
        self.goal = State(board_size, goal_state)

    def get_root(self):
        return self.root

    def is_goal(self, subtree_root):
        return subtree_root.is_equal(self.goal)

    @staticmethod
    def get_successors(subtree_root):
        return subtree_root.get_successors()


def main(argv):
    if len(argv) != 1:
        return False
    input_file_name = argv[0]
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
        search_algorithm = lines[0].strip()
        board_size = int(lines[1].strip())
        init_state = lines[2].strip()

    problem = Problem(board_size, init_state)
    if search_algorithm == '2':
        action_path = breadth_first_search(problem)
    for v in action_path:
        print v
    return True


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(-1)