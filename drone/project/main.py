import socket
import time

# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = '127.0.0.1'  
PORT = 9999       


# 소켓 객체를 생성합니다. 
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
client_socket.connect((HOST, PORT))



# GPS값을 2초마다 한번씩 전송한다.
message = 37.5665
while True: 
    client_socket.send(str(message).encode())
    message *= 1.000001
    time.sleep(2)

client_socket.close()