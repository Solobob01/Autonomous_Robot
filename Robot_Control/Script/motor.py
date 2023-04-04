import cv2
import math
import time

TIME_1M = 0.5
TIME_180D = 0.75

FIRST_BOTTLE_X_THR = 280
SECOND_BOTTLE_X_THR = 360

WAKE_UP = True
FIRST_BOTTLE = False
SECOND_BOTTLE = False
THIRD_BOTTLE = False

def setMotorPower(GPG, powerLeft = 0, powerRight = 0):
    GPG.set_motor_power(GPG.MOTOR_LEFT, powerLeft)
    GPG.set_motor_power(GPG.MOTOR_RIGHT, powerRight)

def D2T(degrees):
    return (degrees * TIME_180D / 180)

def M2T(meters):
    return math.floor(meters * TIME_1M)

#left 1
#right 0
def rotateMotorDegrees(GPG, direction, degrees):
    if direction == 1:
        setMotorPower(GPG, -100, 100)
    else:
        setMotorPower(GPG, 100, -100)
    time.sleep(D2T(degrees))
    setMotorPower(GPG, 0, 0)

#front 1
#back 0
def moveMotorMeters(GPG, direction, meters):
    if direction == 1:
        setMotorPower(GPG, 100, 100)
    else:
        setMotorPower(GPG, -100, -100)
    time.sleep(3)
    setMotorPower(GPG, 0, 0)


def searchForSecondBottle(GPG, closestBottle):
    global SECOND_BOTTLE
    x, y, w, h = closestBottle
    setMotorPower(GPG, -40, 40)
    if x + w <= FIRST_BOTTLE_X_THR and x + w >= 100:
        SECOND_BOTTLE = True

def checkDodgeSecondBottle(GPG, closestBottle):
    global SECOND_BOTTLE, THIRD_BOTTLE
    x, y, w, h = closestBottle
    if x == -1 and y == -1:
        setMotorPower(GPG, -40, 40)
    elif x != -1 and y !=-1:


def checkDodgeFirstBottle(GPG, closestBottle):
    global FIRST_BOTTLE, SECOND_BOTTLE
    x, y, w ,h = closestBottle
    print("Walking first bottle: X: " + str(x) + " Y: " + str(y))
    setMotorPower(GPG, 75, 75)
    print("Distance: " + str(12 * 100 * 5 / h))
    if x == -1 and y == -1:
        #a disparut sticla
        time.sleep(2)
        FIRST_BOTTLE = False
        SECOND_BOTTLE = True
        setMotorPower(GPG, 0, 0)
        time.sleep(0.5)

def controlAutonomous(GPG, closestBottle):
    global WAKE_UP, FIRST_BOTTLE, SECOND_BOTTLE
    print(closestBottle)
    x, y, w, h = closestBottle
    print("X: " + str(x + w) + " Y: " + str(y))
    if WAKE_UP == True:
        onWakeUp(GPG, closestBottle)
    elif FIRST_BOTTLE == True:
        checkDodgeFirstBottle(GPG, closestBottle)
    elif SECOND_BOTTLE == True:
        print("Cautam a doua sticla!")
    key = cv2.waitKey(1) & 0XFF
    if key == ord('q'):
        setMotorPower(GPG, 0, 0)
        return 0

def onWakeUp(GPG, closestBottle):
    global WAKE_UP, FIRST_BOTTLE
    x, y, w, h = closestBottle
    #print("Rotate X: " + str(x) + " Y: " + str(y))
    setMotorPower(GPG, -40, 40)
    if x  + w <= FIRST_BOTTLE_X_THR and x + w >= 100:
        WAKE_UP = False
        FIRST_BOTTLE = True
        setMotorPower(GPG, 0, 0)
        time.sleep(0.5)


def controlRobotWithKeyboard(GPG):
    key = cv2.waitKey(1) & 0XFF
    if key == ord('w'):
        GPG.set_motor_power(GPG.MOTOR_LEFT + GPG.MOTOR_RIGHT, 100)
    elif key == ord('s'):
        GPG.set_motor_power(GPG.MOTOR_LEFT + GPG.MOTOR_RIGHT, -100)
    elif key == ord('a'):
        GPG.set_motor_power(GPG.MOTOR_LEFT, -100)
        GPG.set_motor_power(GPG.MOTOR_RIGHT, 100)
    elif key == ord('d'):
        GPG.set_motor_power(GPG.MOTOR_RIGHT, -100)
        GPG.set_motor_power(GPG.MOTOR_LEFT, 100)
    elif key == ord('e'):
        GPG.set_motor_power(GPG.MOTOR_RIGHT, 0)
        GPG.set_motor_power(GPG.MOTOR_LEFT, 0)
    elif key == ord('q'):
        return 0
    return 1