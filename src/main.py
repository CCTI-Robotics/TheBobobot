#region VEXcode Generated Robot Configuration
from vex import *
# import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
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

global drivetrain_needs_to_be_stopped_controller_1, controller_1_left_shoulder_control_motors_stopped, controller_1_x_b_buttons_control_motors_stopped, remote_control_code_enabled

# define variables used for controlling motors based on controller inputs
controller_1_left_shoulder_control_motors_stopped = True
controller_1_x_b_buttons_control_motors_stopped = True
drivetrain_needs_to_be_stopped_controller_1 = False



def control_armlad():
    global drivetrain_needs_to_be_stopped_controller_1, controller_1_left_shoulder_control_motors_stopped, controller_1_x_b_buttons_control_motors_stopped, remote_control_code_enabled
    if controller_1.buttonL1.pressing():
        armlad.set_velocity(300,RPM)
        armlad.spin_to_position(0,DEGREES,wait=True)
        controller_1_left_shoulder_control_motors_stopped = False
    elif controller_1.buttonL2.pressing():
        armlad.set_velocity(300,RPM)
        armlad.spin_to_position(3200,DEGREES,wait=True)
        controller_1_left_shoulder_control_motors_stopped = False
    elif not controller_1_left_shoulder_control_motors_stopped:
        armlad.stop()

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_needs_to_be_stopped_controller_1, controller_1_left_shoulder_control_motors_stopped, controller_1_x_b_buttons_control_motors_stopped, remote_control_code_enabled

    
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis4
            # right = axis3 - axis4
            drivetrain_left_side_speed = controller_1.axis3.position() + controller_1.axis4.position()
            drivetrain_right_side_speed = controller_1.axis3.position() - controller_1.axis4.position()
            
            # check if the values are inside of the deadband range
            if abs(drivetrain_left_side_speed) < 5 and abs(drivetrain_right_side_speed) < 5:
                # check if the motors have already been stopped
                if drivetrain_needs_to_be_stopped_controller_1:
                    # stop the drive motors
                    left_drive_smart.stop()
                    right_drive_smart.stop()
                    # tell the code that the motors have been stopped
                    drivetrain_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the motors next
                # time the input is in the deadband range
                drivetrain_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.set_max_torque(100,PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.set_max_torque(100,PERCENT)
                right_drive_smart.spin(FORWARD)
            # check the buttonL1/buttonL2 status
            # to control armlad
            Thread(control_armlad)
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
            controller_1_left_shoulder_control_motors_stopped = True
            # check the buttonX/buttonB status
            # to control intake
            if controller_1.buttonB.pressing():
                intake.set_velocity(600,RPM)
                intake.spin(FORWARD)
                controller_1_x_b_buttons_control_motors_stopped = False
            elif controller_1.buttonX.pressing():
                intake.set_velocity(600,RPM)
                intake.spin(REVERSE)
                controller_1_x_b_buttons_control_motors_stopped = False
            elif not controller_1_x_b_buttons_control_motors_stopped:
                intake.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_x_b_buttons_control_motors_stopped = True
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

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

def red_offense():
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


competition = Competition(lambda: print("Hi!"), red_offense)