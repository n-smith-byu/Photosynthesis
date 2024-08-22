from .Inventory import PlayerInventory
from .Store import PlayerStore
from .Trees import Tree

from collections import defaultdict
import numpy as np

class GameBoard:
    @staticmethod
    def get_empty_board(zeros=False):
        F = np.inf
        board = [[-F, -F, -F, -1, -1, -1, -1],
                 [-F, -F, -1, -1, -1, -1, -1],
                 [-F, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -F],
                 [-1, -1, -1, -1, -1, -F, -F],
                 [-1, -1, -1, -1, -F, -F, -F]]
        
        if zeros:
            board += 1
        
        return board

    def __init__(self, num_players):
        self.tree_board = GameBoard.get_empty_board()
        self.player_board = GameBoard.get_empty_board()
        self.player_trees = defaultdict(set)      # dictionary of trees by player
        self.tree_positions = {}

    def apply_action(action):
        pass

