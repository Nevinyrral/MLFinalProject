class MCTEdge:
    def __init__(
        self, child_id, parent_id, start_tuple, end_tuple, opponent_move):
        self.times_visited = 0
        self.backtracking_accumulator = 0
        self.mean = 0
        self.probability = 0
