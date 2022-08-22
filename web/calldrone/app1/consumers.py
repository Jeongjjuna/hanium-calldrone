import json
from collections import deque
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer


class WSConsumer(AsyncWebsocketConsumer):
    """외부 드론으로부터 들어오는 위치정보 데이터를 담고있는 Queue자료구조"""
    data_from_drone = deque([37.5665])
    print("새로운 소켓 생성")

    async def connect(self):
        await self.accept()
        while True:
            if self.data_from_drone:
                await self.send(json.dumps({'message' : self.data_from_drone.popleft()}))
                await sleep(2)

                print(self.data_from_drone)