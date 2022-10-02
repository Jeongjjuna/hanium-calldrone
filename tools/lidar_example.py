import PyLidar2
import time # Time module
#Serial port to which lidar connected, Get it from device manager windows
#In linux type in terminal -- ls /dev/tty*
#port = input("Enter port name which lidar is connected:") #windows
port = "/dev/ttyUSB0" #linux
Obj = PyLidar2.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size)

try:
    if(Obj.Connect()):
        print(Obj.GetDeviceInfo())
        gen = Obj.StartScanning()
        t = 0
        while t < 500: #scan for 30 seconds
            print(gen)
            data = next(gen)
        
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
