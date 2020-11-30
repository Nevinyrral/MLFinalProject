from MCTNode import MCTNode
import numpy as np

EXPLORATION_LEVEL = 3.5

class MCT:
    def __init__(self, player_initial_state, opponent_initial_state):
        self.root = MCTNode(player_initial_state, opponent_initial_state)
        self.__build_player_tables(player_initial_state)
        self.__build_opponent_tables(opponent_initial_state)
        self.nodes = {}
        self.edges = {}
        self.root.expand()
    
    def __build_player_tables(self, state):
        print("Building global player lookup tables...")
        self.player_id_table = {}
        self.player_position_table = {}
        for index, value in np.ndenumerate(state):
            self.player_id_table[value] = index
            self.player_position_table[index] = value
        print("Build complete!")

    def __build_opponent_tables(self, state):
        print("Building global opponent lookup tables...")
        self.opponent_id_table = {}
        self.opponent_position_table = {}
        for index, value in np.ndenumerate(state):
            self.opponent_id_table[value] = index
            self.opponent_position_table[index] = value
        print("Build complete!")