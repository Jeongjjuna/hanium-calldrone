from django.shortcuts import render
from django.http import HttpResponse

from collections import deque

send_data_to_drone = deque() #manage.py에서 함께 공유하는 변수

# Create your views here.
def page1(request):
    return render(request, 'app1/page1.html')

def page2(request):
    global send_data_to_drone
    '''
    만약 post정보가 들어온다면
        1. 목적지정보(위치, 구, 상세주소)
        2. 원하는 배송품 무게

        ->
        1. 목적지 정보 데이터로 거리를 계산한다
        2. 드론속도정보[1,2,3,
                    4,5,6,
                    7,8,9]

        >>>>>> 사용자에게 최적 정보를 렌더링 해줘야함
    '''
    send_data_to_drone.append('927.2447')
    return render(request, 'app1/page2.html')

def page3(request):
    return render(request, 'app1/page3.html', context={'text' : 'Hello World'})

def page4(request):
    return render(request, 'app1/page4.html')