import numpy as np

class GameBoard:
    def __init__(self, num_players):
        self.tree_board = GameBoard.get_empty_board()
        self.player_board = GameBoard.get_empty_board()
        self.trees = {}

        


    def apply_action(action):
        pass

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