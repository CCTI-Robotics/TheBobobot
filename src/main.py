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
    
# def red_offense_1():
#     """
#     This method is to control the robot when it starts in a Red Offensive area. 
#     The robot will drop its alliance tri-ball in the nearest goal, then go to the 
#     red match load zone and take a tri-ball. It will then go to the alliance pole
#     and touch it for the AWP.
#     """
#     if not ye_olde_compass.heading 

class Position(int):
    def __init__(self, value):
        super().__init__()

    def __add__(self, other):
        new = super().__add__(other)
        if new > 360:
            new -= 360
        return Position(new)
    
    def __sub__(self, other):
        new = super().__sub__(other)
        if new < 0:
            new += 360
        return Position(new)
    

def change_heading(desired_position: Position):
    """
    This function is to change the heading of the robot to the desired position.
    """
    current_heading = ye_olde_compass.heading()
    while not (current_heading > desired_position - 10 and current_heading < desired_position + 10):
        if current_heading > desired_position:
            drivetrain.turn(RIGHT, 15, PERCENT)
        else:
            drivetrain.turn(LEFT, 15, PERCENT)
            
        current_heading = ye_olde_compass.heading()

def red_offense(): 
    """
    This function is to control the robot when it starts in the red offensive position.
    """
    printed = False
    if armlad.position(DEGREES) <=4 or armlad.position(DEGREES) >= 350 and eyes.is_near_object():
        # Make the robot face straight
        # while ye_olde_compass.heading() < -177:
        #     drivetrain.turn(LEFT, 10, PERCENT)
        #     if not printed:
        #         print("print 1: Turning left; Heading: ",ye_olde_compass.heading())
        #         printed = True
        # printed = False
        # while ye_olde_compass.heading() < -357:
        #     drivetrain.turn(RIGHT, 10, PERCENT)
        #     if not printed:
        #         print("print 2: Turning right; Heading: ",ye_olde_compass.heading())
        #         printed = True
        # printed = False

        # current_heading = ye_olde_compass.heading()
        # while not (current_heading > 350 or current_heading < 10):
        #     if current_heading > 180:
        #         drivetrain.turn(RIGHT, 15, PERCENT)
        #     else:
        #         drivetrain.turn(LEFT, 15, PERCENT)
                
        #     current_heading = ye_olde_compass.heading()

        change_heading(Position(0))

        print("Done with that")

 

        while ye_olde_compass.y_position(MM) < -200:
            drivetrain.drive(FORWARD, 10, PERCENT)
            if not printed:
                print("print 3: Driving forward; Y Position: ",ye_olde_compass.y_position(MM), "Heading: ",ye_olde_compass.heading())
                printed = True
        printed = False
        while ye_olde_compass.heading() < 267:
            drivetrain.turn(LEFT)
            if not printed:
                print("print 4: Turning left; Heading: ",ye_olde_compass.heading())
                printed = True
        printed = False
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
    print("Hello, world!")

def print_positions():
    while True:
        print("X: ",ye_olde_compass.x_position(MM),"Y: ",ye_olde_compass.y_position(MM),"Heading: ",ye_olde_compass.heading())
        wait(1,SECONDS)
    
Thread(print_positions)
Thread(red_offense)