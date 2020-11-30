class ActionQueue:
    def __init__(self, start_position, end_position, action_queue, 
        opponent_player):
        self.distance_score = self.__calculate_score(
            start_position, end_position
        )
        self.action_queue = action_queue
        self.__create_action_set()
        self.opponent_player = opponent_player
        self.repeating = False

    def __calculate_score(self, start_position, end_position):
        # Calculate forward distance
        if self.opponent_player:
            return (
                end_position[0] - end_position[1]
            ) - (
                start_position[0] - start_position[1]
            )  
        else:
            return (
                start_position[0] - start_position[1]
            ) - (
                end_position[0] - end_position[1]
            )

    def __create_action_set(self):
        aux_queue = self.action_queue
        self.action_set = set()
        while not aux_queue:
            item = aux_queue.popleft()
            if not item in self.action_set:
                self.action_set.add(item)
            else:
                self.repeating = True
                break