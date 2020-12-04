from .mct_node import MCTNode
from utils.helpers import Helpers
from utils.constants import Configuration
from utils.constants import Agent
import numpy as np
import math

class MCT:
    def __init__(self, player_initial_state, opponent_initial_state, iterations):
        self.__build_players_tables(
            player_initial_state, opponent_initial_state)
        self.player_initial_state = player_initial_state.copy()
        self.opponent_initial_state = opponent_initial_state.copy()
        self.player_current_state = player_initial_state.copy()
        self.opponent_current_state = opponent_initial_state.copy()
        self.root = MCTNode(self.player_current_state, 
            self.opponent_current_state, 0)
        self.iterations = iterations
        self.root.initial_expansion()
        self.current_node = self.root
        self.wins = []
        self.loses = []
        self.current_best = None
        for iteration in range(0, self.iterations):
            if iteration % 1000 == 0:
                print(f'Current iteration: {iteration + 1}')
                print(f'Current node visits: {self.current_node.times_visited}')
                print(f'''Current node score: {
                    self.current_node.backtracking_accumulator}''')
            while True:
                if self.current_node.expanded():
                    rollout = False
                    minimize = False
                    for child in self.current_node.children.values():
                        if child.visited():
                            self.current_node.children[
                                child.id
                            ].calculate_selection_coefficient(
                                self.root.times_visited
                            )
                            # print("Mean: ", self.current_node.children[child.id].mean)
                            # print("UCB: ", self.current_node.children[child.id].upper_confidence_bound)
                            if self.current_node.children[child.id].mean < 0:
                                minimize = True
                        else:
                            # print(f'''Node {
                            #     child.id
                            # } has zero visits, executing rollout...''')
                            rollout = True
                            self.current_node.children[child.id].rollout()
                            self.current_node = self.root
                            break
                    if rollout:
                        break
                    if not minimize:
                        next_node = max(self.current_node.children.values(),
                            key = lambda item: (
                                item.upper_confidence_bound + item.mean
                            )
                        )
                    else:
                        next_node = min(self.current_node.children.values(),
                            key = lambda item: (
                                item.upper_confidence_bound + abs(item.mean)
                            )
                        )
                    self.current_node = self.current_node.children[next_node.id]
                    self.current_node.evaluate_endgame()
                    if self.current_node.winner:
                        current_winner = self.current_node.winner
                        if current_winner == Agent.PLAYER:
                            self.wins = self.current_node
                        else: 
                            self.loses = self.current_node
                    if not self.current_best:
                        self.current_best = next_node
                    elif self.current_best.depth < next_node.depth and (
                            self.current_best.upper_confidence_bound + 
                            self.current_best.mean
                        ) < (next_node.upper_confidence_bound + next_node.mean):
                        self.current_best = next_node

                else:
                    if not self.current_node.visited():
                        self.current_node.rollout()
                        # print(f'Rolling out node {self.current_node.id}, visits: {self.current_node.times_visited}')
                        self.current_node = self.root
                        break
                    else:
                        # print(f'Expanding {self.current_node.id}...')
                        self.current_node.expand()
                        children = self.current_node.children.values()
                        self.current_node = self.current_node.children[
                                list(children)[0].id
                            ]
                        self.current_node.rollout()
                        self.current_node = self.root
                        break
        
        print("Wins: ", len(self.wins))
        print("Loses: ", len(self.loses))           
    
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
                print(f'Player piece no. {value}: {index}')
        for index, value in np.ndenumerate(opponent_state):
            if value != 0:
                self.opponent_id_table[value] = index
                self.opponent_position_table[index] = value
                print(f'Opponent piece no. {value}: {index}')
        print("Build complete!")