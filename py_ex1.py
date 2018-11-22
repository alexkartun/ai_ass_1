import sys
import heapq


class Searcher(object):
    """
    Abstract class 'Searcher'. Contains open_set, meta and developed_nodes indicator
    """
    def __init__(self):
        self.open_set = list()
        # map node/state to tuple of (parent node/state, operation to this state)
        self.meta = dict()
        self.developed_nodes = 0
        self.algorithm_cost = 0

    def construct_action_path(self, state):
        """
        Produce a backtrace of the actions taken to find the goal node, using the
        recorded meta dictionary
        :param state: State/node to start backtracking from
        :return: Action path
        """
        action_list = list()
        # Continue until you reach root meta data (i.e. (None, None))
        while self.meta[state][0] is not None:
            state, action = self.meta[state]
            action_list.append(action)

        action_list.reverse()
        return action_list


class BFS(Searcher):
    """
    BFS class extending Searcher class for reuse of duplicated code like construction the path.
    """
    def search(self, root, goal):
        """
        Searching algorithm of BFS using list as queue and looking for path from root to goal.
        :param root: Initial state.
        :param goal: Goal state.
        :return: The path from init to goal.
        """
        # init
        self.meta[root] = (None, None)
        self.open_set.append(root)
        # For each node on the current level expand and process, if no children (leaf) then unwind.
        while self.open_set:
            self.developed_nodes += 1
            subtree_root = self.open_set.pop(0)
            # We found the node we wanted so stop and emit a path.
            if goal == subtree_root:
                return self.construct_action_path(subtree_root), self.developed_nodes, self.algorithm_cost
            # For each child of the current tree process
            for child in subtree_root.get_successors():
                self.meta[child] = (subtree_root, child.get_action_operator())
                self.open_set.append(child)


class AStar(Searcher):
    """
    AStar class extending Searcher class for reuse of duplicated code like construction the path.
    """
    def __init__(self):
        Searcher.__init__(self)
        # Create priority queue
        heapq.heapify(self.open_set)

    def search(self, root, goal):
        """
        Searching algorithm of AStar using list as priority queue and looking for path from root to goal.
        Algorithm using manhattan heuristics.
        :param root: Initial state.
        :param goal: Goal state.
        :return: The path from init to goal.
        """
        # Init
        self.meta[root] = (None, None)
        heapq.heappush(self.open_set, root)
        # For each node on the current level expand and process, if no children (leaf) then unwind.
        while self.open_set:
            self.developed_nodes += 1
            subtree_root = heapq.heappop(self.open_set)
            # We found the node we wanted so stop and emit a path.
            if goal == subtree_root:
                self.algorithm_cost = subtree_root.get_g()
                return self.construct_action_path(subtree_root), self.developed_nodes, self.algorithm_cost
            # For each child of the current tree process
            for child in subtree_root.get_successors():
                child.set_g(subtree_root.get_g() + subtree_root.get_cost())
                child.set_h(child.heuristic_function())
                self.meta[child] = (subtree_root, child.get_action_operator())
                heapq.heappush(self.open_set, child)


class IDS(Searcher):
    """
    IDS class extending Searcher class for reuse of duplicated code like construction the path.
    """
    def search(self, root, goal):
        """
        Searching algorithm of IDS using DFS algorithm depth by depth. For each depth executing DFS to search
        over all the nodes that don't pass the current depth. If found in specific depth return the path. Otherwise
        increase the depth by 1 and execute DFS again.
        Algorithm using manhattan heuristics.
        :param root: Initial state.
        :param goal: Goal state.
        :return: The path from init to goal.
        """
        # Init
        depth = 0
        self.meta[root] = (None, None)
        # Iterate over all depths from 0 to max_depth
        while True:
                # Calling DFS search util that will search not beyond the depth threshold.
                status, action_path = self.dfs_by_depth(root, goal, depth)
                # If DFS found path to goal node return the action path
                if status:
                    self.algorithm_cost = depth
                    return action_path, self.developed_nodes, self.algorithm_cost
                # Reset the developed nodes indicator for next iteration and increase the depth.
                depth += 1
                self.developed_nodes = 0

    def dfs_by_depth(self, root, goal, depth):
        """
        Searching for goal state in tree until current depth.
        :param root: Init state.
        :param goal: Goal state.
        :param depth: The current depth. The algorithm will not pass it.
        :return:
        """
        # Increase indicator of developed nodes
        self.developed_nodes += 1
        # 1st stopping case. Check if root is goal node. If yes return action path
        if goal == root:
            return True, self.construct_action_path(root)
        # 2nd stopping case
        if depth <= 0:
            return False, None
        # For each child of the current tree process
        for child in root.get_successors():
            self.meta[child] = (root, child.get_action_operator())
            # Call recursively to search util with new subtree to explore with lower depth
            status, action_path = self.dfs_by_depth(child, goal, depth - 1)
            # Is processed subtree found path, so return it
            if status:
                return True, action_path
        # Otherwise no path found on this subtree
        return False, None


