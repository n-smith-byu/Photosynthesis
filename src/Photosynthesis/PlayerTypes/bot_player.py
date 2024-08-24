from BoardGame.Players import AIPlayer
import numpy as np


class PhotosynthesisAIPlayer(AIPlayer):
    def __init__(self, player_num=None):
        super(PhotosynthesisAIPlayer, self).__init__(player_num)

    def choose_move(self, possible_actions):
        # TODO: Make Automatic
        # for now just pick a random move
        return possible_actions[np.random.choice(len(possible_actions))]