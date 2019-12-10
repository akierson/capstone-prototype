# You need to install pyaudio to run this example
# pip install pyaudio

# When using a microphone, the AudioSource `input` parameter would be
# initialised as a queue. The pyaudio stream would be continuosly adding
# recordings to the queue, and the websocket client would be sending the
# recordings to the speech to text service

import pyaudio
import sys
import glob
import random
import serial
import time
from typewriter import Typewriter
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
ARD_PORT = "com4"
QUESTIONS = open("../testCorpus/mood.txt", "r").read().strip()

running = True

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
    time.sleep(3)
except Exception as e:
    print('Serial Error: {}'.format(e))

    ser = None

if ser:
    tp = Typewriter(ser, QUESTIONS)
    tp.write_qtitle()

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

        # Limit corpus to not include so many yeahs
        if transcript[0]['transcript'][0] not in ['%HESITATION', 'yeah']:
            if ser:
                tp.writePrinter('.')
            mGen.add_to_corpus([x for x in transcript[0]['transcript'].split() if x != '%HESITATION'])

        # Make sure corpus long enough - needs at least 17 syllables
        if len(mGen.corpus_noStop) > 20:
            mGen.make_markov_haiku()
            mGen.print_poem()
            if ser:
                tp.writePrinter('\n')
                tp.writePrinter(mGen.poem)
                tp.writePrinter('\n. . . . . . \n     by turkishtypewriter\n\n\n\n\n\n\n\n')
                # Clear corpus for next poem
            time.sleep(120)
            mGen.corpus = []
            mGen.corpus_noStop = []
            mGen.title = ""
            # Delay for x time until people add more paper
            # Reprint Title
            if ser:
                tp.write_qtitle()

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        # Clear Print and allow shit to function
        sys.stdout.flush()

    def on_data(self, data):
        pass

    def on_close(self):
        print("Connection closed")

# this function will initiate the recognize service and pass in the AudioSource
def recognize_using_websocket(*args):
    mcallback = MyRecognizeCallback()
    # Will Run until Stopped
    while running:
        try:
            speech_to_text.recognize_using_websocket(audio=audio_source,
                                             content_type='audio/l16; rate=44100',
                                             recognize_callback=mcallback,
                                             inactivity_timeout = -1,
                                             interim_results=True)
        except Exception as e:
            print('Error Starting Thread: {}'.format(e))

        # To Catch Keyboard Interrupts
        if running:
            print('Connection closed. Restarting in 15 seconds')
            time.sleep(15)


###############################################
#### Prepare the for recording using Pyaudio ##
###############################################

# Variables for recording the speech
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

try:
    recognize_thread = Thread(target=recognize_using_websocket, args=())
    recognize_thread.start()

    while True:
        pass

except KeyboardInterrupt:
    # stop recording
    running = False
    stream.stop_stream()
    stream.close()
    audio.terminate()
    audio_source.completed_recording()
    sys.exit()
