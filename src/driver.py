#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_36_1, False)
right_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_36_1, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
succer = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
armlad = Motor(Ports.PORT4, GearSetting.RATIO_36_1, False)


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
        armlad.spin_to_position(-550,DEGREES,wait=True)
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
            # to control succer
            if controller_1.buttonB.pressing():
                succer.set_velocity(600,RPM)
                succer.spin(FORWARD)
                controller_1_x_b_buttons_control_motors_stopped = False
            elif controller_1.buttonX.pressing():
                succer.set_velocity(600,RPM)
                succer.spin(REVERSE)
                controller_1_x_b_buttons_control_motors_stopped = False
            elif not controller_1_x_b_buttons_control_motors_stopped:
                succer.stop()
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