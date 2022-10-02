import time
from dronekit import connect, VehicleMode, LocationGlobalRelative


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

    # Move vehicle
    vehicle.simple_takeoff(altitude)

    # Wait until complete
    while True:
        print("Altitude:", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= altitude*0.95:
            print("Reached target altitude!")
            break
        time.sleep(1)


def moving(lat, lon, alt):
    print("\nGoing towards point1")

    # Move vehicle
    point1 = LocationGlobalRelative(lat, lon, alt)
    vehicle.simple_goto(point1)

    # Wait until complete
    while True:
        print("Altitude:", vehicle.location.global_relative_frame.lat)
        print("Longitude:", vehicle.location.global_relative_frame.lon)
        if ((vehicle.location.global_relative_frame.lat >= point1.lat*0.9999995) and (vehicle.location.global_relative_frame.lat <= point1.lat*1.0000005)) and ((vehicle.location.global_relative_frame.lon >= point1.lon*0.999999995) and (vehicle.location.global_relative_frame.lon <= point1.lon*1.0000005)):
            print("Reached target place!")
            break
        if ((vehicle.location.global_relative_frame.lat >= point1.lat*0.9999995) and (vehicle.location.global_relative_frame.lat <= point1.lat*1.0000005)) and ((vehicle.location.global_relative_frame.lon >= point1.lon*0.999999995) and (vehicle.location.global_relative_frame.lon <= point1.lon*1.0000005)):
            print("Reached target place!")
            break
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


def printInstance():
    # Print instance of the Vehicle class
    print("Attitude: %s" % vehicle.attitude)
    print("Battery: %s" % vehicle.battery)
    print("Mode: %s" % vehicle.mode.name)
    print("Armable: %s" % vehicle.is_armable)


if __name__ == "__main__":

    try:
        # Connect to the vehicle
        vehicle = connect('tcp:127.0.0.1:5762',
                          wait_ready=True, heartbeat_timeout=15)

        # Arm vehicle
        arm()

        # Takeoff vehicle
        takeoffing(10)

        # Set airspeed
        print("Set airspeed to 10")
        vehicle.airspeed = 10

        # Move vehicle
        moving(35.178304, 126.909166, 10)

        # Return vehicle
        returning()

        # Close vehicle
        print("\nClose vehicle")
        vehicle.close()

    except:
        print('\nSome other error!')

        returning()

        print("\nClose vehicle")
        vehicle.close()
