from typing import Type
from . import PlayerTypes
from .GameBoard import *
from .ActionTypes import BuyTree, PlantSeed, GrowTree, HarvestTree, PassTurn
from src import BoardGame
import numpy as np

class PhotosynthesisGame(BoardGame.BoardGame):
    @classmethod
    def get_max_num_players(cls) -> int:
        return 4
    
    @classmethod
    def get_min_num_players(cls) -> int:
        return 2
    
    @classmethod
    def get_ai_player_class(cls) -> type[BoardGame.Players.AIPlayer]:
        return PlayerTypes.AIPlayer
    
    @classmethod
    def get_human_player_class(cls) -> type[BoardGame.Players.HumanPlayer]:
        return PlayerTypes.HumanPlayer

    SUN_POSITIONS = 6

    def __init__(self, players: list[BoardGame.Players.Player], 
                 extra_round: bool=False, print_board=False):
        super(PhotosynthesisGame, self).__init__(players)
        self.__num_players = len(players)
        self.__initialize_board(self.__num_players)
        
        self.__num_rounds = 3 + extra_round
        self.__current_round = -1
        self.__first_player_token = 0
        self.__curr_player = 0

    def __initialize_board(self, num_players):
        self.__board = GameBoard(num_players)


    # Public Methods

    def run(self):
        possible_first_actions = list(self.__board.get_possible_first_turn_spaces())
        # setting initial trees on board
        for i in range(2):
            for player_num in range(self.__num_players):
                while True:
                    player = self._BoardGame__players[player_num]
                    action_ind = player.choose_move(possible_first_actions.copy())
                    try:
                        position = possible_first_actions[action_ind]
                    except Exception as ex:
                        print('Invalid Action')
                    else:
                        self.__board.player_initial_tree_placement(player_num, position)
                        possible_first_actions.remove(position)
                        break

        # playing the game
        self.__board.rotate_sun()
        for round in range(self.__num_rounds):
            self.__current_round = round

            for sun_pos in range(PhotosynthesisGame.SUN_POSITIONS):
                self.__curr_player = self.__first_player_token
                for i in range(self.__num_players):
                    player:BoardGame.Players.Player = self._BoardGame__players[self.__curr_player]
                    possible_actions = list(self.__board.get_possible_actions(self.__curr_player))
                    while True:
                        action_ind= player.choose_move(possible_actions.copy())
                        try:
                            action = possible_actions[action_ind]
                        except Exception as ex:
                            print('Invalid Action')
                        else:
                            if isinstance(action, PassTurn):
                                break
                            else:
                                self.apply_action(action)
                                break
                    
                    self.__curr_player = (self.__curr_player + 1) % self.__num_players
                    
                self.__first_player_token = (self.__first_player_token + 1) % self.__num_players
                if not (round == self.__num_rounds and self.__board.get_sun_pos() == 5): 
                    self.__board.rotate_sun()
            
        scores = self.__board.get_player_scores()
        for player_num in range(self.__num_players):
            remaining_suns = self.__board.get_player_suns(player_num)
            scores[player_num] += remaining_suns // 3

        return tuple(scores)

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
        player = self._BoardGame__players[self.__first_player]
        return (player.player_num, player.player_name)
    
    def get_sun_pos(self):
        return self.__sun_position
    
    def apply_action(self, action):
        if isinstance(action, BuyTree):
            self.__board.player_buy_tree(action.player, action.size)
        elif isinstance(action, PlantSeed):
            self.__board.player_plant_seed(action.player, action.parent_tree, action.position)
        elif isinstance(action, GrowTree):
            self.__board.player_grow_tree(action.player, action.tree)
        elif isinstance(action, HarvestTree):
            self.__board.player_harvest_tree(action.player, action.tree)
        elif isinstance(action, PassTurn):
            pass