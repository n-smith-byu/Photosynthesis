from .base_action import Action
from src.Photosynthesis.GameBoard.Trees import Tree

class HarvestTree(Action):
    def __init__(self, player_num, tree:Tree):
        super(HarvestTree, self).__init__(player_num)

        if player_num != tree.player:
            raise ValueError('Cannot harvest tree of another player')
    
        self.__tree = tree

    @property
    def tree(self):
        return self.__tree
