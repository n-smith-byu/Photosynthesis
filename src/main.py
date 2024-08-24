from Server import GameServer
from Photosynthesis import PhotosynthesisGame

def main():
    server = GameServer(PhotosynthesisGame)
    server.run()


main()