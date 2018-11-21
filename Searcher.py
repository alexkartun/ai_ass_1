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
        raise Exception("Problem can not be solved.")


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
        raise Exception("Problem can not be solved.")


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
                status, action_path, remaining = self.dfs_by_depth(root, goal, depth)
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
