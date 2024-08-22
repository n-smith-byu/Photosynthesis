import numpy as np
from collections import defaultdict
from Photosynthesis.Players import Player

class PlayerStore:
    def __init__(self, player_num):
        self.__player_num = player_num
        self.__capacities = {0:4, 1:5, 2:3, 3:2}
        self.__inventory = {0:4, 1:4, 2:3, 3:2}

        # initialize costs
        # self.__costs[i][n] is the cost if buying a tree of size i when n are available in the store
        self.__costs = {0:[np.inf, 2, 2, 1, 1],
                        1:[np.inf, 3, 3, 2, 2],
                        2:[np.inf, 4, 3, 3],
                        3:[np.inf, 5, 4]}
        
    # Public Functions
    def get_num_available(self, size):
        return self.__inventory[size]
    
    def get_cost(self, size):
        num_available = self.__inventory[size]
        return self.__costs[size][num_available]
    
    def buy_tree(self, size):
        if self.__inventory[size] == 0:
            return False
        
        self.__inventory[size] -= 1

    def player_num(self):
        return self.__player_num


