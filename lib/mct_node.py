import numpy as np
import uuid as UUID
from collections import deque
from .action_queue import ActionQueue
from utils.constants import Configuration
from utils.helpers import Helpers

class MCTNode:
    def __init__(self, player_state, opponent_state, mct,
        opponent_playing = False, parent = None):
        self.id = UUID.uuid4
        self.parent = parent
        self.children = []
        self.player_state = player_state.copy()
        self.opponent_state = opponent_state.copy()
        self.actions = []
        self.__build_players_tables(player_state, opponent_state)
        self.opponent_playing = opponent_playing

    def search(self):
        for key, value in self.player_id_table.items():
            self.__simulate(key, value)
        print(f'{len(self.actions)} actions simulated...')
        print("Score  Progression")
        for action in self.actions:
            action.configure_positions(self.player_id_table[action.piece_id])
            action.calculate_score()
        import ipdb; ipdb.set_trace()
        
    def __build_players_tables(self, player_state, opponent_state):
        print(f'Building players lookup tables for node {self.id}...')
        self.player_id_table = {}
        self.player_position_table = {}
        self.opponent_id_table = {}
        self.opponent_position_table = {}
        for index, value in np.ndenumerate(player_state):
            if value != 0:
                self.player_id_table[value] = index
                self.player_position_table[index] = value
        for index, value in np.ndenumerate(opponent_state):
            if value != 0:
                self.opponent_id_table[value] = index
                self.opponent_position_table[index] = value
        print("Build complete!")

    def __simulate(self, key, position, action_queue = list()):
        # *********************************************************************
        # We must take into account the following rules of engagement:
        #
        # 1. Check if a movement is inside matrix bounds
        # 2. Check if an adjacent space on the allowed configurations is free:
        #   a. If the space is free, a jump can be made
        #   b. If not, check if the adjacent space parallel to the direction of 
        #      the space we were originally checking is free and in bounds,
        #      if so, a jump can be made
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
        row, col = position
        rows, cols = self.player_state.shape
        # Horizontal validation
        for move_key in Configuration.VALID_MOVES:
            move = Configuration.VALID_MOVES[move_key]
            short_cell, long_cell = Helpers.get_cells(
                row, col, rows, cols, move
            )
            short_value = (
                self.player_state[short_cell]
            ) if short_cell else None
            long_value = (
                self.player_state[long_cell]
            ) if long_cell else None
            if short_value == 0:
                aux_action_queue = action_queue.copy()
                aux_action_queue.append(short_cell)
                action_queue_object = ActionQueue(aux_action_queue, 
                    self.opponent_playing, key)
                if not action_queue_object.repeating: # Pruning
                    print(f'{key} {move_key} {position} - > {short_cell} Short')
                    print(f'Progression: {aux_action_queue}')
                    print(self.player_state)
                    self.actions.append(action_queue_object)

            elif short_value and short_value != 0 and long_value == 0:
                aux_action_queue = action_queue.copy()
                aux_action_queue.append(long_cell)
                action_queue_object = ActionQueue(aux_action_queue,
                    self.opponent_playing, key)
                if not action_queue_object.repeating: # Pruning
                    print(f'{key} {move_key} {position} - > {long_cell} Long')
                    print(f'Progression: {aux_action_queue}')
                    print(self.player_state)
                    self.actions.append(action_queue_object)
                    self.__simulate(key, long_cell, aux_action_queue)
                
                    
        
        

