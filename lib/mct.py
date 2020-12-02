from .mct_node import MCTNode
from utils.helpers import Helpers
import numpy as np

EXPLORATION_LEVEL = 3.5

class MCT:
    def __init__(self, player_initial_state, opponent_initial_state):
        self.__build_players_tables(
            player_initial_state, opponent_initial_state)
        self.player_initial_state = player_initial_state.copy()
        self.opponent_initial_state = opponent_initial_state.copy()
        self.player_current_state = player_initial_state.copy()
        self.opponent_current_state = opponent_initial_state.copy()
        self.root = MCTNode(self.player_current_state, 
            self.opponent_current_state)
        self.nodes = {}
        self.edges = {}
        self.root.search()
    
    def __build_players_tables(self, player_state, opponent_state):
        print("Building global players lookup tables...")
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