# By: Azariah Kierson-Galeano
# 4/12/19
# Using previous and listen_in_background from Speech Recognition
# Made call callable from

import speech_recognition as sr
import datetime
import string

import random
import string
from nltk.corpus import stopwords
from nltk.corpus import cmudict
import MarkovPoemGenerator as mpg

GOOGLE_KEY = ""

d = cmudict.dict()

# Create test phrase for script to match ie change params until phrase x is matched. run 5 times

# Function: callback
# Parms: recognizer is a speech recognizer, audio is the
# Returns: bool
def callback(recognizer, audio):
	# received audio data, now we'll recognize it using Google Speech Recognition
	try:
		r.recognize_google(audio, key=GOOGLE_KEY)
		# Pass variable out
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
		
if __name__ == '__main__':
	mGen = mpg.MarkovPoemGenerator('')
	# Get Text from Speech

	r = sr.Recognizer()
	mic = sr.Microphone()

	#
	with mic as source:
	    audio = r.listen(source)

	textfromspeech = r.recognize_google(audio)

	# Mix is source
	# callback is a function
	r.listen_in_background(mic, callback)
	print(textfromspeech)



	# Run MarkovPoemGenerator

	# now = datetime.datetime.now()
	# fileName = "capstoneTest" + str(now).translate(str.maketrans('','', string.punctuation)) + ".txt"
	#
	# file = open(fileName, "w")
	#
	# file.write(textfromspeech)
	#
	# capstoneTestTwo.MarkovPoemGenerator(fileName)
