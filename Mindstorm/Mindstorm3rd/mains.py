import os 
import math 
from mindstorms import Motor, Hub
import time
#from ComArduino import LiquidHandler

hub = Hub()

class Arm:
    def __init__(self):
        self.gripper = hub.port.C.motor
        self.arm = hub.port.E.motor #the highest it goes is  -120
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
      
        #self.arm.run_to_degrees_counted(45,30) 
        self.arm.run_for_degrees(20)
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
        self.wheels = hub.port.A.motor
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
            time.sleep(10)
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
        time.sleep(3000)
        self.arm.arms.grip()
        time.sleep(3000)
        self.arm.moveUp()
        time.sleep(3000)
        self.base.moveTo(beaker.start)
        time.sleep(5000)
        self.arms.moveDown()
        time.sleep(3000)
        #perform water logic...
        self.arm.moveUp()
        time.sleep(3000)
        self.base.moveTo(self.MetalHolder.findFreeLot())
        time.sleep(3000)
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
        def pourLiquid(self,testData):
            ComArduino.runTest(testData)
            
arms = Arm()
base = Base()
board = Board(arms, base)

#board.load_labwear('MetalHolder', location = 5, lotSize = 30)
#board.load_labwear('Beaker', size = 1, location = 30)
#board.load_labwear('MetalHolder', location = 5, lotSize = 30)
#print(board.peripherals[0].coordinates)
#board.performExperiment("fdf")


#arms.setDefault()

debug = False

if debug ==False:
    
    #arms.setDefault()
    #arms.updateCurrentPosition()
    #base.moveForward()
    #base.moveToOrigin()
    #arms.moveUp()

    #arms.moveDown()
    #time.sleep(2000)
    #arms.grip()
    #time.sleep(2000)
    arms.moveUp()
    #time.sleep(2000)
    #base.moveTo(-2200)    2200 for the first lot
    #time.sleep(6000)
    #arms.moveDown()
    #time.sleep(2000)
    #arms.release()
    #arms.grip()
    #time.sleep(2000)

    #base.moveTo(0)
 
    #base.moveTo(0)
    #print("Final pos " + str(arms.armPos))
    #arms.release()
    #time.sleep(2000)
    #arms.grip()
    
    #arms.releaseIntoBeaker()
    #time.sleep(2000)
    #arms.moveUp()
    #time.sleep(2000)
    #base.moveToOrigin()
    #arms.grip()
    #time.sleep(2000)
    #arms.release()
else:
    arms.moveDown()
    time.sleep(3000)
    arms.grip()
    time.sleep(3000)
    arms.moveUp()
    time.sleep(3000)
    base.moveTo(-1300)
    time.sleep(5000)
    arms.moveDown()
    time.sleep(3000)
    arms.release()

    time.sleep(4000)

    ##Second
    arms.moveUp()
    time.sleep(3000)
    base.moveTo(-300)
    time.sleep(3000)
    arms.moveDown()
    time.sleep(3000)
    arms.grip()
    time.sleep(3000)
    arms.moveUp()
    time.sleep(3000)
    base.moveTo(-1460)
    time.sleep(3000)
    arms.moveDown()
    time.sleep(3000)
    arms.release()
    time.sleep(3000)
    arms.moveUp()
    time.sleep(3000)
    base.moveTo(0)
