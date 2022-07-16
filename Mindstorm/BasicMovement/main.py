from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math
from hub import port
from utime import sleep_ms
import ubluetooth
# Create your objects here.
hub = MSHub()


# wrapper for ubluetooth module (HM-10 specific implementation)
class BLEHandler:

    def __init__(self):
        # constants
        self.__IRQ_SCAN_RESULT = const(1 << 4)
        self.__IRQ_SCAN_COMPLETE = const(1 << 5)
        self.__IRQ_PERIPHERAL_CONNECT = const(1 << 6)
        self.__IRQ_PERIPHERAL_DISCONNECT = const(1 << 7)
        self.__IRQ_GATTC_SERVICE_RESULT = const(1 << 8)
        self.__IRQ_GATTC_CHARACTERISTIC_RESULT = const(1 << 9)
        self.__IRQ_GATTC_DESCRIPTOR_RESULT = const(1 << 10)
        self.__IRQ_GATTC_READ_RESULT = const(1 << 11)
        self.__IRQ_GATTC_NOTIFY = const(1 << 13)

        # used to enable notifications
        self.__NOTIFY_ENABLE = const(1)

        # enter device specific service and characteristic UUIDs (from nRF Connect app)
        # the service and characteristic UUIDs below are for the HM-10 BluetoothLE module
        self.__PERIPHERAL_SERVICE_UUID = ubluetooth.UUID(0xFFE0)
        self.__PERIPHERAL_SERVICE_CHAR = ubluetooth.UUID(0xFFE1)
        # enter peripheral device ID here
        self.__DEVICE_ID = b'\x00\x00\x00\x00\x00\x00'

        # class specific
        self.__ble = ubluetooth.BLE()
        self.__ble.active(True)
        self.__ble.irq(handler=self.__irq)
        self.__decoder = Decoder()
        self.__reset()

    def __reset(self):
        # cached data
        self.__addr = None
        self.__addr_type = None
        self.__adv_type = None
        self.__services = None
        self.__man_data = None
        self.__name = None
        self.__conn_handle = None
        self.__value_handle = None

        # reserved callbacks
        self.__scan_callback = None
        self.__read_callback = None
        self.__notify_callback = None
        self.__connected_callback = None
        self.__disconnected_callback = None

    # start scan for ble devices
    def scan_start(self, timeout, callback):
        self.__scan_callback = callback
        self.__ble.gap_scan(timeout, 30000, 30000)

    # stop current scan
    def scan_stop(self):
        self.__ble.gap_scan(None)

    # write gatt client data
    def write(self, data, adv_value=None):
        if not self.__is_connected():
            return
        if adv_value:
            #self.__ble.gattc_write(self.__conn_handle, adv_value, data)
            self.__ble.gattc_write(self.__conn_handle, adv_value, struct.pack("<h", int(data)))
        else:
            #self.__ble.gattc_write(self.__conn_handle, self.__value_handle, data)
            self.__ble.gattc_write(self.__conn_handle, self.__value_handle, struct.pack("<h", int(data)))

        print("Data Written")
        print(data)

    # read gatt client
    def read(self, callback):
        if not self.__is_connected():
            return
        print("Read requested...")
        self.__read_callback = callback
        print("Read callback set")
        self.__ble.gattc_read(self.__conn_handle, self.__value_handle)
        print("Read initiated")

    # connect to ble device
    def connect(self, addr_type, addr):
        self.__ble.gap_connect(addr_type, addr)

    # disconnect from ble device
    def disconnect(self):
        if not self.__is_connected():
            return
        self.__ble.gap_disconnect(self.__conn_handle)
        self.__reset()

    # get notification
    def on_notify(self, callback):
        self.__notify_callback = callback

    # get callback on connect
    def on_connect(self, callback):
        self.__connected_callback = callback

    # get callback on connect
    def on_disconnect(self, callback):
        self.__disconnected_callback = callback

    # +-------------------+
    # | Private Functions |
    # +-------------------+

    # ble event handler
    def __irq(self, event, data):
        # called for every result of a ble scan
        if event == self.__IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            print(ubinascii.hexlify(addr))
            print(self.__decoder.decode_services(adv_data), addr_type)
            if ubinascii.hexlify(self.__DEVICE_ID) == ubinascii.hexlify(addr):
                print("Device found")
                self.__addr_type = addr_type
                self.__addr = bytes(addr)
                self.__adv_type = adv_type
                self.__name = self.__decoder.decode_name(adv_data)
                print("Name=" + self.__name)
                self.__services = self.__decoder.decode_services(adv_data)
                print("Getting services")
                self.__man_data = self.__decoder.decode_manufacturer(adv_data)
                print("Getting manufacturer details")
                self.scan_stop()

        # called after a ble scan is finished
        elif event == self.__IRQ_SCAN_COMPLETE:
            if self.__addr:
                if self.__scan_callback:
                    self.__scan_callback(self.__addr_type, self.__addr, self.__man_data)
                self.__scan_callback = None
            else:
                self.__scan_callback(None, None, None)

        # called if a peripheral device is connected
        elif event == self.__IRQ_PERIPHERAL_CONNECT:
            print("Device connected")
            conn_handle, addr_type, addr = data
            self.__conn_handle = conn_handle
            self.__ble.gattc_discover_services(self.__conn_handle)

        # called if a peripheral device is disconnected
        elif event == self.__IRQ_PERIPHERAL_DISCONNECT:
            conn_handle, _, _ = data
            self.__disconnected_callback()
            if conn_handle == self.__conn_handle:
                self.__reset()

        # called if a service is returned
        elif event == self.__IRQ_GATTC_SERVICE_RESULT:
            print("Getting service")
            conn_handle, start_handle, end_handle, uuid = data
            print(uuid)
            if conn_handle == self.__conn_handle and uuid == self.__PERIPHERAL_SERVICE_UUID:
                print("Found service")
                self.__ble.gattc_discover_characteristics(self.__conn_handle, start_handle, end_handle)

        # called if a characteristic is returned
        elif event == self.__IRQ_GATTC_CHARACTERISTIC_RESULT:
            print("Getting characteristic")
            conn_handle, def_handle, value_handle, properties, uuid = data
            print(uuid)
            if conn_handle == self.__conn_handle and uuid == self.__PERIPHERAL_SERVICE_CHAR:
                print("Found characteristic")
                self.__value_handle = value_handle
                # finished discovering, connecting finished
                self.__connected_callback()
                # set notifications to true
                #self.__ble.gattc_write(conn_handle, 49, struct.pack('<h', self.__NOTIFY_ENABLE), 1)

        # called if a descriptor is returned
        elif event == self.__IRQ_GATTC_DESCRIPTOR_RESULT:
            print("Getting descriptor")
            conn_handle, dsc_handle, uuid = data
            print(conn_handle)
            print(dsc_handle)
            print(uuid)

        # called if data was successfully read
        elif event == self.__IRQ_GATTC_READ_RESULT:
            print("Read result received")
            conn_handle, value_handle, char_data = data
            print(char_data)
            if self.__read_callback:
                self.__read_callback(char_data)

        # called if a notification appears
        elif event == self.__IRQ_GATTC_NOTIFY:
            print("Notify event raised")
            conn_handle, value_handle, notify_data = data
            if self.__notify_callback:
                self.__notify_callback(notify_data)

    # connection status
    def __is_connected(self):
        return self.__conn_handle is not None

