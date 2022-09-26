#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
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
    print('listen_data_from_jetson생성!')
    a = 37.5665
    while True:
        WSConsumer.data_from_drone.append(a)
        time.sleep(2)
        a = a * (1.000001)
        print(WSConsumer.data_from_drone)


if __name__ == '__main__':
    """
    드론 - 서버 소켓통신 시작하는 쓰레드 함수
    WSconsumer 클래스의 변수(data_from_drone)에 접근하여 드론으로부터의 실시간 데이터를 전달해줄 수 있다.
    """
    start_new_thread(listen_data_from_jetson, (0, 1))
    
    """django 서버 시작하는 함수"""
    main()
