class MCTEdge:
    def __init__(
        self, parent, child, start_tuple, end_tuple, probability, actions
        ):
        self.times_visited = 0
        self.backtracking_accumulator = 0
        self.mean = 0
        self.parent = parent
        self.child = child
        self.probability = probability
        self.actions = actions