class State(object):
    def __init__(self, b_size, state, action_operator=None):
        self.board_size = b_size
        self.state = state
        # Cost of each move
        self.cost = 1
        # Heuristic value of this node
        self.h = 0
        # Path cost from root node to this node
        self.g = 0
        # operator that bring to this state
        self.action_operator = action_operator

    def get_cost(self):
        return self.cost

    def get_action_operator(self):
        return self.action_operator

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
            successors.append(State(self.board_size, new_state, 'U'))
        # Check potential movement down
        if zero_row != 0:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row - 1, zero_col), list(tokens))
            successors.append(State(self.board_size, new_state, 'D'))
        # Check potential movement left
        if zero_col != self.board_size - 1:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row, zero_col + 1), list(tokens))
            successors.append(State(self.board_size, new_state, 'L'))
        # Check potential movement right
        if zero_col != 0:
            new_state = self.create_new_state((zero_row, zero_col), (zero_row, zero_col - 1), list(tokens))
            successors.append(State(self.board_size, new_state, 'R'))
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

    def evaluate_operator(self):
        if self.action_operator == 'U':
            return 4
        elif self.action_operator == 'D':
            return 3
        elif self.action_operator == 'L':
            return 2
        else:
            return 1

    def __cmp__(self, other):
        """
        Comparator overloading. Deciding which state is with higher priority.
        Priority queue of states use this operator to decide which state is has higher priority.
        :param other: Other state to compare
        :return: Which element is with higher priority.
        """
        # checking h + g value
        res = cmp(self.g + self.h, other.g + other.h)
        if res == 0:
            # h + g values are same so decide by their depth.
            res = cmp(self.g, other.g)
            # their depths are equal.
            if res == 0:
                # decide by operator value
                return cmp(self.evaluate_operator(), other.evaluate_operator())
        # Otherwise first or second if was not executed so return the res value.
        return res

    def __eq__(self, other):
        """
        Operator == overloading. Check if current state equals to other state.
        :param other: Other state.
        :return: True = equal, False - otherwise.
        """
        return self.state == other.state


def build_goal_state(size):
    """
    Creating goal state representation by size
    :param size: Size of the board
    :return: String representation of goal state
    """
    goal_s = [str(i) for i in range(1, size * size)]
    goal_s.append('0')
    return '-'.join(goal_s)


if __name__ == '__main__':
    # parse data from file
    input_file_name = sys.argv[1]
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
    search_algorithm = lines[0].strip()
    board_size = int(lines[1].strip())
    init_state = lines[2].strip()

    # create root and goal state of 'X puzzle'
    root_state = State(board_size, init_state)
    goal_state = State(board_size, build_goal_state(board_size))

    # activate search algorithm depends on user's input.
    if search_algorithm == '1':
        path, developed_nodes, algorithm_cost = IDS().search(root_state, goal_state)
    elif search_algorithm == '2':
        path, developed_nodes, algorithm_cost = BFS().search(root_state, goal_state)
    else:
        path, developed_nodes, algorithm_cost = AStar().search(root_state, goal_state)

    output = '{} {} {}'.format(''.join(path), str(developed_nodes), str(algorithm_cost))
    with open('output.txt', 'w') as output_file:
        output_file.write(output)
