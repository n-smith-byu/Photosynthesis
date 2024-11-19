from src.BoardGame.Players import HumanPlayer

class PhotosynthesisHumanPlayer(HumanPlayer):
    def __init__(self, player_name=None):
        super(PhotosynthesisHumanPlayer, self).__init__(player_name=player_name)

    def choose_move(self, possible_actions:list, num_suns:int):
        move_chosen = False
        possible_moves_str = [{str(action)} for action in possible_actions]
        while not move_chosen:
            print('Please Choose Move From Available Options: ')
            print('Possible moves:')
            for i, action in enumerate(possible_moves_str):
                print(f'[{i}]: {action}')
            print(f'Num Suns: {num_suns}')
            choice = input('Input Choice:')
            if not choice.isdigit() or int(choice) >= len(possible_actions):
                print('Invalid Choice')
                continue

            return int(choice)