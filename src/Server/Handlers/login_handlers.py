from BoardGame.GameSetup import WaitingRoom
from BoardGame.Exceptions import *
from BoardGame.Players import HumanPlayer
from .game_handlers import GameHandler

from http.server import BaseHTTPRequestHandler
import json

class LoginHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        print('POST Request Received')  
        
        url_path: list[str] = self.validate_and_split_url(self.path)
        if not url_path:
            self.send_error(404, "Invalid API Url")
            return
        url_path = url_path[1:]                         # remove leading empty string

        if url_path[0] == 'login':
            if len(url_path) > 2:
                self.send_error(404, "Invalid API Url")
                return
            elif len(url_path) == 2:
                player_name = url_path[1]
            else:
                player_name = None

            try:
                json_response = self.__add_login()
                self.send_response(201, "Successfully Logged In")
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(json_response).encode('utf-8'))

            except TooManyPlayersException as ex:
                self.send_error(409, "Too Many Players")

        elif url_path[0] == 'remove_player':
            if len(url_path) != 2:
                self.send_error(404, "Invalid API Url")         # path should be /remove_player/{unique_key}
            else:
                unique_key = url_path[1]
                try:
                    self.__remove_player(unique_key)
                except KeyError as ex:
                    self.send_error(400, f"No player associated with {unique_key}")
        
        elif url_path[0] == 'start':
            if len(url_path) > 1:
                self.send_error(404, "Invalid API Url")
                return
            try:
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length).decode('utf-8')
                game_parameters = json.loads(body)
                response_json = self.__start_game(kwargs=game_parameters)
                
            except Exception as ex:
                self.send_error(500, "Unknown Error")
                raise ex
            
            self.send_response(200, f"Game Starting with {self.server.num_humans} players " +
                                    f"and {self.server.num_bots} bots")
            self.end_headers()

        else:
            self.send_error(404, "Invalid API Url")

    def __add_login(self, player_name) -> str:
        unique_key, player = self.server.waiting_room.add_player()
        message = "Successfully Added Player\n." + \
                 f"{self.server.waiting_room.num_players()} players logged in."

        return {
            'message': message,
            'player_name': player_name,
            'player_key': unique_key
        } 
    
    def __remove_player(self, unique_key):
        player: HumanPlayer = self.server.waiting_room.remove_player(unique_key)

        return {
            'message': "Successfully Removed Player",
            'player_name': player.name,
            'unique_key': unique_key,
        }
    
    def __start_game(self, **game_parameters):
        waiting_room: WaitingRoom = self.server.waiting_room
        self.server.game = waiting_room.create_game(**game_parameters)

        self.server.RequestHandlerClass = GameHandler           # change to the game request handler
    
    def validate_and_split_url(self, url):
        if url[0] != '/':               
            return []
        
        return url.split(sep='/')



