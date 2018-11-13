import heapq


class Searcher(object):
    """
    Abstract class 'Searcher'. Contains open_set, closed_set, meta and developed_nodes indicator
    """
    def __init__(self):
        self.open_set = list()
        self.closed_set = set()
        # map node/state to tuple of (parent node/state, operation to this state)
        self.meta = dict()
        self.developed_nodes = 0

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
    def search(self, root, goal):
        # Init
        self.meta[root] = (None, None)
        self.enqueue(root)
        # For each node on the current level expand and process, if no children
        # (leaf) then unwind
        while self.open_set:
            subtree_root = self.dequeue()
            # We found the node we wanted so stop and emit a path.
            if goal.is_equal(subtree_root):
                return self.construct_action_path(subtree_root), self.developed_nodes
            # For each child of the current tree process
            for (child, action) in subtree_root.get_successors():
                # The node has already been processed, so skip over it
                if child in self.closed_set:
                    continue
                # The child is not enqueued to be processed, so enqueue this level of
                # children to be expanded
                self.meta[child] = (subtree_root, action)
                self.enqueue(child)
            # We finished processing the root of this subtree, so add it to the closed set
            self.closed_set.add(subtree_root)

    def dequeue(self):
        """
        Pop first node from queue and increase developed nodes indicator
        :return: First node
        """
        self.developed_nodes += 1
        return self.open_set.pop(0)

    def enqueue(self, state):
        """
        Insert node to the end of the queue
        :param state: Node we want to insert
        :return:
        """
        self.open_set.append(state)


class AStar(Searcher):
    def __init__(self):
        Searcher.__init__(self)
        # Create priority queue
        heapq.heapify(self.open_set)

    def search(self, root, goal):
        # Init
        self.meta[root] = (None, None)
        self.enqueue(root)
        # For each node on the current level expand and process, if no children
        # (leaf) then unwind
        while self.open_set:
            subtree_root = self.dequeue()
            # We found the node we wanted so stop and emit a path.
            if goal.is_equal(subtree_root):
                return self.construct_action_path(subtree_root), self.developed_nodes, subtree_root.get_g()
            # For each child of the current tree process
            for (child, action) in subtree_root.get_successors():
                # The node has already been processed, so skip over it
                if child in self.closed_set:
                    continue
                child.set_g(subtree_root.get_g() + subtree_root.get_cost())
                child.set_h(child.heuristic_function())
                # The child is not enqueued to be processed, so enqueue this level of
                # children to be expanded
                self.meta[child] = (subtree_root, action)
                self.enqueue(child)
            # We finished processing the root of this subtree, so add it to the closed set
            self.closed_set.add(subtree_root)

    def dequeue(self):
        """
        Pop node with highest priority from the queue and increase developed nodes indicator
        :return: Node with highest priority
        """
        self.developed_nodes += 1
        return heapq.heappop(self.open_set)

    def enqueue(self, state):
        """
        Insert new node to the priority queue
        :param state: Node we want to insert
        :return:
        """
        heapq.heappush(self.open_set, state)


class IDS(Searcher):
    def search(self, root, goal):
        # Init
        depth = 0
        self.meta[root] = (None, None)
        # Iterate over all depths from 0 to max_depth
        while True:
                # Calling DFS search util that will search not beyond the depth threshold.
                status, action_path = self.search_util(root, goal, depth)
                print depth
                # If DFS found path to goal node return the action path
                if status:
                    return action_path, self.developed_nodes, depth
                # Reset the developed nodes indicator for next iteration
                depth += 1
                self.developed_nodes = 0

    def search_util(self, root, goal, depth):
        # Increase indicator of developed nodes
        self.developed_nodes += 1
        # 1st stopping case. Check if root is goal node. If yes return action path
        if goal.is_equal(root):
            return True, self.construct_action_path(root)
        # 2nd stopping case
        if depth <= 0:
            return False, None
        # For each child of the current tree process
        for (child, action) in root.get_successors():
            self.meta[child] = (root, action)
            # Call recursively to search util with new subtree to explore with lower depth
            status, action_path = self.search_util(child, goal, depth - 1)
            # Is processed subtree found path, so return it
            if status:
                return True, action_path
        # Otherwise no path found on this subtree
        return False, None
