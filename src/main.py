from Server import GameServer
from Photosynthesis import PhotosynthesisGame
import asyncio

async def main():
    server = GameServer(PhotosynthesisGame)
    await server.run()

asyncio.run(main())