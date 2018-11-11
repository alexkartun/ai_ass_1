class Problem:

    def __init__(self, root, goal):
        self.root = root
        self.goal = goal

    def get_root(self):
        return self.root

    def is_goal(self, subtree_root):
        return subtree_root.is_equal(self.goal)
