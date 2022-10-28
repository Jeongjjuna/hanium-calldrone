from dronekit import connect, VehicleMode, LocationGlobalRelative
import socket
import time
from _thread import *
from collections import deque
import time

lidar_q = deque()
target_q = deque()


def arm():
    # Check pre-arm
    print("\nBasic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise ...")
        time.sleep(1)
    print("Pre-arm check has been completed!")

    # Change mode
    print("\nSet Vehicle.mode = GUIDED (currently: %s)" % vehicle.mode.name)
    vehicle.mode = VehicleMode("GUIDED")
    while not vehicle.mode.name == 'GUIDED':
        print(" Waiting for mode change ...")
        time.sleep(1)
    print("Currently Vehicle.mode: %s" % vehicle.mode.name)
    print("The mode change has been completed!")

    # Arm the vehicle
    print("\nSet Vehicle.armed = True (currently: %s)" % vehicle.armed)
    vehicle.armed = True
    while not vehicle.armed == True:
        print(" Waiting for armed status change ...")
        time.sleep(1)
    print("Currently Vehicle.armed: %s" % vehicle.armed)
    print("Vehicle arming has been completed!")


def takeoffing(altitude):
    print("\nTaking off!")
    try:
        # Move vehicle
        vehicle.simple_takeoff(altitude)

        # Wait until complete
        while True:
            print("Altitude:", vehicle.location.global_relative_frame.alt)
            if vehicle.location.global_relative_frame.alt >= altitude*0.95:
                print("Reached target altitude!")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        vehicle.mode = VehicleMode("LOITER")
        try:
            while True:
                print("Now Loiter Mode")
                time.sleep(1)
        except KeyboardInterrupt:
            vehicle.mode = VehicleMode("STABILIZE")
            while True:
                print("Now Stabilize Mode")
                time.sleep(1)


def moving(client_socket, lat, lon, alt, speed):
    global lidar_q

    print("\nGoing towards point1")
    try:
        print('moving : %s, %s', lat, lon)

        # Move vehicle
        point1 = LocationGlobalRelative(float(lat), float(lon), alt)
        print('moving : %f, %f', lat, lon)
        vehicle.simple_goto(point1, airspeed=speed)

        d = str(lat) + ' ' + str(lon)
        client_socket.send(d.encode())
        time.sleep(2)
        # Wait until complete
        while True:
            # -----------------------------realtime--------------
            print("Altitude:", vehicle.location.global_relative_frame.lat)
            print("Longitude:", vehicle.location.global_relative_frame.lon)
            x = str(vehicle.location.global_relative_frame.lat)
            y = str(vehicle.location.global_relative_frame.lon)
            data = x + ' ' + y
            client_socket.send(data.encode())

            # ------------------------------condition ended---------------
            if ((vehicle.location.global_relative_frame.lat >= point1.lat*0.9999995) and (vehicle.location.global_relative_frame.lat <= point1.lat*1.0000005)) and ((vehicle.location.global_relative_frame.lon >= point1.lon*0.999999995) and (vehicle.location.global_relative_frame.lon <= point1.lon*1.0000005)):
                print("Reached target place!")
                break

            # -----------------------ladar_q------------------------------------------
            # if len(lidar_q) > 0:
            #     dist = lidar_q.popleft()
            #     if dist < 3000:
            #         # change Auto mode

            #         while (dist > 3000):
            #             # left right move
            #             pass
            #         # target mode
            #         #point1 = LocationGlobalRelative(lat, lon, alt)
            #         # vehicle.simple_goto(point1)
            # print(dist)
            time.sleep(1)
    except KeyboardInterrupt:
        vehicle.mode = VehicleMode("LOITER")
        try:
            while True:
                print("Now Loiter Mode")
                time.sleep(1)
        except KeyboardInterrupt:
            vehicle.mode = VehicleMode("STABILIZE")
            while True:
                print("Now Stabilize Mode")
                time.sleep(1)


def returning():
    print("\nReturning to launch")

    # Download the vehicle waypoints
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

    # Mode change
    print("Set Vehicle.mode = RTL (currently: %s)" % vehicle.mode.name)
    vehicle.mode = VehicleMode("RTL")
    while not vehicle.mode.name == 'RTL':
        print(" Waiting for mode change ...")
        time.sleep(1)
    print("Currently Vehicle.mode: %s" % vehicle.mode.name)
    print("The mode change has been completed!")

    # Wait until complete
    while True:
        print("Altitude:", vehicle.location.global_relative_frame.lat)
        print("Longitude:", vehicle.location.global_relative_frame.lon)
        if vehicle.armed == False:
            print("Reached target place!")
            break
        time.sleep(1)


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

    print('django ended')
    client_socket.close()


def land():
    vehicle.mode = VehicleMode("LAND")
    try:
        print("Now Land Mode")
        while True:
            print("Altitude:", vehicle.location.global_relative_frame.alt)
            if vehicle.location.global_relative_frame.alt <= 0:
                print("Landing Complete!")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        vehicle.mode = VehicleMode("LOITER")
        try:
            while True:
                print("Now Loiter Mode")
                time.sleep(1)
        except KeyboardInterrupt:
            vehicle.mode = VehicleMode("STABILIZE")
            while True:
                print("Now Stabilize Mode")
                time.sleep(1)


# Set altitude and airspeed
alt = 2
speed = 1

# APP sever contact setting
HOST = '168.131.153.213'
PORT = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


# start_new_thread(camera, (0, 0))
# start_new_thread(lidar, (0, 0))
start_new_thread(listen_data_from_django, (client_socket, ))

# Connect to the vehicle
vehicle = connect('tcp:172.20.10.3:5762',
                  wait_ready=True, heartbeat_timeout=15)

# region - plz make function jonjar jihun
message = '0 0'
while True:
    client_socket.send(message.encode())
    time.sleep(2)
    print(target_q)

    if len(target_q) == 1:
        data = target_q[0]
        target_x, target_y = data.split()
        break
# endregion

# Arm vehicle
arm()


# Takeoff vehicle
takeoffing(alt)

# Move vehicle
moving(client_socket, target_x, target_y, alt, speed)

# Land
land()

# Return vehicle
# returning()

# Close vehicle
print("\nClose vehicle")
vehicle.close()
