import serial
import time

ser = serial.Serial('com4', 9600)

while True:
    ser.write(1)
    print('on')
    time.sleep(1)

    ser.write(0)
    print('off')
    time.sleep(1)

ser.close()
