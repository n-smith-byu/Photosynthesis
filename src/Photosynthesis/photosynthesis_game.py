from typing import Type
from BoardGame import BoardGame
from BoardGame.Players import AIPlayer, HumanPlayer, Player
from .PlayerTypes import *
from .GameBoard import *

class PhotosynthesisGame(BoardGame):
    @classmethod
    def get_max_num_players(cls) -> int:
        return 4
    
    @classmethod
    def get_min_num_players(cls) -> int:
        return 2
    
    @classmethod
    def get_ai_player_class(cls) -> type[AIPlayer]:
        return AIPlayer
    
    @classmethod
    def get_human_player_class(cls) -> type[HumanPlayer]:
        return HumanPlayer

    SUN_POSITIONS = 6

    def __init__(self, players: list[Player], extra_round: bool=False):
        self.__players = players
        self,__num_players = len(players)
        self.__initialize_board(self.__num_players)
        
        self.__num_rounds = 3 + extra_round

        self.__current_round = 0
        self.__sun_position = 0
        self.__first_player = 0

    def __initialize_players(self, num_humans, num_bots):

        self.num_players = num_humans + num_bots

        if num_humans < 0 or num_humans > 4 or \
                num_bots < 0 or num_bots > 4 or \
                self.num_players > 4 or self.num_players <= 1:
            raise ValueError("Invalid number of players. Must have at least two players and no more than 4.")
        
        player_classes = [HumanPlayer for i in range(num_humans)] + \
                         [AIPlayer for j in range(num_bots)]
        
        # initialize players
        self.__players = []
        for i in range(self.num_players):
            self.__players.append(player_classes[i](player_num=i))

    def __initialize_board(self, num_players):
        self.board = GameBoard(num_players)


    # Public Methods

    def run(self):
        for round in range(self.__num_rounds):
            self.__current_round = round

            for turn in range(PhotosynthesisGame.SUN_POSITIONS):
                for i in range(self.__num_players):
                    curr_player_num = (self.__first_player + i) % self.__num_players
                    curr_player:Player = self.__players[curr_player_num]

                    action = curr_player.choose_move(possible_actions=[1,2,3]) # TODO: Fix This
                    self.board.apply_action(action, curr_player_num)
            
            
            # pass the first player token
            self.__first_player = (self.__first_player + 1) % self.__num_players


    # Getters
    def get_num_players(self):
        return self.__num_players
    
    def get_num_bots(self):
        return self.__num_bots
    
    def get_num_humans(self):
        return self.__num_humans

    def get_num_rounds(self):
        return self.__num_rounds

    def get_current_round(self):
        return self.__current_round
    
    def get_first_player(self):
        player = self.__players[self.__first_player]
        return (player.player_num, player.name)
    
    def get_sun_pos(self):
        return self.__sun_position