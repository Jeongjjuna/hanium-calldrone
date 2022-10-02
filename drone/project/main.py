import socket
import time
from _thread import *
from collections import deque

#import PyLidar2
#import cv2
import time

ladar_q = deque()

# lidar
def lidar(a, b):
    global lidar_q

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
                
                lidar_q.append(data[0])
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



target_q = deque()
#from thread_func import *


#from dronekit import connect, VehicleMode, LocationGlobalRelative

# def arm():
#     # Check pre-arm
#     print("\nBasic pre-arm checks")
#     while not vehicle.is_armable:
#         print(" Waiting for vehicle to initialise ...")
#         time.sleep(1)
#     print("Pre-arm check has been completed!")

#     # Change mode
#     print("\nSet Vehicle.mode = GUIDED (currently: %s)" % vehicle.mode.name)
#     vehicle.mode = VehicleMode("GUIDED")
#     while not vehicle.mode.name == 'GUIDED':
#         print(" Waiting for mode change ...")
#         time.sleep(1)
#     print("Currently Vehicle.mode: %s" % vehicle.mode.name)
#     print("The mode change has been completed!")

#     # Arm the vehicle
#     print("\nSet Vehicle.armed = True (currently: %s)" % vehicle.armed)
#     vehicle.armed = True
#     while not vehicle.armed == True:
#         print(" Waiting for armed status change ...")
#         time.sleep(1)
#     print("Currently Vehicle.armed: %s" % vehicle.armed)
#     print("Vehicle arming has been completed!")


# def takeoffing(altitude):
#     print("\nTaking off!")

#     # Move vehicle
#     vehicle.simple_takeoff(altitude)

#     # Wait until complete
#     while True:
#         print("Altitude:", vehicle.location.global_relative_frame.alt)
#         if vehicle.location.global_relative_frame.alt >= altitude*0.95:
#             print("Reached target altitude!")
#             break
#         time.sleep(1)


def moving(client_socket, lat, lon, alt):
    print("\nGoing towards point1")
    print(f'moving : {lat}, {lon}')

    # Move vehicle
    #point1 = LocationGlobalRelative(lat, lon, alt)
    #vehicle.simple_goto(point1)


    d = str(lat) + ' ' + str(lon)
    client_socket.send(d.encode())
    time.sleep(2)
    # Wait until complete
    while True:
        # ------------------------------실시간 좌표 전송--------------
        #print("Altitude:", vehicle.location.global_relative_frame.lat)
        #print("Longitude:", vehicle.location.global_relative_frame.lon)
        #x = str(vehicle.location.global_relative_frame.lat)
        #y = str(vehicle.location.global_relative_frame.lon)
        #data = x + ' ' + y
        #client_socket.send(data.encode())
        
        # ------------------------------도착 종료 조건 확인---------------
        #if ((vehicle.location.global_relative_frame.lat >= point1.lat*0.9999995) and (vehicle.location.global_relative_frame.lat <= point1.lat*1.0000005)) and ((vehicle.location.global_relative_frame.lon >= point1.lon*0.999999995) and (vehicle.location.global_relative_frame.lon <= point1.lon*1.0000005)):
        #    print("Reached target place!")
        #    break
        
        #-----------------------ladar_q 값확인------------------------------------------
        if len(ladar_q)>0:
            dist = ladar_q.popleft()
            if dist < 3000:
                # Auto모드로 변경

                while (dist > 3000):
                    # 좌 혹은 우로 이동하기 명령(한 2미터정도는 이동하도록해야될듯)
                    pass
                # 다시 목표지점으로 이동설정
                #point1 = LocationGlobalRelative(lat, lon, alt)
                #vehicle.simple_goto(point1)


        time.sleep(2)


# def returning():
#     print("\nReturning to launch")

#     # Download the vehicle waypoints
#     cmds = vehicle.commands
#     cmds.download()
#     cmds.wait_ready()

#     # Mode change
#     print("Set Vehicle.mode = RTL (currently: %s)" % vehicle.mode.name)
#     vehicle.mode = VehicleMode("RTL")
#     while not vehicle.mode.name == 'RTL':
#         print(" Waiting for mode change ...")
#         time.sleep(1)
#     print("Currently Vehicle.mode: %s" % vehicle.mode.name)
#     print("The mode change has been completed!")

#     # Wait until complete
#     while True:
#         print("Altitude:", vehicle.location.global_relative_frame.lat)
#         print("Longitude:", vehicle.location.global_relative_frame.lon)
#         if vehicle.armed == False:
#             print("Reached target place!")
#             break
#         time.sleep(1)


# def printInstance():
#     # Print instance of the Vehicle class
#     print("Attitude: %s" % vehicle.attitude)
#     print("Battery: %s" % vehicle.battery)
#     print("Mode: %s" % vehicle.mode.name)
#     print("Armable: %s" % vehicle.is_armable)


# target_q -> main.py
def listen_data_from_django(client_socket):
    global target_q
    print('success connected server!')
    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                break

            data = data.decode()
            target_q.append(data)
        except ConnectionResetError as e:
            break

    print('django와 연결 종료')
    client_socket.close()


HOST = '127.0.0.1'
#HOST = '168.131.153.213'  
PORT = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


#start_new_thread(camera, (0, 0))
#start_new_thread(lidar, (0, 0))
start_new_thread(listen_data_from_django, (client_socket, ))

try:
    '''
    # Connect to the vehicle
    vehicle = connect('tcp:127.0.0.1:5762',
                    wait_ready=True, heartbeat_timeout=15)

    # Arm vehicle
    arm()

    '''

    # 목적지 좌표를 전송 받으면 이륙
    message = '0 0'
    while True:
        client_socket.send(message.encode())
        time.sleep(2)
        print(target_q)

        if len(target_q) == 1:
            data = target_q[0]
            target_x, target_y = data.split()
            break

        # if len(target_q) != 0:
        #     data = target_q.pop()
        #     target_x, target_y = map(float, data.split())
        #     print(target_x, target_y)
        #     break
    
    '''
    # Takeoff vehicle
    takeoffing(10)

    # Set airspeed
    print("Set airspeed to 10")
    vehicle.airspeed = 10
    '''

    # Move vehicle
    moving(client_socket, target_x, target_y, 10)

    # Return vehicle
    returning()

    # Close vehicle
    print("\nClose vehicle")
    vehicle.close()

except:
    print('\nSome other error!')

    #returning()

    print("\nClose vehicle")
    #vehicle.close()