# helper class to decode ubluetooth data elements
class Decoder:

    def __init__(self):
        self.__COMPANY_IDENTIFIER_CODES = {"4d48": "DSD Tech"}

    def decode_manufacturer(self, payload):
        man_data = []
        n = self.__decode_field(payload, const(0xFF))
        if not n:
            return []
        company_identifier = ubinascii.hexlify(struct.pack('<h', *struct.unpack('>h', n[0])))
        print("Identifier=" + company_identifier.decode())
        company_name = self.__COMPANY_IDENTIFIER_CODES.get(company_identifier.decode(), "?")
        print("Company Name=" + company_name)
        company_data = n[0][2:]
        man_data.append(company_identifier.decode())
        man_data.append(company_name)
        man_data.append(company_data)
        return man_data

    def decode_name(self, payload):
        n = self.__decode_field(payload, const(0x09))
        return str(n[0], "utf-8") if n else "Parsing failed!"

    def decode_services(self, payload):
        services = []
        for u in self.__decode_field(payload, const(0x3)):
            services.append(ubluetooth.UUID(struct.unpack("<h", u)[0]))
        for u in self.__decode_field(payload, const(0x5)):
            services.append(ubluetooth.UUID(struct.unpack("<d", u)[0]))
        for u in self.__decode_field(payload, const(0x7)):
            services.append(ubluetooth.UUID(u))
        return services

    def __decode_field(self, payload, adv_type):
        i = 0
        result = []
        while i + 1 < len(payload):
            if payload[i + 1] == adv_type:
                result.append(payload[i + 2: i + payload[i] + 1])
            i += 1 + payload[i]
        return result

