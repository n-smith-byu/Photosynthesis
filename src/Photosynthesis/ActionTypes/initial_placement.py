from .base_action import Action

class InitialPlacement(Action):
    def __init__(self, player_num, position:tuple[int]):
        super(InitialPlacement, self).__init__(player_num)

        self.__position = position
    
    @property
    def position(self):
        return self.__position