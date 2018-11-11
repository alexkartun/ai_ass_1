from Searcher import Searcher


class BFS(Searcher):

    def search(self, problem):
        root = problem.get_root()
        self.meta[root] = (None, None)
        self.enqueue(root)
        while self.open_set:
            subtree_root = self.dequeue()
            if problem.is_goal(subtree_root):
                return self.construct_action_path(subtree_root), self.developed_nodes

            for (child, action) in subtree_root.get_successors():

                if child in self.closed_set:
                    continue

                if not self.is_state_in_open_set(child):
                    self.meta[child] = (subtree_root, action)
                    self.enqueue(child)

            self.closed_set.add(subtree_root)
