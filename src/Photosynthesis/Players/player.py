from abc import ABC, abstractmethod
from Store import *


class Player(ABC):

    def __init__(self, player_num, is_bot, name=None):
        self.name = name if name is not None else f"Player{player_num}"
        self.player_num = player_num
        self.__is_bot = is_bot

        self.__inventory = {0:2,1:4,2:1,3:0}
        self.__store = Store(self)
        self.__suns = 0
        self.__score = 0

    def is_bot(self):
        return self.__is_bot
    
    def get_suns(self):
        return self.__suns
    
    def get_score(self):
        return self.__score
    
    def get_inventory(self, size=None):
        if size is None:
            return self.__inventory.copy()
        
        else:
            return self.__inventory[size]


    @abstractmethod
    def choose_move(self, possible_actions):
        pass

