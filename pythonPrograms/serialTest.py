import serial
import time

#
# class ArduinoWriter(object):
#     """docstring for ArduinoWriter."""
#
#     def __init__(self, com='com7', speed=0.1, baud=9600):
#         super(ArduinoWriter, self).__init__()
#         self.com = com
#         self.baud = 9600


ser = serial.Serial('com5', 9600)


time.sleep(5)
for i in 'this is a test':

    ser.write(i.encode('ascii'))
    print(i)
    print(i.encode('ascii'))
    time.sleep(.1)

ser.close()
