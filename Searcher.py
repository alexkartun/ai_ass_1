import heapq


class Searcher(object):
    def __init__(self):
        self.open_set = list()
        self.closed_set = set()
        self.meta = dict()
        self.developed_nodes = 0

    def construct_action_path(self, state):
        action_list = list()

        while self.meta[state][0] is not None:
            state, action = self.meta[state]
            action_list.append(action)

        action_list.reverse()
        return action_list


class BFS(Searcher):

    def search(self, root, goal):
        self.meta[root] = (None, None)
        self.enqueue(root)
        while self.open_set:
            subtree_root = self.dequeue()
            if goal.is_equal(subtree_root):
                return self.construct_action_path(subtree_root), self.developed_nodes

            for (child, action) in subtree_root.get_successors():
                if child in self.closed_set:
                    continue
                self.meta[child] = (subtree_root, action)
                self.enqueue(child)

            self.closed_set.add(subtree_root)

    def dequeue(self):
        self.developed_nodes += 1
        return self.open_set.pop(0)

    def enqueue(self, state):
        self.open_set.append(state)


class AStar(Searcher):

    def __init__(self):
        Searcher.__init__(self)
        heapq.heapify(self.open_set)

    def search(self, root, goal):
        self.meta[root] = (None, None)
        self.enqueue(root)
        while self.open_set:
            subtree_root = self.dequeue()
            if goal.is_equal(subtree_root):
                return self.construct_action_path(subtree_root), self.developed_nodes, subtree_root.get_g()
            for (child, action) in subtree_root.get_successors():
                if child in self.closed_set:
                    continue
                child.set_g(subtree_root.get_g() + subtree_root.get_cost())
                child.set_h(child.heuristic_function())
                self.meta[child] = (subtree_root, action)
                self.enqueue(child)
            self.closed_set.add(subtree_root)

    def dequeue(self):
        self.developed_nodes += 1
        return heapq.heappop(self.open_set)

    def enqueue(self, state):
        heapq.heappush(self.open_set, state)


class IDS(Searcher):

    def search(self, root, goal, max_depth):
        self.meta[root] = (None, None)
        for depth in range(max_depth):
            status, action_path = self.search_util(root, goal, depth)
            if status:
                return action_path, self.developed_nodes, depth
            self.developed_nodes = 0

    def search_util(self, root, goal, depth):
        self.developed_nodes += 1
        if goal.is_equal(root):
            return True, self.construct_action_path(root)
        if depth <= 0:
            return False, None

        for (child, action) in root.get_successors():
            self.meta[child] = (root, action)
            status, action_path = self.search_util(child, goal, depth - 1)
            if status:
                return True, action_path
        return False, None

