import json
from collections import deque
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer

# 장고 서버 실행시 WSConsumer class는 두 번 호출 된다
class WSConsumer(AsyncWebsocketConsumer):
    print("WSConsumer class호출")
    
    # 외부 드론으로부터 들어오는 위치정보 데이터를 담고있는 Queue자료구조
    data_from_drone = deque([37.5665])
    
    # 클라이언트 단에서 웹소켓 연결요청을 하면 connect함수가 실행 된다
    # 연결이 끊어지면 connect함수는 종료 된다
    async def connect(self):
        print('확인용')
        await self.accept()
        while True:
            if self.data_from_drone:
                await self.send(json.dumps({'message' : self.data_from_drone.popleft()}))
                await sleep(2)