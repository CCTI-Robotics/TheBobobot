#region VEXcode Generated Robot Configuration
from vex import *
# import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_36_1, False)
right_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_36_1, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
rotationizer = Rotation(Ports.PORT11, True)
eyes = Optical(Ports.PORT13)
intake = Motor(Ports.PORT8, GearSetting.RATIO_6_1, True)
armlad = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)
whiskers = Distance(Ports.PORT15)
# ye_olde_compass = Gps(Ports.PORT19, -100.00, -130.00, MM, 180)
ye_olde_compass = Gps(Ports.PORT19, -171, -70, MM, 180)


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


"""
171.45 x
gps offset
70mm y
Ideally we want to check the gps x and y position to find out where we take the alliance tri-ball
that the robot starts with, or check if there is a ball in the chamber (intake motor / arm).
-x and -y, Location E and F
-x and +y Location A and B
+x and +y Location C and D
+x and -y Location G and H

# optical ultrasonic gps rotation

A/B = Blue Defense
C/D = Blue Offense
E/F = Red Offense
G/H = Red Defense
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TODO #1
    In order to determine the robot's true position, I feel that we need to have the drivetrain
    heading value be the same as the gps heading value, checking the gps heading intermittently
    

TODO #2
    Once TODO #1 is complete, We need to use those results to decide what to do next:
        -make a function to take the loaded triball to the alliance goal
        -̶I̶f̶ w̶e̶ d̶o̶n̶'t̶ h̶a̶v̶e̶ a̶ t̶r̶i̶b̶a̶l̶l̶ i̶n̶ t̶h̶e̶ c̶h̶a̶m̶b̶e̶r̶, W̶e̶ g̶o̶ t̶o̶ t̶h̶e̶ n̶e̶c̶e̶s̶s̶a̶r̶y̶ m̶a̶t̶c̶h̶ l̶o̶a̶d̶ z̶o̶n̶e̶ a̶n̶d̶ p̶i̶c̶k̶ o̶n̶e̶ u̶p̶

TODO #3
    After we have the alliance triball in the goal, we could:
        - push other balls over the middle bar for extra points and then touch the alliance pole for the AWP if we are at the defensive position.
        - high-tail it to the alliance pole for the AWP if brain.screen.y_position()we are in a time crunch / we need to get done first / we are at the offensive position.


    -Zane
"""
#drivetrain.set_velocity(600,RPM)
def strtcheck(): #basing our knowledge on what team we are on and if we are on offense or defense off of our position on the mat
    global team,Pos
    team = None
    Pos = None
    if ye_olde_compass.x_position(MM) < 0 and ye_olde_compass.y_position(MM) < 0:
        team,Pos = "Red","Off"
    elif ye_olde_compass.x_position(MM) < 0 and ye_olde_compass.y_position(MM) > 0:
        team,Pos = "Blue","Def"
    elif ye_olde_compass.x_position(MM) > 0 and ye_olde_compass.y_position(MM) < 0:
        team,Pos = "Red","Def"
    else:
        team,Pos = "Blue","Off"
    
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
    distance = whiskers.object_distance(MM)
    print(distance)

    while not (distance > 1580 and distance < 1620):
        print(distance)
        if distance < 1600:
            drivetrain.drive(REVERSE, 50, PERCENT)
        else:
            drivetrain.drive(FORWARD, 50, PERCENT)
            
        distance = whiskers.object_distance(MM)

def red_offense_1():
    # change_heading(0)

    # y = ye_olde_compass.y_position(INCHES)

    # while y < 0:
    #     print(y)
    #     drivetrain.drive(FORWARD, 15, PERCENT)
    #     y =  ye_olde_compass.y_position(INCHES)

    print("Driving to center")
    drive_to_center()

    print("Moving right!")
    drivetrain.turn_for(LEFT, 45, DEGREES, 15, PERCENT)

def has_triball() -> int:
    """
    This function is to check if the robot has a triball in the chamber.
    """
    if not eyes.is_near_object():
        return Triball.NONE
    
    if eyes.color() == Color.RED:
        return Triball.RED
    
    elif eyes.color() == Color.GREEN:
        return Triball.GREEN
    
    elif eyes.color() == Color.BLUE:
        return Triball.BLUE

    return Triball.UNKNOWN

def red_offense(): 
    """
    This function is to control the robot when it starts in the red offensive position.
    """
    printed = False
    if armlad.position(DEGREES) <=4 or armlad.position(DEGREES) >= 350 and eyes.is_near_object():
        # Make the robot face straight
        change_heading(0)

        # Drive forward until we are in the middle of the field, or y = 0
        drivetrain.drive_for(FORWARD, abs(ye_olde_compass.y_position(MM)), MM, 15, PERCENT)

        # while ye_olde_compass.y_position(MM) < -200:
        #     drivetrain.drive(FORWARD, 10, PERCENT)
        #     if not printed:
        #         print("print 3: Driving forward; Y Position: ",ye_olde_compass.y_position(MM), "Heading: ",ye_olde_compass.heading())

        change_heading(90)
        # while ye_olde_compass.heading() < 267:
        #     drivetrain.turn(LEFT)
        #     if not printed:
        #         print("print 4: Turning left; Heading: ",ye_olde_compass.heading())

        while ye_olde_compass.heading() > 273:
            drivetrain.turn(RIGHT)
            if not printed:
                print("print 5: Turning right; Heading: ",ye_olde_compass.heading())
                printed = True
        drivetrain.drive_for(REVERSE,6,INCHES)
        print("This should run. If not, there's a problem.")
        while armlad.position(DEGREES)<550:
            armlad.spin(FORWARD)
            # print("print 6: Spinning arm forward; Position: ",armlad.position(DEGREES))
        drivetrain.drive_for(FORWARD,10,INCHES)
        drivetrain.drive_for(REVERSE,4,INCHES)
        print("Print 7: End")

def print_test():
    for i in range(60):
        print(has_triball())
        wait(1, SECONDS)

def print_positions():
    while True:
        print("X: ",ye_olde_compass.x_position(MM),"Y: ",ye_olde_compass.y_position(MM),"Heading: ",ye_olde_compass.heading())
        print("Distance", whiskers.object_distance(MM))
        wait(1,SECONDS)
    
# Thread(print_test)
# Thread(red_offense_1)
# print the total wattage of all motors
