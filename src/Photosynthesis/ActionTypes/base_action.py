from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def perform(self, board):
        pass

