import serial
import time
import random

class Typewriter(object):
    """docstring for Typewriter."""

    def __init__(self, ser, questions):
        super(Typewriter, self).__init__()
        self.carriage_pos = 0
        self.ser = ser
        self.questions = questions.split('?')

    def writePrinter(self, string):
        print('to Typewriter:', string)
        if self.ser:
            try:
                if not self.ser.isOpen():
                    try:
                        self.ser.open()
                    except Exception as e:
                        print("Error Reopening Port:", e)
                # Check max string length
                for i in string:
                    self.ser.write(i.encode('ascii'))
                    self.carriage_pos = self.carriage_pos + 1
                    time.sleep(.2)
                    if i == '\n':
                        self.carriage_pos = 0
                        time.sleep(.3)
                    if self.carriage_pos > 50 and i == " ":
                        self.ser.write('\n'.encode('ascii'))
                        time.sleep(.3)
                        self.ser.write(' '.encode('ascii'))
                        time.sleep(.2)
                        self.ser.write(' '.encode('ascii'))
                        time.sleep(.2)
                        self.ser.write(' '.encode('ascii'))
                        time.sleep(.2)
                        self.carriage_pos = 3
            except Exception as e:
                print(e)

    def write_qtitle(self):
        questions = random.choice(self.questions).strip().lower()
        print(questions)

        self.writePrinter(questions)
        # Moves title into view
        self.writePrinter('\n\n\n\n\n\n\n\n\n')
