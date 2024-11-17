from .Handlers import *
from BoardGame import BoardGame
from BoardGame.Exceptions import *
from BoardGame.GameSetup import WaitingRoom

from typing import Type

import urllib.parse
import websockets
import json

class GameServer:
    def __init__(self, GameClass: Type[BoardGame], host='localhost', port=8000):

        self.game_class = GameClass
        self.host = host
        self.port = port

        self.server = None
        self.current_handler = self.login_handler
        self.connected_clients = {}
        self.waiting_room = WaitingRoom(GameClass)
        self.game: GameClass

        self.not_found_error = "Invalid API Url"

    async def run(self):
        self.server = await websockets.serve(self.connection_handler, "localhost", 8000)
        print("Server starting...")
        await self.server.wait_closed()

    async def connection_handler(self, websocket, path):
        print(f"New connection from {path}")
        print(f'Passing Request to {self.current_handler.__name__}')
        await self.current_handler(websocket, path)

    async def login_handler(self, websocket, path):
        uri_path = self.__validate_and_split_url(path)
        try: 
            async for message in websocket:
                print(f"Received message: {message}")
                if uri_path[0] == 'register_player':
                    if len(uri_path) != 2:
                        websocket.send(self.not_found_error)
                        return
                    else:
                        player_key = uri_path[1]                                    # path should be '/register_player/{player_key}
                    try:
                        json_response = self.__add_login(player_key)
                        await websocket.send(json.dumps(json_response).encode('utf-8'))

                    except TooManyPlayersException:
                        await websocket.send("Too Many Players")

                # remove_player
                elif uri_path[0] == 'remove_player':
                    if len(uri_path) != 2:
                        self.send_error(404, self.not_found_error)                 # path should be '/remove_player/{player_key}'
                    else:
                        unique_key = uri_path[1]
                        try:
                            json_response = self.__remove_player(unique_key)
                            self.send_response(200, "Successfully Removed Player")
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps(json_response).encode('utf-8'))
                        except KeyError as ex:
                            self.send_error(400, f"No player associated with {unique_key}")

                # add or remove bots
                elif uri_path[0] == 'add_bot' or uri_path[0] == 'remove_bot' :          
                    pass

                await websocket.send(f"Echo: {message}")

        except websockets.exceptions.ConnectionClosedOK:
            print(f"Connection closed for {path}")

    async def game_handler(self, websocket, path):
        pass
            
    def start_game(self):
        self.game = self.waiting_room.create_game()
        self.current_handler = self.game_handler

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
    
    def __add_login(self, websocket, player_name=None) -> dict:
        self.connected_clients.add(websocket)
        unique_key = self.waiting_room.add_player(player_name)
        message = "Successfully Added Player\n." + \
                 f"{self.waiting_room.total_num_players()} players logged in. " + \
                 f"{self.waiting_room.num_human_players()} humans. " + \
                 f"{self.waiting_room.num_bots()} bots."

        return {
            'message': message,
            'player_name': player_name,
            'player_key': unique_key
        } 
    
    def __remove_player(self, websocket, unique_key) -> dict:
        player = self.waiting_room.remove_player(unique_key)

        return {
            'message': "Successfully Removed Player",
            'player_name': player.player_name,
            'player_key': unique_key,
        }
    