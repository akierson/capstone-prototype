# You need to install pyaudio to run this example
# pip install pyaudio

# When using a microphone, the AudioSource `input` parameter would be
# initialised as a queue. The pyaudio stream would be continuosly adding
# recordings to the queue, and the websocket client would be sending the
# recordings to the speech to text service

import pyaudio
import time
import sys
import glob
import serial
import random
import MarkovPoemGenerator as mpg
import speech_recognition as sr
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# For different versions
try:
    from Queue import Queue, Full
except ImportError:
    from queue import Queue, Full

# Imported Files
IBM_KEY = open("../keys/ibm-credentials.txt", "r").read().strip()
ARD_PORT = "COM4"
QUESTIONS = open("../testCorpus/mood.txt", "r").read().strip()

# Keep Track of states
HAS_TITLE = False
POEM_PRINTED = False

# Write a question from An Interogative Mood: A Novel?
# TODO: Needs Shorter Questions
def write_qtitle(ser):
    questions = random.choice(QUESTIONS.split('?')).strip().lower()
    print(questions)

    writePrinter(questions, ser)
    # Moves title into view
    writePrinter('\n\n\n\n\n\n\n\n', ser)

def writePrinter(string, ser):
    if ser:
        try:
            if not ser.isOpen():
                try:
                    ser.open()
                except Exception as e:
                    print("Error Reopening Port:", e)
            # Check max string length
            car_pos = 0
            for i in string:
                ser.write(i.encode('ascii'))
                car_pos = car_pos + 1
                time.sleep(.2)
                if i == '\n':
                    car_pos = 0
                    time.sleep(.5)
                if car_pos > 50 and i == " ":
                    ser.write('\n'.encode('ascii'))
                    time.sleep(.2)
                    ser.write(' '.encode('ascii'))
                    time.sleep(.2)
                    ser.write(' '.encode('ascii'))
                    time.sleep(.2)
                    ser.write(' '.encode('ascii'))
                    time.sleep(.2)
                    car_pos = 3
        except Exception as e:
            print(e)

###############################################
#### Initalize queue, classes to store the recordings ##
###############################################
CHUNK = 2048
# Note: It will discard if the websocket client can't consumme fast enough
# So, increase the max size as per your choice
BUF_MAX_SIZE = CHUNK * 10
# Buffer to store audio
q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))

# Create an instance of AudioSource
audio_source = AudioSource(q, True, True)

mGen = mpg.MarkovPoemGenerator()

# Initialize Serial
try:
    ser = serial.Serial(ARD_PORT, 9600)
    time.sleep(2)
except Exception as e:
    print('Error: Input port not available')
    ser = None

write_qtitle(ser)

###############################################
####### Prepare Speech to Text Service ########
###############################################

# initialize speech to text service
authenticator = IAMAuthenticator(IBM_KEY)
speech_to_text = SpeechToTextV1(authenticator=authenticator)

# define callback for the speech to text service
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        print(transcript[0]['transcript'])
        writePrinter('. ', ser)
        mGen.add_to_corpus([x for x in transcript[0]['transcript'].split() if x != '%HESITATION'])
        if len(mGen.corpus_noStop) > 20:
            mGen.make_markov_haiku()
            mGen.print_poem()
            if ser:
                writePrinter('\n', ser)
                writePrinter(mGen.poem, ser)
                writePrinter('\n. . . . . . ', ser)
                writePrinter('\n     by turkishtypewriter\n\n\n\n\n\n\n\n', ser)
                POEM_PRINTED = True
                # Clear corpus for next poem
            mGen.corpus = []
            mGen.corpus_noStop = []
            mGen.title = ""
            # Delay for x time until people add more paper
            time.sleep(45)
            # Reprint Title
            write_qtitle(ser)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        sys.stdout.flush()

    def on_data(self, data):
        pass

    def on_close(self):
        print("Connection closed")
        # TODO: Check if mGen.corpus has info
        # TODO: Add Close option from Arduino

# this function will initiate the recognize service and pass in the AudioSource
def recognize_using_websocket(*args):
    mcallback = MyRecognizeCallback()
    # Will Run until Stopped
    while True:
        speech_to_text.recognize_using_websocket(audio=audio_source,
                                             content_type='audio/l16; rate=44100',
                                             recognize_callback=mcallback,
                                             interim_results=True)
        print('Connection closed. Restarting in 30 seconds')
        time.sleep(30)


###############################################
#### Prepare the for recording using Pyaudio ##
###############################################

# Variables for recording the speech
THRESHOLD = 200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# define callback for pyaudio to store the recording in queue
def pyaudio_callback(in_data, frame_count, time_info, status):
    try:
        q.put(in_data)
    except Full:
        pass # discard
    return (None, pyaudio.paContinue)

# instantiate pyaudio
audio = pyaudio.PyAudio()

# open stream using callback
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
    stream_callback=pyaudio_callback,
    start=False
)

#########################################################################
#### Start the recording and start service to recognize the stream ######
#########################################################################

print("Enter CTRL+C to end recording...")
stream.start_stream()

# TODO: Set THRESHOLD

try:
    recognize_thread = Thread(target=recognize_using_websocket, args=())
    recognize_thread.start()

    while True:
        pass

except KeyboardInterrupt:
    # stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    audio_source.completed_recording()
    sys.exit()
