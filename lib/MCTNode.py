from numpy import np
import uuid as UUID
from collections import deque
from ActionQueue import ActionQueue

class MCTNode:
    def __init__(self, player_state, opponent_state, 
        opponent_playing = False, parent_id = None):
        self.id = UUID.uuid4
        self.parent_id = parent_id
        self.children = []
        self.player_state = player_state
        self.opponent_state = opponent_state
        self.actions = []
        self.__build_player_tables(player_state)
        self.__build_opponent_tables(opponent_state)
        self.opponent_playing = opponent_playing

    def expand(self):
        for key, value in self.player_id_table.items():
            self.__process_possible_moves(key, value)
        
    def __build_player_tables(self, state):
        print(f'Building player lookup tables for node {self.id}...')
        self.player_id_table = {}
        self.player_position_table = {}
        for index, value in np.ndenumerate(state):
            self.player_id_table[value] = index
            self.player_position_table[index] = value
        print("Build complete!")

    def __build_opponent_tables(self, state):
        print(f'Building opponent lookup tables for node {self.id}...')
        self.opponent_id_table = {}
        self.opponent_position_table = {}
        for index, value in np.ndenumerate(state):
            self.opponent_id_table[value] = index
            self.opponent_position_table[index] = value
        print("Build complete!")
    
    def __process_possible_moves(self, key, position, action_queue = deque()):
        row, col = position
        # *********************************************************************
        # We must take into account the following validation rules:
        #
        # 1. Check if a movement is inside matrix bounds
        # 2. Check if an adjacent space on the allowed configurations is free:
        #   a. If the space is free, a jump can be made
        #   b. If not, check if the adjacent space parallel to the direction of 
        #      the space we were originally checking is free and in bounds,
        #      if so, a jump can be done
        #
        #   Allowed configurations:
        #  
        #    0         0
        #      **      |
        #         1    1                       0    0
        #           ** |                         ** |
        #    0 -- 1 -- 1 -- 1 -- 0     AND     0 -- 1 -- 0      
        #              | **                         | **
        #              1    1                       0    0
        #              |      **
        #              0         0
        #
        # *********************************************************************
        # TODO Refactor, could be more compact
        rows, cols = self.player_state.shape
        # Calculate bounds
        row_lower, row_upper = (row - 1, row + 1)
        col_lower, col_upper = (col - 1, col + 1)
        # Horizontal validation
        if row_upper < rows:
            aux_action_queue = action_queue
            if self.player_state[row_upper][col] == 0:
                aux_action_queue.append((row_upper, col))
                action_queue_object = ActionQueue(
                    (row, col), (row_upper, col), aux_action_queue,
                    self.opponent_playing
                )
                self.actions.append(action_queue_object)
            elif (row_upper + 1 < rows and 
                self.player_state[row_upper + 1][col] == 0):
                aux_action_queue.append((row_upper + 1, col))
                action_queue_object = ActionQueue(
                    (row, col), (row_upper + 1, col), aux_action_queue,
                    self.opponent_playing
                )
                self.actions.append(action_queue_object)
                self.__process_possible_moves(key, (row_upper + 1, col),
                    aux_action_queue
                )
        if row_lower > 0:
            aux_action_queue = action_queue
            if self.player_state[row_lower][col] == 0:
                aux_action_queue.append((row_lower, col))
                action_queue_object = ActionQueue(
                    (row, col), (row_lower, col), aux_action_queue,
                    self.opponent_playing
                )
                self.actions.append(action_queue_object)
            elif (row_lower - 1 > 0 and 
                self.player_state[row_lower - 1][col] == 0):
                aux_action_queue.append((row_lower - 1, col))
                action_queue_object = ActionQueue(
                    (row, col), (row_lower - 1, col), aux_action_queue,
                    self.opponent_playing
                )
                self.actions.append(action_queue_object)
                self.__process_possible_moves(key, (row_lower + 1, col),
                    aux_action_queue
                )
        # Vertical validation
        if col_upper < cols:
            aux_action_queue = action_queue
            if self.player_state[row][col_upper] == 0:
                aux_action_queue.append((row, col_upper))
                action_queue_object = ActionQueue(
                    (row, col), (row, col_upper), aux_action_queue,
                    self.opponent_playing
                )
                self.actions.append(action_queue_object)
            elif (col_upper + 1 < col and 
                self.player_state[row][col_upper + 1] == 0):
                aux_action_queue.append((row, col_upper + 1))
                action_queue_object = ActionQueue(
                    (row, col), (row, col_upper + 1), aux_action_queue,
                    self.opponent_playing
                )
                self.actions.append(action_queue_object)
                self.__process_possible_moves(key, (row, col_upper + 1),
                    aux_action_queue
                )
        if col_lower > 0:
            aux_action_queue = action_queue
            if self.player_state[row][col_lower] == 0:
                aux_action_queue.append((row, col_lower))
                action_queue_object = ActionQueue(
                    (row, col), (row, col_lower), aux_action_queue,
                    self.opponent_playing
                )
                self.actions.append(action_queue_object)
            elif (col_lower - 1 > 0 and 
                self.player_state[row][col_lower - 1] == 0):
                aux_action_queue.append((row, col_lower - 1))
                action_queue_object = ActionQueue(
                    (row, col), (row, col_lower - 1), aux_action_queue,
                    self.opponent_playing
                )
                self.actions.append(action_queue_object)
                self.__process_possible_moves(key, (row, col_lower - 1),
                    aux_action_queue
                )
        # Diagonal validation
        if col_lower > 0 and row_upper < rows:
            aux_action_queue = action_queue
            if self.player_state[row_upper][col_lower] == 0:
                aux_action_queue.append((row_upper, col_lower))
                action_queue_object = ActionQueue(
                    (row, col), (row_upper, col_lower), aux_action_queue,
                    self.opponent_playing
                )
                self.actions.append(action_queue_object)
            elif ((col_lower - 1 > 0 and row_upper + 1 < rows) and 
                self.player_state[row_upper + 1][col_lower - 1] == 0):
                aux_action_queue.append((row_upper + 1, col_lower - 1))
                action_queue_object = ActionQueue(
                    (row, col), (row_upper + 1, col_lower - 1), 
                    aux_action_queue, self.opponent_playing
                )
                self.actions.append(action_queue_object)
                self.__process_possible_moves(
                    key, (row_upper + 1, col_lower - 1), aux_action_queue
                )
        if col_upper < cols and row_lower > 0:
            aux_action_queue = action_queue
            if self.player_state[row_lower][col_upper] == 0:
                aux_action_queue.append((row_lower, col_upper))
                action_queue_object = ActionQueue(
                    (row, col), (row_lower, col_upper), aux_action_queue,
                    self.opponent_playing
                )
                self.actions.append(action_queue_object)
            elif ((col_upper + 1 < cols and row_lower - 1 > 0) and 
                self.player_state[row_lower - 1][col_upper + 1] == 0):
                aux_action_queue.append((row_lower - 1, col_upper + 1))
                action_queue_object = ActionQueue(
                    (row, col), (row_lower - 1, col_upper + 1), 
                    aux_action_queue, self.opponent_playing
                )
                self.actions.append(action_queue_object)
                self.__process_possible_moves(
                    key, (row_lower - 1, col_upper + 1), aux_action_queue
                )


