from .base_action import Action
from src.Photosynthesis.GameBoard.Trees import Tree

class GrowTree(Action):
    def __init__(self, player_num, tree:Tree):
        super(GrowTree, self).__init__(player_num)
        if tree.size >= 3:
            raise ValueError('Tree of size 3 cannot be grown. Please use HarvestTree action instead.')
        
        self.__tree = tree

    @property
    def tree(self):
        return self.__tree
