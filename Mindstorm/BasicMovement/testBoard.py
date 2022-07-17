import os 
import math 
from mindstorms import Motor

class Arm:
    def __init__(self):
        #self.gripper = Motor('C')
        #self.arm = Motor('E') #the highest it goes is  -120
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
        #self.wheels = port.A.motor
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
        
        self.arm = arm
        self.base = base
        self.peripherals = []
    def status(self):
        self.arms.getCurrentPosition()
        self.base.getCurrentPosition()
    def load_labwear(self, name, location, numLots = 5, lotSize = None, taken = [],size = 0):
    #fix this the following way https://stackoverflow.com/questions/5079609/methods-with-the-same-name-in-one-class-in-python
        if name == 'MetalHolder':
            metalHolder = self.MetalHolder(location, numLots, lotSize, taken) # generate an empty array of 0 be default
            self.peripherals.append(metalHolder)
        if name == 'Beaker':
            beaker = self.Beaker(size, location)
            self.peripherals.append(beaker)
    def performExperiment(self, name):
        metalHolder1 = self.peripherals[0]
        beaker = self.peripherals[1]
        metalHolder2 = self.peripherals[2]
        self.arm.moveDown()
        sleep_ms(3000)
        self.arm.arms.grip()
        sleep_ms(3000)
        self.arm.moveUp()
        sleep_ms(3000)
        self.base.moveTo(beaker.start)
        sleep_ms(5000)
        self.arms.moveDown()
        sleep_ms(3000)
        #perform water logic...
        self.arm.moveUp()
        sleep_ms(3000)
        self.base.moveTo(self.MetalHolder.findFreeLot())
        sleep_ms(3000)
        self.arms.moveDown()
        
        pourLiquid()

    class Beaker():
        sizeOptions = [[30,40], [50,60]] #comes in as [height, radius]
        def __init__(self, size, location):
            self.size = self.sizeOptions[size]
            self.start = location
            self.end = location +size
        def changeSize(size):
            self.size = self.sizeOptions[size]


    class MetalHolder():

        
        def __init__(self, start, numLots, lotSize, taken):
            self.start = start
            self.numLots = numLots
            self.lotSize = lotSize
            self.coordinates = []
            self.generateLocation(start) # array of x and y coordiates of the spots in the holder
            self.taken = taken # array of taken spots of the holder

            
        def updateLot(self, idx, status=1):
            taken[idx] = status
        def status():
            for x,status in zip([x for x,y in self.coordinates], self.taken):
                print("The point with coordinates " + str(x) + " has status " + str(status))
        def findFreeLot():
            for count, coord in enumerate(self.coordinates):
                if not self.taken[count]:
                    x, y = coordinates
                    updateLot(count)
                    return x
            return None
        def findTaken():
            for count, coord in enumerate(self.coordinates):
                if self.taken[count]:
                    x, y = coordinates
                    updateLot(count,0)
                    return x
        def generateLocation(self, start):            
            y = 0
            x = start
            for i in range(self.numLots):
                print(i, self.lotSize)
                x += self.lotSize
                self.coordinates.append([x,y])
    class LiquidHandler():
        def __init__(self):
            pass
arm = Arm()
base = Base()
board = Board(arm, base)

board.load_labwear('MetalHolder', location = 5, lotSize = 30)
print(board.peripherals[0].coordinates)
board.performExperiment("fdf")