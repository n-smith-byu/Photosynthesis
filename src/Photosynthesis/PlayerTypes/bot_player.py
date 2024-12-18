from src.BoardGame.Players import AIPlayer
from src.Photosynthesis.GameBoard import BoardSummary
import numpy as np

class PhotosynthesisAIPlayer(AIPlayer):
    def __init__(self, player_num=None):
        super(PhotosynthesisAIPlayer, self).__init__(player_num)

    def choose_move(self, state:BoardSummary):
        # TODO: Make Automatic
        # for now just pick a random move
        return np.random.choice(len(state.available_actions))