# wrapper for a Bluetooth peripheral
class BLEPeripheral:

    def __init__(self):
        # constants

        # class specific
        self.__handler = BLEHandler()

        # callbacks
        self.__connect_callback = None
        self.__disconnect_callback = None

        self.__move_data = None

    def connect(self, timeout=3000):
        self.__handler.on_connect(callback=self.__on_connect)
        self.__handler.on_disconnect(callback=self.__on_disconnect)
        self.__handler.on_notify(callback=self.__on_notify)
        self.__handler.scan_start(timeout, callback=self.__on_scan)

    def disconnect(self):
        self.__handler.disconnect()

    def read(self, callback):
        self.__handler.read(callback)

    def write(self, data):
        self.__handler.write(data)

    def on_button(self, callback):
        self.__button_callback = callback

    def on_connect(self, callback):
        self.__connect_callback = callback

    def on_disconnect(self, callback):
        self.__disconnect_callback = callback

    def is_connected(self):
        return self.__handler.__is_connected()

    def getMoveData(self):
        return self.__move_data

    def resetMoveData(self):
        self.__move_data = None

    # +-------------------+
    # | Private Functions |
    # +-------------------+

    # callback for scan result
    def __on_scan(self, addr_type, addr, man_data):
        self.__handler.connect(addr_type, addr)

    def __on_connect(self):
        if self.__connect_callback:
            self.__connect_callback()

    def __on_disconnect(self):
        if self.__disconnect_callback:
            self.__disconnect_callback()

    def __on_notify(self, data):
        print("Data received=")
        print(data)
        if data != b'\x00':
            self.__move_data = data
            print("Move data saved")

def on_connect():
    hub.status_light.on("azure")

def on_disconnect():
    hub.status_light.on("white")


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
    def __init__(self, arm, base, peripherals):
        
        self.arm = arm
        self.base = base
        self.peripherals = []
    def status(self):
        self.arms.getCurrentPosition()
        self.base.getCurrentPosition()
    def load_labwear(self, name, location, lotSize, taken)
    #fix this the following way https://stackoverflow.com/questions/5079609/methods-with-the-same-name-in-one-class-in-python
        if name == 'MetalHolder':
            metalHolder = MetalHolder(location, lotSize, taken) # generate an empty array of 0 be default
        if name == 'Beaker':
            beaker = Beaker(size, location)

class Beaker():
    sizeOptions = [[30,40], [50,60]] #comes in as [height, radius]
    def __init__(self, size, location):
        self.size = self.sizeOptions[size]

class MetalHolder():

    
    def __init__(self, coordinates, taken, lotSize, numLots):
        self.coordinates = coordinates # array of x and y coordiates of the spots in the holder
        self.taken = taken # array of taken spots of the holder
        self.lotSize = lotSize
        self.numLots = numLots
    def updateLot(self, idx, status=1):
        taken[idx] = status
    def status():
        for x,status in zip(x for x,y in self.coordinates, self.taken)
            print("The point with coordinates " + str(x) + " has status " + str(status))
    def findFree():
        for count, coord in enumerate(self.coordinates):
            if not self.taken[count]:
                x, y = coordinates
                updateLot(count)
                return x
        break
    def findTaken():
        for count, coord in enumerate(self.coordinates):
            if self.taken[count]:
                x, y = coordinates
                updateLot(count,0)
                return x
    def generateLocation(self, start):            
        y = 0
        x = start
        for i in range(numLots):
            x += self.lotSize
            self.coordinates.append([x,y])



# Write your program here.
hub.speaker.beep()
arms = Arm()
base = Base()
#arms.setDefault()
#arms.moveDown()
#arms.grip()


#arms.setDefault()

debug = False

if debug ==False:
    pass
    #arms.setDefault()
    #arms.updateCurrentPosition()
    #base.moveForward()
    #base.moveToOrigin()
    #arms.moveUp()

    #arms.moveDown()
    #sleep_ms(2000)
    #arms.grip()
    #sleep_ms(2000)
    #arms.moveUp()
    #arms.release()

    #print("Final pos " + str(arms.armPos))
    #arms.release()
    #sleep_ms(2000)
    #arms.grip()
    
    #arms.releaseIntoBeaker()
    #sleep_ms(2000)
    #arms.moveUp()
    #sleep_ms(2000)
    #base.moveToOrigin()
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




#MotorA.mode(2)# set mode to absolute position

#MotorA.preset(MotorA.get()[0])# preset 0 position to absolute zero position

# Turn motors to different positions in parallel
#MotorA.run_to_position(0,speed=30)
#MotorA.run_to_position(0,speed=50)

remote = BLEPeripheral()

# scan for the target device and connect if found
utime.sleep(1)
remote.on_connect(callback=on_connect)
remote.on_disconnect(callback=on_disconnect)
remote.connect()

while remote.is_connected() is not None:
    print("yes")


