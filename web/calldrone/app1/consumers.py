import json
from collections import deque
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer

# 장고 서버 실행시 WSConsumer class가 생성된다.
class WSConsumer(AsyncWebsocketConsumer):
    print("WSConsumer class생성완료")
    
    # 외부 드론으로부터 들어오는 위치정보 데이터를 담고있는 Queue자료구조
    data_from_drone = deque([])
    
    # 클라이언트 단에서 웹소켓 연결요청을 하면 connect함수가 실행 된다
    # 연결이 끊어지면 connect함수는 종료 된다
    async def connect(self):
        print('connect함수 실행')
        await self.accept()
        
        
        # 사용자가 새로 지도페이지에 접속했기 때문에
        # data_from_drone 내부값을 비워주고 새로 갱신한다.
        print('위치정보갱신')
        self.data_from_drone.clear()

        while True:
            try:
                if self.data_from_drone:
                    await self.send(json.dumps({'message' : self.data_from_drone.popleft()}))
                    await sleep(2)
            except:
                break
        print('connect함수 종료')