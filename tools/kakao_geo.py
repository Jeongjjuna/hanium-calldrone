# 카카오API를 사용하여 주소->좌표 변환
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

crd = get_location("광주광역시 도산로 9번길 35")
print(crd)



# 카카오API를 사용하여 좌표->주소 변환
# import requests, json, pprint

# def get_address(lat, lng):
#     url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x="+lng+"&y="+lat
#     # 'KaKaoAK '는 그대로 두시고 개인키만 지우고 입력해 주세요.
#     # ex) KakaoAK 6af8d4826f0e56c54bc794fa8a294
#     headers = {"Authorization": "KakaoAK 개인키"}
#     api_json = requests.get(url, headers=headers)
#     full_address = json.loads(api_json.text)

#     return full_address

# full_address = get_address('36.5760732781656', '128.15935928504484')
# pprint.pprint(full_address)