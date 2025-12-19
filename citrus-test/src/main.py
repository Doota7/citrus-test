# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       savai                                                        #
#   Created:      9/4/2025, 6:57:26 PM                                         #
#   Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       syota                                                        #
#   Created:      9/15/2025, 9:51:04 PM                                        #
#   Description:  V5 project                                                   #
#                                                                              #
# ---------------------- ^ yeah I guess I'm here too ^ ----------------------- #

#   ## ##  ###### ###### ###### ##  ## ###### ###### ###### ## ## ## ###### ###### ###### 
#  ####### ##  ## ##  ## ##     ##  ## ##  ## ##     ##     ## ## ## ##     ##     ##  ## 
#   ## ##  ###### ###### ###### ###### ###### ##     ###### ## ## ## ###### ###### ###### 
#  #######     ## ##  ##     ##     ##     ## ##         ## ## ## ## ##     ##     ##     
#   ## ##      ## ###### ######     ##     ## ###### ###### ######## ###### ###### ##   


#

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()
#controller
controller_1 = Controller(PRIMARY)




# Set pen color to orange
brain.screen.set_pen_color(Color.ORANGE)




# Print your text
brain.screen.print("Citrus 𓄿𓄿𓄿")

# Why are we making every single thing a comment



#individual motors vars.
motor_topLeft = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
motor_middleLeft = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
motor_backLeft = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)

motor_topRight = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)
motor_middleRight = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
motor_backRight = Motor(Ports.PORT21, GearSetting.RATIO_18_1, False)

motor_intake1 = Motor(Ports.PORT18, GearSetting.RATIO_18_1, True)
motor_intake2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
motor_intake3 = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)

match_load_piston = DigitalOut(brain.three_wire_port.b)
descore_piston = DigitalOut(brain.three_wire_port.h)


# motor groups, drivetrain #1
left_motors = MotorGroup(motor_topLeft, motor_middleLeft, motor_backLeft)
right_motors = MotorGroup(motor_topRight, motor_middleRight, motor_backRight)
intake_motors = MotorGroup(motor_intake1, motor_intake2)

drivetrain = DriveTrain(lm=left_motors, rm=right_motors,
                        externalGearRatio=4.5, # lol
                        units=DistanceUnits.IN,
                        wheelTravel=10.21, # circumference of wheels (3.25 in)
                        trackWidth=10.56, # width of drivetrain from center of wheels
                        wheelBase=11.56) # length of drivetrain from center of wheels (11.56)

# Setting the velocity of stuff
drivetrain.set_drive_velocity(60, PERCENT)
drivetrain.set_turn_velocity(50, PERCENT)
motor_intake1.set_velocity(50, PERCENT)
motor_intake2.set_velocity(100, PERCENT)
motor_intake3.set_velocity(100, PERCENT)
driveVelocity = 0.55
turnVelocity = 0.20

def arcadeDriveLoop(left, right):
    leftPower, rightPower = (left + right) * driveVelocity, (left - right) * driveVelocity

    left_motors.set_velocity(leftPower, PERCENT)
    right_motors.set_velocity(rightPower, PERCENT)

    left_motors.spin(FORWARD)
    right_motors.spin(FORWARD)


batteryReports = -1 # sorry, magic numbers inbound!!! this one's -1 because of an off-by-one error because we're doing += 1 before the modulo stuff
def reportBattery():
    controllerRows = 3 # well, not this magic number
    global batteryReports
    batteryReports += 1
    if (batteryReports % controllerRows) + 1 == 1: # reports mod rows == 0 works too but for the sake of readability
        controller_1.screen.clear_screen()
    controller_1.screen.set_cursor((batteryReports % controllerRows) + 1, 1)
    controller_1.screen.print("brain's at ", brain.battery.capacity(), "% rn", sep="")

def invertScraper():
    match_load_piston.set(not match_load_piston.value())

def invertDescore():
    descore_piston.set(not descore_piston.value())

def pre_autonomous():
    brain.screen.clear_screen()
    brain.screen.print("pre-autonomous code")
    match_load_piston.set(False)

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    drivetrain.stop()
    match_load_piston.set(False)
    wait(100, MSEC)
    match_load_piston.set(True)
    drivetrain.drive_for(FORWARD, distance=2.64, units=INCHES, velocity=100, units_v=PERCENT)
    drivetrain.turn_for(LEFT, angle=85, units=DEGREES, velocity=50, units_v=PERCENT)

    intake_motors.spin(FORWARD)
    wait(500, MSEC)
    drivetrain.drive_for(FORWARD, distance=0.7, units=INCHES, velocity=1000, units_v=PERCENT)
    wait(1500, MSEC)
    intake_motors.stop(BRAKE)
"""
    drivetrain.drive_for(REVERSE, distance=0.1, units=INCHES, velocity=100, units_v=PERCENT)
    match_load_piston.set(False)
    drivetrain.turn_for(RIGHT, angle=175, units=DEGREES, velocity=50, units_v=PERCENT)
    drivetrain.drive(FORWARD, velocity=100, units=PERCENT)
    wait(3000, MSEC)
    # drivetrain.drive_for(FORWARD, distance=1.575, units=INCHES, velocity=100, units_v=PERCENT)
    motor_intake3.spin(FORWARD)
    drivetrain.stop(BRAKE)
    wait(5000, MSEC)"""

def user_control():
    controller_1.screen.clear_screen()
    controller_1.screen.set_cursor(1, 1)
    controller_1.screen.print("Press down D-pad for battery percent... I hope?")
    controller_1.screen.set_cursor(1, 1)

    controller_1.buttonX.pressed(invertScraper) # apparently these don't go in the while loop hahaha
    controller_1.buttonUp.pressed(invertDescore)
    controller_1.buttonDown.pressed(reportBattery)
    while True:
        if controller_1.buttonR1.pressing(): # not happy with all this but I'm scared if I change something it'll bork the drivetrain again
            intake_motors.spin(FORWARD)
        elif controller_1.buttonR2.pressing():
            intake_motors.spin(REVERSE)
        else:
            intake_motors.stop()

        if controller_1.buttonL1.pressing(): # ditto
            motor_intake3.spin(FORWARD)
        elif controller_1.buttonL2.pressing():
            motor_intake3.spin(REVERSE)
        else:
            motor_intake3.stop()

        arcadeDriveLoop(controller_1.axis3.position() ** 2 / 100, controller_1.axis1.position() ** 2 / 100) # left stick Y, right stick X (squared for a nicer curve)

        wait(20, MSEC)  # X CPU overload

comp = Competition(user_control, autonomous)
pre_autonomous()