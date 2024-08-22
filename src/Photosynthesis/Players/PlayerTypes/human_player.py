from ..player import Player

class HumanPlayer(Player):
    def __init__(self, player_num):
        super(HumanPlayer, self).__init__(player_num, is_bot=False)

    def choose_move(self, possible_actions):
        return super().choose_move(possible_actions)