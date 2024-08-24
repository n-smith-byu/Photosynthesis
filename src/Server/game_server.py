from .Handlers import *
from BoardGame import BoardGame
from BoardGame.GameSetup import WaitingRoom
from Photosynthesis import PhotosynthesisGame

from http.server import HTTPServer
from typing import Type
import requests
import threading
import time

class GameServer(HTTPServer):
    def __init__(self, GameClass: Type[BoardGame], host='localhost', port=8000):
        super(GameServer, self).__init__((host, port), LoginHandler)

        self.game_class = GameClass
        self.host = host
        self.port = port

        self.waiting_room = WaitingRoom(GameClass)
        self.game: GameClass

    def run(self):
        print("Server starting...")
        thread = threading.Thread(target=self.serve_forever)
        thread.start()

        # wait for keyboard interrupt, then cleanup other thread
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt as ex:
                self.shutdown()
                thread.join()
                raise ex
            
    def start_game(self):
        self.game: PhotosynthesisGame = self.waiting_room.create_game()

