#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import socket
import sys
import time
from _thread import *

from app1.consumers import WSConsumer


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calldrone.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def listen_data_from_jetson(client_socket, addr):
    print('success connected drone!')
    while True:
        try:
            # 데이터 수신
            data = client_socket.recv(1024)

            # 드론으로부터 아무 정보수신도 되지 않는다면
            # 연결이 끊겼다고 생각하고 while문 나가기
            if not data:
                break
            
            # 디코딩된 문자열을 실수로변환
            data = float(data.decode())
            WSConsumer.data_from_drone.append(data)
            
            print(WSConsumer.data_from_drone)
        except ConnectionResetError as e:
            break

    print('드론 연결 종료' + addr[0],':',addr[1]) # 예외발생시 젯슨과의 tcp연결 종료를 알리는 디벙깅용함수
    client_socket.close() #젯슨 과의 클라이언트 연결 종료     


if __name__ == '__main__':
    # socket통신 세팅
    HOST = '127.0.0.1'
    PORT = 9999
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()  # 프로젝트용 드론1개기준 socket접속대기
    print('프로젝트용 드론 1대를 접속 대기중입니다...')
    client_socket, addr = server_socket.accept()

    # 프로젝트용 드론이 연결 되었다면..
    # jetson으로부터 실시간 수신대기하는 쓰레드생성
    start_new_thread(listen_data_from_jetson, (client_socket, addr))
    
    # django 서버 시작
    main()
