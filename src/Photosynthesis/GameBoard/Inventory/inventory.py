

class PlayerInventory:
    def __init__(self, player_num):
        self.__player_num = player_num
        self.__trees: dict
        self.__suns: int
        self.__points: int

        self.reset()

    def reset(self):
        self.__trees = {0:2,1:4,2:1,3:0}
        self.__suns = 0
        self.__points = 0

    def add_tree(self, size):
        if size in [0,1,2,3]:
            self.__trees[size] += 1
            return True
        else:
            return False

    def remove_tree(self, size):
        if size in [0,1,2,3] and self.__trees[size] > 0:
            self.__trees[size] -= 1
            return True
        else:
            return False
        
    def subtract_suns(self, number):
        if number >= 0 and self.__suns >= number:
            self.__suns -= number
            return True 
        else:
            return False
        
    def add_suns(self, number):
        if number >= 0:
            self.__suns = min(self.__suns + number, 20)     # suns cap out at 20
            return True
        else:
            return False
        
    def add_points(self, number):
        if number >= 0:
            self.__points += number
            return True
        else:
            return False
        
    def player_num(self):
        return self.__player_num
