class State(object):

    def __init__(self, board_size, state):
        self.board_size = board_size
        self.state = state
        self.cost = 1
        self.h = 0
        self.g = 0

    def get_cost(self):
        return self.cost

    def get_state(self):
        return self.state

    def get_board_size(self):
        return self.board_size

    def get_h(self):
        return self.h

    def get_g(self):
        return self.g

    def set_h(self, h):
        self.h = h

    def set_g(self, g):
        self.g = g

    def get_successors(self):
        successors = list()

        tokens = self.state.split('-')
        zero_index = tokens.index('0')
        zero_row = zero_index / self.board_size
        zero_col = zero_index % self.board_size

        if zero_row != self.board_size - 1:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row + 1, zero_col), list(tokens))
            successors.append((State(self.board_size, new_state), 'U'))

        if zero_row != 0:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row - 1, zero_col), list(tokens))
            successors.append((State(self.board_size, new_state), 'D'))

        if zero_col != self.board_size - 1:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row, zero_col + 1), list(tokens))
            successors.append((State(self.board_size, new_state), 'L'))

        if zero_col != 0:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row, zero_col - 1), list(tokens))
            successors.append((State(self.board_size, new_state), 'R'))

        return successors

    def create_new_state(self, zero_place, swap_place, tokens):
        (zero_row, zero_col) = zero_place
        (swap_row, swap_col) = swap_place
        swap_value = tokens[swap_row * self.board_size + swap_col]
        tokens[swap_row * self.board_size + swap_col] = '0'
        tokens[zero_row * self.board_size + zero_col] = swap_value
        new_state = '-'.join(tokens)
        return new_state

    def heuristic_function(self):
        h = 0
        for ind, s in enumerate(self.state.split('-')):
            if not s == '0':
                value = int(s)
                current_row = ind / self.board_size
                current_col = ind % self.board_size
                target_row = (value - 1) / self.board_size
                target_col = (value - 1) % self.board_size
                h += abs(current_row - target_row) + abs(current_col - target_col)
        return h

    def __cmp__(self, other):
        return cmp(self.g + self.h, other.g + other.h)

    def is_equal(self, s):
        return self.state == s.state

