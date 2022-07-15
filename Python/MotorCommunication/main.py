import serial
import time
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    arduino.write(bytes("3434", 'utf-8'))
    arduino.write(bytes("dfdfd", 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
def write_speed(motorNum, pumpAmount, motorSpeed):
    arduino.write(bytes(motorNum, 'utf-8'))
    arduino.write(bytes(pumpAmount, 'utf-8'))
    arduino.write(bytes(motorSpeed, 'utf-8'))
while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    print(value) # printing the value


def sendPumpLiquid(num, amount):
    pass 
