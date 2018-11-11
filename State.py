class State:

    def __init__(self, board_size, state):
        self.board_size = board_size
        self.state = state

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

        if zero_col != 0:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row, zero_col - 1), list(tokens))
            successors.append((State(self.board_size, new_state), 'R'))

        if zero_col != self.board_size - 1:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row, zero_col + 1), list(tokens))
            successors.append((State(self.board_size, new_state), 'L'))
        return successors

    def create_new_state(self, zero_place, swap_place, tokens):
        (zero_row, zero_col) = zero_place
        (swap_row, swap_col) = swap_place
        swap_value = tokens[swap_row * self.board_size + swap_col]
        tokens[swap_row * self.board_size + swap_col] = '0'
        tokens[zero_row * self.board_size + zero_col] = swap_value
        new_state = '-'.join(tokens)
        return new_state

    def is_equal(self, s):
        return self.state == s.state
