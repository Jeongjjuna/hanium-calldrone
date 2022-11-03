from django.shortcuts import render, redirect
from django.http import HttpResponse

from collections import deque
from haversine import haversine, Unit

from app1.consumers import WSConsumer
import requests, json

#-----------------카카오 소셜 로그인/로그아웃----------------
def login(request):
    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
        return render(request, 'app1/page1.html', _context)
    return render(request, 'app1/login.html', _context)

def kakaoLoginLogic(request):
    _restApiKey = '9f978728a234188af99c073236af7def' # 입력필요
    _redirectUrl = 'http://127.0.0.1:8000/app1/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    try:
        _qs = request.GET['code']
        _restApiKey = '9f978728a234188af99c073236af7def' # 입력필요
        _redirect_uri = 'http://127.0.0.1:8000/app1/kakaoLoginLogicRedirect'
        _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
        _res = requests.post(_url)
        _result = _res.json()
        request.session['access_token'] = _result['access_token']
        request.session.modified = True

        _context = {'check':False}
        if request.session.get('access_token'):
            _context['check'] = True
        return render(request, 'app1/page1.html', _context)
    except:
        _context = {'check':False}
        return render(request, 'app1/login.html', _context)

    

def kakaoLogout(request):
    _token = request.session['access_token']
    # _url = 'https://kapi.kakao.com/v1/user/logout'
    # _header = {
    #     'Authorization': f'bearer {_token}'
    # }
    _url = 'https://kapi.kakao.com/v1/user/unlink'
    _header = {
        'Authorization': f'bearer {_token}',
    }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    if _result.get('id'):
        del request.session['access_token']
        _context = {'check':False}
        return render(request, 'app1/login.html', _context)
    else:
        return render(request, 'logoutError.html')

#--------------주소 -> 위경도바꾸는 함수--------

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
    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'app1/page1.html', _context)

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

        # (평균속도, 최대시간)
        drone_payload = [(60, '최대시간1'), (50, '최대시간2'),
                        (40, '최대시간3'), (30, '최대시간4'),
                        (20, '최대시간5'), (10, '최대시간6')]

        drone_max_dist = [0.33, 0.34, 0.35, 0.36, 0.37, 0.38]

        drone = [['F450', '/static/app1/css/images/F450.png', round(dist_target/60, 5)], ['S500', '/static/app1/css/images/S500.png', round(dist_target/50, 5)],
        ['IM-680', '/static/app1/css/images/F450.png', round(dist_target/40, 5)], ['X6', '/static/app1/css/images/X6.png', round(dist_target/30, 5)],
        ['EV410', '/static/app1/css/images/EV410.png', round(dist_target/20, 5)], ['EV610', '/static/app1/css/images/EV610.png', round(dist_target/10, 5)]]

        context={'data' : [], 'dist': dist_target}
        for i, dist in enumerate(drone_max_dist):
            if dist_target < dist:
                d = dict()
                d['name'] =  drone[i][0]
                d['address'] = drone[i][1]
                d['time'] = drone[i][2]
                context['data'].append(d)
        
        '''
        이름, 이미지주소, 도착예정시간
        contex = {'data' : [{'name' : 이름1', 'address' : '어드레스1,
                'time' : dist_target/60}, ], 'dist': dist_target}
        '''
        return render(request, 'app1/page5.html', context=context)


    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'app1/page2.html', _context)

def page3(request):
    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'app1/page3.html', _context)

def page4(request):
    WSConsumer.data_from_drone.append('stop')
    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'app1/page4.html', _context)

def page5(request):
    if request.method == 'POST':
        # manage.py에서 start가 들어가면 드론에 출발하라고 전송해준다.
        send_data_to_drone.append('start')
        return redirect('page1')

    _context = {'check':False}
    if request.session.get('access_token'):
        _context['check'] = True
    return render(request, 'app1/page5.html', _context)