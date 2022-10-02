import time
import socket

from _thread import *
from thread_func import *

#HOST = socket.gethostname()
#HOST = '172.23.16.1'
HOST = '168.131.153.213'  
PORT = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

if __name__=="__main__":
    start_new_thread(camera, (0, 0))
    start_new_thread(lidar, (0, 0))
    start_new_thread(listen_data_from_django, (client_socket, ))


    try:
        message = 37.5665
        while True: 
            client_socket.send(str(message).encode())
            message *= 1.000001
            print(message)
            time.sleep(2)
    except:
        time.sleep(2)
