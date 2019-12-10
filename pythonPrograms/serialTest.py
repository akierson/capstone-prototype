import serial
import time

ser = serial.Serial('com4', 9600)

time.sleep(5)
for i in 'turkishtypewriter\n\none. read the prompt and expound upon it in a vocal manner\ntwo. once twenty five dollar words have been recorded\n      a poem is produced\nthree. take poem and replace paper\n\nplease be patient\n\nby azariah kierson galeano':

    ser.write(i.encode('ascii'))
    if i == '\n':
        time.sleep(.3)
    print(i)
    print(i.encode('ascii'))
    time.sleep(.3)

ser.close()
