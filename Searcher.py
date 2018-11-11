class Searcher:

    def __init__(self):
        self.open_set = list()
        self.closed_set = set()
        self.meta = dict()
        self.developed_nodes = 0

    def dequeue(self):
        self.developed_nodes += 1
        return self.open_set.pop(0)

    def enqueue(self, state):
        self.open_set.append(state)

    def is_state_in_open_set(self, state):
        for s in self.open_set:
            if s.is_equal(state):
                return True
        return False

    def construct_action_path(self, state):
        action_list = list()

        while self.meta[state][0] is not None:
            state, action = self.meta[state]
            action_list.append(action)

        action_list.reverse()
        return action_list
