from abc import ABC, abstractmethod

class Player(ABC):

    def __init__(self, player_num, is_bot, name=None):
        self.name = name if name is not None else f"Player{player_num}"
        self.player_num = player_num
        self.__is_bot = is_bot

    def is_bot(self):
        return self.__is_bot

    @abstractmethod
    def choose_move(self, possible_actions):
        pass

