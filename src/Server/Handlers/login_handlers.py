from BoardGame.GameSetup import WaitingRoom
from BoardGame.Exceptions import *
from BoardGame.Players import HumanPlayer
from .game_handlers import GameHandler

from http.server import BaseHTTPRequestHandler
import urllib.parse
import json

class LoginHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        super(LoginHandler, self).__init__(request, client_address, server)
        self.not_found_error = "Invalid API Url"

    def do_POST(self):
        print(f'POST Request Received at {self.path}')
        
        # verifying path
        url_path, query = self.__validate_and_split_url(self.path)
        if not url_path:
            self.send_error(404, self.not_found_error)
            return
        url_path = url_path[1:]                         # remove leading empty string

        # login
        if url_path[0] == 'register_player':

            if len(url_path) != 2:
                self.send_error(404, self.not_found_error)
                return
            else:
                player_key = url_path[1]                                    # path should be '/register_player/{player_key}
            try:
                json_response = self.__add_login(player_key)
                self.send_response(201, "Successfully Logged In")
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(json_response).encode('utf-8'))

            except TooManyPlayersException as ex:
                self.send_error(409, "Too Many Players")

        # remove_player
        elif url_path[0] == 'remove_player':
            if len(url_path) != 2:
                self.send_error(404, self.not_found_error)                 # path should be '/remove_player/{player_key}'
            else:
                unique_key = url_path[1]
                try:
                    json_response = self.__remove_player(unique_key)
                    self.send_response(200, "Successfully Removed Player")
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(json_response).encode('utf-8'))
                except KeyError as ex:
                    self.send_error(400, f"No player associated with {unique_key}")

        # add or remove bots
        elif url_path[0] == 'add_bot' or url_path[0] == 'remove_bot' :          
            if len(url_path) > 1:                                      # path should be '/add_bot' or '/remove_bot'
                self.send_error(404, self.not_found_error) 
            else:
                action: function = self.__add_bot if url_path[0] == 'add_bot' else self.__remove_bot
                try:
                    json_response = action()
                    if json_response['success']:
                        status_code = 200
                    else:
                        status_code = 400

                    self.send_response(status_code, json_response['message'])
                    self.end_headers()

                except KeyError as ex:
                    self.send_error(404, f"No player associated with {unique_key}")
        
        # start the game
        elif url_path[0] == 'start':
            if len(url_path) > 1:
                self.send_error(404, self.not_found_error)
                return
            try:
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length).decode('utf-8')
                game_parameters = json.loads(body)
                response_json = self.__start_game(**game_parameters)
                
            except Exception as ex:
                self.send_error(500, "Unknown Error")                                       # FIXME: make this actually correct
                raise ex
            
            self.send_response(200, f"Game Starting with {self.server.num_humans} players " +
                                    f"and {self.server.num_bots} bots")
            self.end_headers()

        else:
            self.send_error(404, self.not_found_error)


    def do_GET(self):
        # verifying path
        url_path: list[str] = self.__validate_and_split_url(self.path)
        if not url_path:
            self.send_error(404, self.not_found_error)
            return
        url_path = url_path[1:]                         # remove leading empty string

        if url_path[0] == 'players':
            if len(url_path) > 1:                                      # path should be '/players'
                self.send_error(404, self.not_found_error) 
            json_response = self.__get_players()
            self.send_response(200, "Successfully Retrieved Players")
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(json_response).encode('utf-8'))

        else:
            self.send_error(404, self.not_found_error)




    ### -- Helpers --

    def __add_login(self, player_name=None) -> dict:
        waiting_room: WaitingRoom = self.server.waiting_room
        unique_key = waiting_room.add_player(player_name)
        message = "Successfully Added Player\n." + \
                 f"{waiting_room.total_num_players()} players logged in. " + \
                 f"{waiting_room.num_human_players()} humans. " + \
                 f"{waiting_room.num_bots()} bots."

        return {
            'message': message,
            'player_name': player_name,
            'player_key': unique_key
        } 
    
    def __remove_player(self, unique_key) -> dict:
        player: HumanPlayer = self.server.waiting_room.remove_player(unique_key)

        return {
            'message': "Successfully Removed Player",
            'player_name': player.player_name,
            'player_key': unique_key,
        }
    
    def __add_bot(self) -> dict:
        waiting_room: WaitingRoom = self.server.waiting_room
        if waiting_room.add_bot():
            return {
                'message': "Successfully Added Bot",
                'success': True
            }
        else:
            return {
                'message': "Could Not Add Bot. Too many players are in the game.",
                'success': False
            }

    def __remove_bot(self) -> dict:
        waiting_room: WaitingRoom = self.server.waiting_room
        if waiting_room.remove_bot():
            return {
                'message': "Successfully Removed Bot",
                'success': True
            }
        else:
            return {
                'message': "Could Not Remove Bot. No bots have been added to the game.",
                'success': False
            }
        
    def __get_players(self):
        waiting_room: WaitingRoom = self.server.waiting_room
        return waiting_room.get_player_list()


    def __start_game(self, **game_parameters):
        waiting_room: WaitingRoom = self.server.waiting_room
        self.server.game = waiting_room.create_game(**game_parameters)

        self.server.RequestHandlerClass = GameHandler           # change to the game request handler
    
    def __validate_and_split_url(self, url:str):
        parsed_url = urllib.parse.urlparse(url)
        url_path = parsed_url.path
        url_query = parsed_url.query

        if url_path[0] == '/':
            parsed_url_path = url_path.split(sep='/')[1:]
        else:
            parsed_url_path = []

        parsed_url_query = urllib.parse.parse_qs(url_path)

        return parsed_url_path, parsed_url_query



