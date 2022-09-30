import socket
import time
from _thread import *

def listen_data_from_django(client_socket):
    print('success connected server!')
    while True:
        try:
            # 데이터 수신
            data = client_socket.recv(1024)

            # django서버로부터 아무 데이터도 들어오지 않는다면
            # 연결 종료
            if not data:
                break
            
            # 디코딩된 문자열을 실수로변환
            data = float(data.decode())
            print(data)
        except ConnectionResetError as e:
            break

    print('django와 연결 종료')
    client_socket.close() #젯슨 과의 클라이언트 연결 종료



# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = '127.0.0.1'  
PORT = 9999       

# 소켓 객체를 생성합니다. 
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
client_socket.connect((HOST, PORT))
# 페이지 요청으로부터 오는 정보 수신(django로부터 오는 데이터 수신스레드)
start_new_thread(listen_data_from_django, (client_socket, ))



# gps값을 2초마다 한번씩 전송한다.
message = 37.5665
while True: 
    client_socket.send(str(message).encode())
    message *= 1.000001
    time.sleep(2)

    # <주행에 필요한 정보>
    # 라이다 정보
    # 픽사호크로브부터 gps(x, y)

    # <전송해야할 정보>
    # 픽사호크로브부터 gps(x, y)
    # 배터정보 받고
    # 기울기 정보