from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math
from hub import port
from utime import sleep_ms
# Create your objects here.
hub = MSHub()


class Arm:
    def __init__(self):
        self.gripper = Motor('C')
        self.arm = Motor('E') #the highest it goes is  -120
        self.gripperPos = 0
        self.armPos = 0
        
    def setDefault(self):
        #while not self.arm.was_stalled():
            #self.arm.start(50)
        self.arm.set_degrees_counted(0)
        self.updateCurrentPosition()
    def moveDown(self): # the desired delta is 350
        #self.arm.run_to_position(180, 'counterclockwise', 30) #-400 acceptable
        self.arm.run_to_degrees_counted(-290,30)
        self.updateCurrentPosition() 
    def moveUp(self):
        self.arm.run_to_degrees_counted(45,30) 
        #self.arm.run_to_degrees_counted(0,30)
        self.updateCurrentPosition()
    def moveTo(self,x):
        self.arm.run_to_degrees_counted(x,30)
        #self.arm.run_to_degrees_counted(0,30)
        self.updateCurrentPosition()
    def grip(self):#delta is -10
        self.gripper.run_to_position(78,speed=50)
        #self.gripper.run_to_degrees_counted(0,30)
        self.updateCurrentPosition()
    def release(self):
        self.gripper.run_to_position(93,speed=50)
        #self.gripper.run_to_degrees_counted(8,30)
        self.updateCurrentPosition()
    def releaseIntoBeaker(self):
        #self.gripper.run_to_position(205,speed=50)
        self.gripper.run_to_degrees_counted(25,30)
        self.updateCurrentPosition()
    def updateCurrentPosition(self):
        abs_pos = self.arm.get_position() 
        self.armPos = abs_pos
        print("Updated Arm position to: " + str(abs_pos))
        abs_pos = self.gripper.get_position()
        self.gripperPos = abs_pos
        print("Updated Gripper position to: " + str(abs_pos))
    def getCurrentPosition(self):
        print("Absolute Gripper Position: " + str(self.gripperPos))
        print("Absolute Arm Position: " + str(self.armPos))
 
class Base:
    def __init__(self):
        self.wheels = port.A.motor
        self.wheelsPos = 0
    def setDefault(self):
        self.wheels.preset(self.wheels.get()[0])
    def moveForward(self):
        self.wheels.run_to_position(-1200,speed=50)
    def moveBackwards(self):
        self.wheels.run_to_position(0,speed=50)
    def moveToOrigin(self):
        self.wheels.run_to_position(0, speed=50)
    def presetOrigin(self):
        self.wheels.preset(self.wheels.get()[0])
    def moveTo(self, x):
        self.wheels.run_to_position(x,speed=50)
    def updateCurrentPosition(self):
        while self.wheels.busy(1):
            sleep_ms(10)
        abs_pos = self.wheels.getPosition()
        print("Absolute Wheels position: " + str(abs_pos))
    def getCurrentPosition(self):
        print("Absolurte Wheels position " + str(self.wheelsPos))


class Board():
    def __init__(self, arm, base):
        self.coordinates = [[300,0],[600,0],[900,0][1200,0],[1500,0]]
        self.arm = arm
        self.base = base
    def status(self):
        self.arms.getCurrentPosition()
        self.base.getCurrentPosition()
# Write your program here.
hub.speaker.beep()
arms = Arm()
base = Base()
#arms.setDefault()
#arms.moveDown()
#arms.grip()


#arms.setDefault()

debug = True

if debug ==False:
    #arms.setDefault()
    #arms.updateCurrentPosition()
    #base.moveForward()
    #base.moveToOrigin()
    #arms.moveUp()

    arms.moveDown()
    sleep_ms(2000)
    arms.grip()
    sleep_ms(2000)
    arms.moveUp()
    arms.release()

    #print("Final pos " + str(arms.armPos))
    #arms.release()
    #sleep_ms(2000)
    #arms.grip()
    
    #arms.releaseIntoBeaker()
    #sleep_ms(2000)
    #arms.moveUp()
    #sleep_ms(2000)
    base.moveToOrigin()
    #arms.grip()
    #sleep_ms(2000)
    #arms.release()
else:
    arms.moveDown()
    sleep_ms(3000)
    arms.grip()
    sleep_ms(3000)
    arms.moveUp()
    sleep_ms(3000)
    base.moveTo(-1300)
    sleep_ms(5000)
    arms.moveDown()
    sleep_ms(3000)
    arms.release()

    sleep_ms(4000)

    ##Second
    arms.moveUp()
    sleep_ms(3000)
    base.moveTo(-300)
    sleep_ms(3000)
    arms.moveDown()
    sleep_ms(3000)
    arms.grip()
    sleep_ms(3000)
    arms.moveUp()
    sleep_ms(3000)
    base.moveTo(-1460)
    sleep_ms(3000)
    arms.moveDown()
    sleep_ms(3000)
    arms.release()
    sleep_ms(3000)
    arms.moveUp()
    sleep_ms(3000)
    base.moveTo(0)




#arm = port.E.motor
#arm.run_to_position(-00,speed=30)
#arms.moveUp()
#arms.moveDown()
#arms.grip()
#arms.arm.run_at_speed(speed=60,stall = True)
#hub.speaker.beep()
#print("done")

MotorA = port.A.motor



#MotorA.mode(2)# set mode to absolute position

#MotorA.preset(MotorA.get()[0])# preset 0 position to absolute zero position

# Turn motors to different positions in parallel
#MotorA.run_to_position(0,speed=30)
#MotorA.run_to_position(0,speed=50)




