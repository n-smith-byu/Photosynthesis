from .base_action import Action
from ..Trees import Tree

class PlantSeed(Action):
    def __init__(self, player, position: Tree.Position):
        self.__player = player
        self.__position = position

    def perform(self, board):
        board.add_tree