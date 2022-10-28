from django.shortcuts import render, redirect
from django.http import HttpResponse

from collections import deque
from haversine import haversine, Unit

from app1.consumers import WSConsumer
#--------------주소 -> 위경도바꾸는 함수--------
import requests, json

def get_location(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    # 'KaKaoAK '는 그대로 두시고 개인키만 지우고 입력해 주세요.
    # ex) KakaoAK 6af8d4826f0e56c54bc794fa8a294
    headers = {"Authorization": "KakaoAK 9f978728a234188af99c073236af7def"}
    api_json = json.loads(str(requests.get(url,headers=headers).text))
    address = api_json['documents'][0]['address']
    crd = {"lat": str(address['y']), "lng": str(address['x'])}
    address_name = address['address_name']

    return crd


send_data_to_drone = deque() #manage.py에서 함께 공유하는 변수

# Create your views here.
def page1(request):
    WSConsumer.data_from_drone.append('stop')
    return render(request, 'app1/page1.html')

def page2(request):
    global send_data_to_drone
    WSConsumer.data_from_drone.append('stop')
    
    if request.method == 'POST':
        address = request.POST['도로명주소']
        weight = request.POST['무게']
        width = request.POST['가로']
        height = request.POST['세로']
        high = request.POST['높이']
        crd = get_location(address)

        print(f'\n\n입력받은 주소 : {address}') # "광주광역시 도산로 9번길 35"
        print(f'목적지 위경도 : {crd}') # {'lat': '35.1276555542395', 'lng': '126.790916656135'}
        
        # 드론으로 전송할 데이터를 넣어주기!!
        # send_data_to_drone.append(crd['lat']+' '+crd['lng'])
        send_data_to_drone.append('35.180304'+' '+'126.908297') # 도착 좌표 임의로 지정

        pre_grid = (35.180001, 126.908111) # 시작좌표
        target_grid = (35.180304, 126.908297) # 도착좌표
        dist_target = haversine(pre_grid, target_grid)
        print(f'목적지 까지 거리 : {dist_target}\n\n') # km

        return render(request, 'app1/page5.html')

    return render(request, 'app1/page2.html')

def page3(request):
    return render(request, 'app1/page3.html', context={'text' : 'Hello World'})

def page4(request):
    WSConsumer.data_from_drone.append('stop')
    return render(request, 'app1/page4.html')

def page5(request):
    if request.method == 'POST':
        # manage.py에서 start가 들어가면 드론에 출발하라고 전송해준다.
        send_data_to_drone.append('start')
        return redirect('page1')

    return render(request, 'app1/page5.html')