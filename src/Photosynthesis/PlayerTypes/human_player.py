from BoardGame.Players import HumanPlayer

class PhotosynthesisHumanPlayer(HumanPlayer):
    def __init__(self, player_name=None):
        super(PhotosynthesisHumanPlayer, self).__init__(is_bot=False, name=player_name)

    def choose_move(self, possible_actions):
        return super().choose_move(possible_actions)