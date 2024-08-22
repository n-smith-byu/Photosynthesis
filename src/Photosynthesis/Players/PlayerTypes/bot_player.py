from ..player import Player
import numpy as np


class AIPlayer(Player):
    def __init__(self, player_num):
        super(AIPlayer, self).__init__(player_num, is_bot=True)

    def choose_move(self, possible_actions):
        # TODO: Make Automatic
        # for now just pick a random move
        return possible_actions[np.random.choice(len(possible_actions))]