import json
from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        a = 37.5665
        for i in range(1000):
            await self.send(json.dumps({'message' : a}))
            await sleep(1)
            a = a*1.000001
            print('debug')