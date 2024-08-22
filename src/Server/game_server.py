from .Handlers import *
from Photosynthesis import PhotosynthesisGame

from http.server import HTTPServer
import requests
import threading
import time

class GameServer(HTTPServer):
    def __init__(self, host='localhost', port=8000, num_humans=1, num_bots=1, extra_round=False):
        super(GameServer, self).__init__((host, port), LoginHandler)

        self.host = host
        self.port = port

        self.num_humans = num_humans
        self.num_bots = num_bots
        self.extra_round = extra_round

        self.game: PhotosynthesisGame = None
        self.logged_players = []

    def run(self):
        print("Server starting...")
        thread = threading.Thread(target=self.serve_forever)
        thread.start()

        # if no human players, simply start the game
        if self.num_humans == 0:
            url = f'http://{self.host}:{self.port}/start'
            response = requests.post(url)
            print(response)

        # wait for keyboard interrupt, then cleanup other thread
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt as ex:
                self.shutdown()
                thread.join()
                raise ex

