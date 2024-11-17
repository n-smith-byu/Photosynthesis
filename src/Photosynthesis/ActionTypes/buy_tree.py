from .base_action import Action

class BuyTree(Action):
    def __init__(self, player_num, size):
        super(BuyTree, self).__init__(player_num)
        self.__size = size

    @property
    def size(self):
        return self.__size