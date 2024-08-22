class Tree:
    class Position:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def __init__(self, size:int, player_num:int, pos:Position=None):
        self.__size = size
        self.__pos = pos
        self.__player_num = player_num
    
    def __hash__(self):
        return hash((*self.position(), self.__size, self.__player_num))
    
    def size(self):
        return self.__size
    
    def position(self):
        return self.__pos.x, self.__pos.y
    
    def player(self):
        return self.__player_num