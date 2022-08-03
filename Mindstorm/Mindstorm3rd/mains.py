import os 
import math 
from mindstorms import Motor, Hub
import time
from ComArduino import LiquidHandler
import numpy as np

hub = Hub()
time.sleep(1)
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
        self.arm.run_for_degrees(220, speed=-30)
        #self.updateCurrentPosition() 
    def moveUp(self):
      
        #self.arm.run_to_degrees_counted(45,30) 
        self.arm.run_for_degrees(-225, speed=30)
        #self.arm.run_to_degrees_counted(0,30)
        #self.updateCurrentPosition()
    def moveTo(self,x):
        self.arm.run_to_degrees_counted(x,30)
        #self.arm.run_to_degrees_counted(0,30)
        self.updateCurrentPosition()
    def grip(self):#delta is -10
        #self.gripper.run_to_position(78,speed=50)
        self.gripper.run_for_degrees(40,30)
        #self.updateCurrentPosition()
    def release(self):
        #self.gripper.run_to_position(93,speed=50)
        self.gripper.run_for_degrees(-40,-30)
        #self.updateCurrentPosition()
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
    def load_labwear(self, name, locationStart=0, numLots = 3, lotSize = 300, taken = [],size = 0):
    #fix this the following way https://stackoverflow.com/questions/5079609/methods-with-the-same-name-in-one-class-in-python
        if name == 'MetalHolder':
            metalHolder = self.MetalHolder(locationStart, numLots, taken = taken, lotSize = -lotSize) # generate an empty array of 0 be default
            self.peripherals.append(metalHolder)
        if name == 'Beaker':
            beaker = self.Beaker(size, locationStart)
            self.peripherals.append(beaker)

    def encoder():
        #assume that first is the metal holder, second beaker, and third metal holder
        metalHolder1 = self.peripherals[0]
        beaker = self.peripherals[1]
        metalHolder2 = self.peripherals[2]
        #check if there is enough space for metal pieces from holder1 in holder2 
        if np.count_nonzero(metalHolder1.taken) <= np.count_nonzero(np.array(metalHolder2.taken)==0):
            for i in range(len(np.count_nonzero(metalHolder1.taken))):
                #this is always true for the picking up 1 part
                lotIdx = metalHolder1.findFreeLot()
                self.base.moveTo(lotIdx) 
                self.arms.moveDown() 
                arms.grip()
                arms.moveUp()
                #end of pickup 
                #moving to the beaker
                self.base.moveTo(beaker.start)
                self.moveDown()
                self.moveDown()
                #end of beakerDip
                #this is always true for releaseing 1 part 
                lotIdx = metalHolder2.findFreeLot()
                self.base.moveTo(lotIdx) 
                self.arms.moveDown() 
                arms.release()
                arms.moveUp()
                #end of release
        else:
            print("The number of metals you are trying to transport is too big")

    class Beaker():
        sizeOptions = [[30,40], [50,60]] #comes in as [height, radius]
        def __init__(self, size, location):
            self.size = self.sizeOptions[size]
            self.start = location
            self.end = location +size
        def changeSize(size):
            self.size = self.sizeOptions[size]


    class MetalHolder():

        
        def __init__(self, locationStart, numLots, taken = [], lotSize = -300):
            self.start = locationStart
            self.numLots = numLots
            self.lotSize = lotSize
            self.coordinates = []
            self.generateLocation(locationStart) # array of x and y coordiates of the spots in the holder
            self.taken = taken # array of taken spots of the holder
            print(self.coordinates)
            
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

            
arms = Arm()
base = Base()
board = Board(arms, base)
#liquid = LiquidHandler('COM3',9600)


#testData.append("<2,20,1>")
board.load_labwear('MetalHolder')
#board.load_labwear('Beaker', size = 1, location = 30)
#board.load_labwear('MetalHolder', location = 5, lotSize = 30)
#print(board.peripherals[0].coordinates)
#board.performExperiment("fdf")


#arms.setDefault()

debug = False

if debug ==False:
    

   

    #liquid.runTest(testData)
    #testData = []
    #testData.append("<1,2,1>")
    #testData.append("<2,2,1>")
    #liquid.runTest(testData)
    #arms.setDefault()
    #arms.updateCurrentPosition()
    #base.moveForward()
    #base.moveToOrigin()
    #arms.moveUp()
    
    #arms.release()
    #time.sleep(2)
    #arms.grip()
    #liquid.runTest(testData)

    #arms.moveUp()
    #arms.grip()
    #arms.release()
    #base.moveTo(-2000)
    #time.sleep(5)
    #base.moveTo(-100)
    #time.sleep(2)

    #Testing going down and up
    #arms.moveDown()
    #time.sleep(2)
    #arms.grip()
    #time.sleep(2)
    #arms.release()
    #time.sleep(2)
    #arms.moveUp()


    #arms.moveUp()
    #arms.release()
    #time.sleep(2)
    #arms.moveDown()
    #time.sleep(2)
    #arms.grip()
    #liquid.runTest(testData)
    #arms.moveUp()
    
   
    """
    
    time.sleep(2)
    arms.moveDown()
    time.sleep(2)
    arms.grip()
    time.sleep(2)
    arms.moveUp()
    time.sleep(2)
    base.moveTo(-1400)    #2200 for the first lot
    time.sleep(3)
    arms.moveDown()
    time.sleep(2)
    liquid.runTest(testData)
    time.sleep(10)
    arms.moveUp()
    time.sleep(2)
    base.moveTo(-2080)
    time.sleep(3)
    arms.moveDown()
    time.sleep(3)
    arms.release()
    time.sleep(3)
    arms.moveUp()
    time.sleep(3)
    base.moveTo(-300)
    time.sleep(4)
    arms.moveDown()
    time.sleep(2)
    arms.grip()
    time.sleep(2)
    arms.moveUp()
    time.sleep(2)
    base.moveTo(-1400)    #2200 for the first lot
    time.sleep(10)
    arms.moveDown()
    time.sleep(2)
    liquid.runTest(testData)
    time.sleep(2)
    arms.moveUp()
    time.sleep(2)
    base.moveTo(-2300)
    time.sleep(2)
    arms.moveDown()
    time.sleep(2)
    arms.release()
    arms.moveUp()
    """
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
