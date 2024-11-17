from .base_action import Action

class PassTurn(Action):
    def __init__(self, player_num):
        super(PassTurn, self).__init__(player_num)