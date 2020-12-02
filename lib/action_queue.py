class ActionQueue:
    def __init__(self, action_queue, opponent_player, piece_id):
        self.opponent_player = opponent_player
        self.action_queue = action_queue
        self.repeating = False
        self.end_position = (0, 0)
        self.start_position = (0, 0)
        self.__create_action_set()
        self.piece_id = piece_id

    def calculate_score(self):
        if self.opponent_player:
            self.distance_score = (
                self.end_position[0] - self.end_position[1]
            ) - (
                self.start_position[0] - self.start_position[1]
            )  
        else:
            self.distance_score = (
                self.start_position[0] - self.start_position[1]
            ) - (
                self.end_position[0] - self.end_position[1]
            )
    
    def configure_positions(self, start_position):
        self.start_position = start_position
        self.end_position = self.action_queue[-1]

    def __create_action_set(self):
        aux_queue = self.action_queue.copy()
        self.action_set = set()
        while aux_queue:
            item = aux_queue.pop()
            if not item in self.action_set:
                self.action_set.add(item)
            else:
                self.repeating = True
                break