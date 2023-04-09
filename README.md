# 콜드론 프로젝트
![한이음_콜드론_개발보고서](/한이음_콜드론_개발보고서.hwp)


---

### 내가 맡은 역할 : 클라이언트 - 서버 - 드론간의 실시간 통신 설계

1. 사용자가 서버에 드론 요청을 한다.(HTTP요청)
2. 서버와 드론사이에 멀티스레드 기반으로 실시간 소켓통신을 연결한다.(socket 라이브러리)
3. 드론으로부터 오는 실시간 GPS좌표 정보를 클라이언트에 전송하고 드론의 실시간 위치를 지도화면에 표시한다.(channels 라이브러리)


---

<img src="https://user-images.githubusercontent.com/87998104/230739034-21c93023-c8cb-4b6b-896d-4f3967abfc68.png" alt="이미지 설명" style="display: block; margin: 0 auto; width: 60%; border-radius: 3%;">

---

<img src="https://user-images.githubusercontent.com/87998104/230739970-10438ed8-c055-49d3-a4b7-752bd0286e7b.PNG" alt="이미지 설명" style="display: block; margin: 0 auto; width: 60%">


---

<img src="https://user-images.githubusercontent.com/87998104/230738473-58da00f2-e42e-404b-b510-3c265e164391.PNG" alt="이미지 설명" style="display: block; margin: 0 auto; width: 60%">

---

<img src="https://user-images.githubusercontent.com/87998104/230745685-98f8ec2e-d556-4f17-9bb9-eb404e3a46e6.png" alt="이미지 설명" style="display: block; margin: 0 auto; width: 60%" >

---


|![1](https://user-images.githubusercontent.com/87998104/230754877-18468225-3bed-4ce9-886f-a4ae3cebc6f8.gif)|![2](https://user-images.githubusercontent.com/87998104/230754399-5d58cb7b-24dd-4d1f-9355-af2b0cd87703.gif)|
| :-----------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------: |

<img src="https://user-images.githubusercontent.com/87998104/230754692-2779ad2c-44ea-4bb4-97de-19c4b7ce6f3e.gif" alt="이미지 설명" style="display: block; margin: 0 auto; width: 60%" >


---



<사용한 라이브러리>

python : 3.9.12

django : 4.06

socket

channels : 3.0.5

requests : 2.24.0

haversine : 2.7.0

kakao map api
