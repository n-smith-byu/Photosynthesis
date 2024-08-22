from Server import GameServer

def main():
    server = GameServer(num_humans=2)
    server.run()


main()