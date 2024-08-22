from http.server import BaseHTTPRequestHandler
from Photosynthesis import GameManager
from .game_handlers import GameHandler
from Photosynthesis import PhotosynthesisGame

import uuid
import json

class LoginHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        print('POST Request Received')
        if self.server.RequestHandlerClass == GameHandler:      # if game already started
            self.send_error(409, "Game Already Started")
        elif self.path.startswith('/login'):
            json_response = self.__add_login()
            if json_response['player_key']:
                self.send_response(201, "Successfully Logged In")
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(json_response).encode('utf-8'))
            else:
                self.send_error(409, "Too Many Players")
        elif self.path.startswith('/start'):
            try:
                self.server.RequestHandlerClass = GameHandler
                num_logged_players = len(self.server.logged_players)
                if num_logged_players < self.server.num_humans:
                    diff = self.server.num_humans - num_logged_players
                    self.server.num_bots += diff
                    self.server.num_humans -= diff

                self.server.game = PhotosynthesisGame(self.server.num_humans, 
                                                    self.server.num_bots,
                                                    self.server.extra_round)
                
            except Exception as ex:
                self.send_error(500, "Unknown Error")
                raise ex
            
            self.send_response(200, f"Game Starting with {self.server.num_humans} players " +
                                    f"and {self.server.num_bots} bots")
            self.end_headers()
        else:
            self.send_error(404, "API not found")

    def __add_login(self) -> str:
        server_instance = self.server
        unique_key = str(uuid.uuid4())  
        if len(server_instance.logged_players) >= 4:
            return False
        else:
            server_instance.logged_players.append(unique_key)
            num_logged_in = len(server_instance.logged_players)
            num = 'All' if num_logged_in  == server_instance.num_humans \
                        else f'{num_logged_in}/{server_instance.num_humans}'
            
            message = f'{num} players logged in.'

            return {
                'player_key': unique_key,
                'message': message
            } 


