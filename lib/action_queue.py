from utils.constants import Configuration

class ActionQueue:
    def __init__(self, action_queue, opponent_player, piece_id, origin):
        self.opponent_player = opponent_player
        self.action_queue = action_queue
        self.repeating = False
        self.terminal = False
        self.end_position = action_queue[-1]
        self.start_position = origin
        self.__create_action_set()
        self.piece_id = piece_id
        self.calculate_score()

    def calculate_score(self):
        if self.repeating:
            self.distance_score = -1
            return
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
        self.piece_in_target_score(self.end_position)

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

    def piece_in_target_score(self, position):
        if not self.opponent_player:
            endgame_configuration = Configuration.ENDGAME["opponent"]
        else:
            endgame_configuration = Configuration.ENDGAME["player"]
        if position in endgame_configuration:
            self.distance_score += 10
    
    def build_states(self, player_state, opponent_state):
        new_player_state = player_state.copy()
        new_opponent_state = opponent_state.copy()
        if not self.opponent_player:
            # print("Progression:", self.action_queue)
            new_player_state[(self.start_position)] = player_state[(
                self.end_position)].copy()
            new_player_state[(self.end_position)] = player_state[(
                self.start_position)].copy()
            # print("Before:", player_state)
            # print("After:", new_player_state)
        else:
            # print("Progression:", self.action_queue)
            new_opponent_state[(self.start_position)] = opponent_state[(
                self.end_position)].copy()
            new_opponent_state[(self.end_position)] = opponent_state[(
                self.start_position)].copy()
            # print("Before:", opponent_state)
            # print("After:", new_opponent_state)
        return new_player_state, new_opponent_state
