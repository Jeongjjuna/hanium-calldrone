#import PyLidar2
import cv2
import time

# camera
def camera(a, b):
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if capture.isOpened():
        ret, a = capture.read()

        while ret:
            ret, a = capture.read()
            cv2.imshow("test", a)

            if cv2.waitKey(1) & 0xFF ==27:
                break

    capture.release()
    cv2.destroyAllWindows()


# lidar
def lidar(a, b):
    port = "/dev/ttyUSB0" #linux
    Obj = PyLidar2.YdLidarX4(port)
    try:
        if(Obj.Connect()):
            print(Obj.GetDeviceInfo())
            gen = Obj.StartScanning()
            t = 0
            while t < 500: #scan for 30 seconds
                print(gen)
                data = next(gen)
                
                data[0]
                print(data[0])

                #time.sleep(2)
                t += 1
            Obj.StopScanning()
            Obj.Disconnect()
            print('ended1')
        else:
            print('ended2')
            print("Error connecting to device")
            Obj.StopScanning()
            Obj.Disconnect()
    except:
        print('ended3')
        Obj.StopScanning()
        Obj.Disconnect()