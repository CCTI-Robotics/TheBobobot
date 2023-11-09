#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
rotationizer = Rotation(Ports.PORT11, False) # Closed: 0, open 178.85
eyes = Optical(Ports.PORT13)
intake = Motor(Ports.PORT8, GearSetting.RATIO_6_1, False)
armlad = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)
whiskers = Distance(Ports.PORT15)
ye_olde_compass = Gps(Ports.PORT19, -171.00, -70.00, MM, 180)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code

armlad_moving = False
driving = False

class Triball:
    NONE = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    UNKNOWN = 4

def change_heading(desired_position: int):
    """
    This function is to change the heading of the robot to the desired position.
    """
    current_heading = ye_olde_compass.heading()

    plus10 = (desired_position + 10) if ((desired_position + 10) < 360) else ((desired_position + 10) - 360)
    minus10 = (desired_position - 10) if ((desired_position - 10) > 0) else ((desired_position - 10) + 360)

    print(plus10, minus10)

    while not (current_heading < plus10 or current_heading > minus10):
        print(current_heading)
        if current_heading > desired_position:
            drivetrain.turn(RIGHT, 15, PERCENT)
        else:
            drivetrain.turn(LEFT, 15, PERCENT)
            
        current_heading = ye_olde_compass.heading()

def drive_to_center():
    global driving
    driving = True
    distance = whiskers.object_distance(MM)
    print(distance)

    while not (distance > 1580 and distance < 1620):
        print(distance)
        if distance < 1600:
            drivetrain.drive(REVERSE, 80, PERCENT)
        else:
            drivetrain.drive(FORWARD, 80, PERCENT)
            
        distance = whiskers.object_distance(MM)
    
    driving = False

def open_armlad():
    # global armlad_moving
    # armlad_moving = True

    rotation = rotationizer.angle()

    

    # armlad.spin_to_position(500, DEGREES, 50, PERCENT)

    counter = 1

    print("Rotation: ", rotation, "Counter: ", counter)
    armlad.spin_to_position(3200, DEGREES, 70, PERCENT, wait=False)
    rotation = rotationizer.angle()
    print("Rotation: ", rotation, "Counter: ", counter)

    counter += 1

    # armlad_moving = False

def red_offense_1():
    # change_heading(0)

    # y = ye_olde_compass.y_position(INCHES)

    # while y < 0:
    #     print(y)
    #     drivetrain.drive(FORWARD, 15, PERCENT)
    #     y =  ye_olde_compass.y_position(INCHES)

    # Move the robot to the center of the field
    print("Driving to center")
    drive_to_center()

    # Open up the armlad
    print("Spinning!")
    open_armlad()

    # Turn the robot to face the goal
    print("Moving Left!")
    drivetrain.turn_for(LEFT, 90/1.10, DEGREES, 100, PERCENT)

    drivetrain.drive_for(REVERSE, 300, MM, 90, PERCENT)


    #920

    drivetrain.drive_for(FORWARD, 250, MM, 75, PERCENT)

    # distance = whiskers.object_distance()

    # counter = 1

    # while not distance < 930:
    #     print(distance, counter)
    #     drivetrain.drive(FORWARD, 10, PERCENT)
    #     distance = whiskers.object_distance()
    #     counter += 1

    # Expell the triball from the robot
    intake.spin_for(REVERSE, 720, DEGREES, 50, PERCENT)
    armlad.spin_to_position(0, DEGREES, 100, PERCENT)

    # Ram the triball into the goal
    drivetrain.drive_for(FORWARD, 400, MM, 100, PERCENT)
    # drivetrain.drive_for(REVERSE, 100, MM, 75, PERCENT)
    # drivetrain.drive_for(FORWARD, 110, MM, 75, PERCENT)
    drivetrain.drive_for(REVERSE, 200, MM, 50, PERCENT)

    # wait(100, MSEC)

    # Turn the robot back towards its starting position
    drivetrain.turn_for(LEFT, 90/1.20, DEGREES, 90, PERCENT)

    distance = whiskers.object_distance()
    print(distance)

    # Drive towards the starting position until it gets close to the wall
    while distance > 600:
        drivetrain.drive(FORWARD, 100, PERCENT)
        distance = whiskers.object_distance()
        print(distance)
    
    drivetrain.stop(mode=BRAKE)


red_offense_1()