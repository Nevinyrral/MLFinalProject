import numpy as np
import uuid as UUID
from collections import deque
from .action_queue import ActionQueue
from .mct_edge import MCTEdge
from utils.constants import Configuration
from utils.constants import Agent
from utils.helpers import Helpers
import random
import math

class MCTNode:
    def __init__(self, player_state, opponent_state, piece_id, actions = [],
        opponent_playing = False, parent = None, probability = 0):
        self.id = UUID.uuid4()
        self.parent = parent
        self.children = {}
        self.player_state = player_state.copy()
        self.opponent_state = opponent_state.copy()
        self.simulations = []
        self.winner = None
        self.__build_players_tables(player_state, opponent_state)
        self.opponent_playing = opponent_playing
        self.times_visited = 0
        self.backtracking_accumulator = 0
        self.mean = 0
        self.upper_confidence_bound = 0
        self.depth = 0 if not parent else parent.depth + 1
        self.probability = probability
        self.actions = actions
        self.piece_id = piece_id

    def initial_expansion(self):
        print("------------------ INITIAL EXPANSION ------------------")
        for key, value in self.player_id_table.items():
            self.simulate(key, value, value)
        actions_total_score = Helpers.actions_score(self.simulations)
        print(f'Node probable actions score: {actions_total_score}')
        print(f'{len(self.simulations)} actions simulated, building nodes...')
        for action in self.simulations:
            action_player_state, action_opponent_state = action.build_states(
                self.player_state, self.opponent_state)
            child = MCTNode(
                action_player_state, action_opponent_state, 
                action.piece_id, action.action_queue,
                not self.opponent_playing, self, Helpers.calculate_probability(
                    action.distance_score, actions_total_score, 
                    not self.opponent_playing
                )
            )
            self.children[child.id] = child
            # print(f'Node prior probability: {child.probability * 100}%')
        print("------------------ EXPANSION COMPLETE ------------------")    

    def rollout(self):
        if not self.opponent_playing:
            current_id_table = self.player_id_table
        else: 
            current_id_table = self.opponent_id_table
        for key, value in current_id_table.items():
            self.simulate(key, value, value)
        random_action = random.choice(self.simulations)
        return self.backpropagate(random_action.distance_score)
        
    def __build_players_tables(self, player_state, opponent_state):
        # print(f'Building players lookup tables for node {self.id}...')
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
        # print("Build complete!")

    def calculate_selection_coefficient(self, total_visits):
        self.upper_confidence_bound = Configuration.EXPLORATION_LEVEL * (
            self.probability * (
               math.sqrt(total_visits) / (self.times_visited + 1)
            )
        )
        self.mean = float(self.backtracking_accumulator) / float(
            self.times_visited
        )

    def simulate(self, key, original_position, start_position, 
        action_queue = list()):
        # *********************************************************************
        # We must take into account the following rules of engagement:
        #
        # 1. Check if a movement is inside the matrix bounds
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
        if not self.opponent_playing:
            current_player_state = self.player_state
            current_opponent_state = self.opponent_state
        else: 
            current_player_state = self.opponent_state
            current_opponent_state = self.player_state
        row, col = start_position
        rows, cols = current_player_state.shape
        # Horizontal validation
        for move_key in Configuration.VALID_MOVES:
            move = Configuration.VALID_MOVES[move_key]
            short_cell, long_cell = Helpers.get_cells(
                row, col, rows, cols, move
            )
            short_value = None
            long_value = None
            if short_cell is not None:
                if current_player_state[short_cell] != 0:
                    short_value = current_player_state[short_cell] 
                elif current_opponent_state[short_cell] != 0:
                    short_value = current_opponent_state
                else:
                    short_value = 0
            if long_cell is not None:
                if current_player_state[long_cell] != 0:
                    long_value = current_player_state[long_cell] 
                elif current_opponent_state[long_cell] != 0:
                    long_value = current_opponent_state[long_cell] 
                else:
                    long_value = 0
            if short_value and short_value == 0:
                aux_action_queue = action_queue.copy()
                aux_action_queue.append(short_cell)
                action_queue_object = ActionQueue(aux_action_queue, 
                    self.opponent_playing, key, original_position)
                if not action_queue_object.repeating: # Pruning
                    # print(f'''{key} {move_key} {start_position} - > {
                    #     short_cell} Short''')
                    # print(f'Progression: {aux_action_queue}')
                    # print(current_player_state + current_opponent_state)
                    self.simulations.append(action_queue_object)
            elif short_value and short_value != 0 and long_value == 0:
                aux_action_queue = action_queue.copy()
                aux_action_queue.append(long_cell)
                action_queue_object = ActionQueue(aux_action_queue,
                    self.opponent_playing, key, original_position)
                if not action_queue_object.repeating: # Pruning
                    # print(f'''{key} {move_key} {start_position} - > {
                    #     long_cell} Long''')
                    # print(f'Progression: {aux_action_queue}')
                    # print(current_player_state + current_opponent_state)
                    self.simulations.append(action_queue_object)
                    self.simulate(key, original_position, long_cell, 
                        aux_action_queue)
    
    def expanded(self):
        return bool(self.children)
    
    def visited(self):
        return self.times_visited > 0

    def backpropagate(self, rollout):
        self.backtracking_accumulator = rollout
        self.times_visited += 1
        current_node = self
        while True:
            if not current_node.parent:
                return current_node
            current_node.parent.times_visited += 1
            current_node.parent.backtracking_accumulator += (
                self.backtracking_accumulator
            )
            current_node = current_node.parent

    def expand(self):
        # print("------------------ EXPAND ------------------")
        actions_total_score = Helpers.actions_score(self.simulations)
        # print(f'Node probable actions score: {actions_total_score}')
        # print(f'{len(self.simulations)} actions simulated, building nodes...')
        for action in self.simulations:
            action_player_state, action_opponent_state = action.build_states(
                self.player_state, self.opponent_state)
            child = MCTNode(
                action_player_state, action_opponent_state, 
                action.piece_id, action.action_queue,
                not self.opponent_playing, self, Helpers.calculate_probability(
                    action.distance_score, actions_total_score, 
                    self.opponent_playing
                )
            )
            self.children[child.id] = child
        #     print(f'Node prior probability: {child.probability * 100}%')
        # print("------------------ EXPANSION COMPLETE ------------------")
    
    def evaluate_endgame(self):
        if not self.opponent_playing:
            current_pieces = set(self.player_id_table.items())
            endgame_configuration = Configuration.ENDGAME["player"]
            current_winner = Agent.PLAYER
        else:
            current_pieces = set(self.opponent_id_table.items())
            endgame_configuration = Configuration.ENDGAME["opponent"]
            current_winner = Agent.OPPONENT
        
        if current_pieces == endgame_configuration:
            print(f'''Found winning state for {
                current_winner.name
            }, prunning from search next states...''')
            self.winner = current_winner
        
                    
        
        

