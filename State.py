class State(object):
    def __init__(self, board_size, state):
        self.board_size = board_size
        self.state = state
        # Cost of each move
        self.cost = 1
        # Heuristic value of this node
        self.h = 0
        # Path cost from root node to this node
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
        """
        Get list of all potential states from this state
        :return: List of states
        """
        successors = list()
        # Get zero row and col in this state
        tokens = self.state.split('-')
        zero_index = tokens.index('0')
        zero_row = zero_index / self.board_size
        zero_col = zero_index % self.board_size
        # Check potential movement up
        if zero_row != self.board_size - 1:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row + 1, zero_col), list(tokens))
            successors.append((State(self.board_size, new_state), 'U'))
        # Check potential movement down
        if zero_row != 0:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row - 1, zero_col), list(tokens))
            successors.append((State(self.board_size, new_state), 'D'))
        # Check potential movement left
        if zero_col != self.board_size - 1:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row, zero_col + 1), list(tokens))
            successors.append((State(self.board_size, new_state), 'L'))
        # Check potential movement right
        if zero_col != 0:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row, zero_col - 1), list(tokens))
            successors.append((State(self.board_size, new_state), 'R'))
        return successors

    def create_new_state(self, zero_place, swap_place, tokens):
        """
        Create new string representation of state by swapping zero value with swapped value
        :param zero_place: Tuple (zero_row, zero_col)
        :param swap_place: Tuple (swap_row, swap_col)
        :param tokens: List of all values in state
        :return: New string repr of state
        """
        (zero_row, zero_col) = zero_place
        (swap_row, swap_col) = swap_place
        swap_value = tokens[swap_row * self.board_size + swap_col]
        tokens[swap_row * self.board_size + swap_col] = '0'
        tokens[zero_row * self.board_size + zero_col] = swap_value
        new_state = '-'.join(tokens)
        return new_state

    def heuristic_function(self):
        """
        Calculating heuristic value of this node by using manhattan distances
        :return: Heuristic value of this node
        """
        h = 0
        # Iterate over all values in this state, except 0
        for ind, s in enumerate(self.state.split('-')):
            if not s == '0':
                value = int(s)
                # Calculate current row and col of the value
                current_row = ind / self.board_size
                current_col = ind % self.board_size
                # Calculate target row and col of the value. Meaning the correct place in goal solution
                target_row = (value - 1) / self.board_size
                target_col = (value - 1) % self.board_size
                # Add the differences between current place to target place
                h += abs(current_row - target_row) + abs(current_col - target_col)
        return h

    def __cmp__(self, other):
        """
        Comparing function of nodes by their heuristic + cost to this node
        Priority queue of nodes use this function to decide higher priority of two nodes
        :param other: Other node to compare
        :return: Which element is bigger
        """
        return cmp(self.g + self.h, other.g + other.h)

    def is_equal(self, s):
        """
        Check node's string representation of state to other(s) node's state
        :param s: Node to check with
        :return: True if equal, False otherwise
        """
        return self.state == s.state
