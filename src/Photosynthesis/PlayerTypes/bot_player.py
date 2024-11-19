from src.BoardGame.Players import AIPlayer
import numpy as np

class PhotosynthesisAIPlayer(AIPlayer):
    def __init__(self, player_num=None):
        super(PhotosynthesisAIPlayer, self).__init__(player_num)

    def choose_move(self, possible_actions:list, num_suns:int):
        # TODO: Make Automatic
        # for now just pick a random move
        return np.random.choice(len(possible_actions))