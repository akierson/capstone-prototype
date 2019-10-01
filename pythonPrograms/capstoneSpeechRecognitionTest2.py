# By: Azariah Kierson-Galeano
# 4/12/19
# Using previous and listen_in_background from Speech Recognition
# Made call callable from

# Based on https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py

import speech_recognition as sr
import time
import sys
import MarkovPoemGenerator as mpg

GOOGLE_KEY = ""

# Need to instanstiate variable before in order to call from callback
corpus = ""

# Create test phrase for script to match ie change params until phrase x is matched. run 5 times

# Function: callback
# Parms: recognizer is a speech recognizer, audio is the
# Returns: bool
def callback(recognizer, audio):
	# received audio data, now we'll recognize it using Google Speech Recognition
	try:
		# TODO: Add other speech recognizers
		# Run Speech recognizer here
		# text = recognizer.recognize_google(audio, key=GOOGLE_KEY)
		text = recognizer.recognize_google(audio)
		# Pass variable out
		print(type(text))
		corpus += text
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == '__main__':
	# TODO: Error reporting
	# Initialize classes
	r = sr.Recognizer()
	mic = sr.Microphone()

	# TODO: add loop

	# Start audio recording
	# TODO: figure out how this works with other mics
	with mic as source:
		r.adjust_for_ambient_noise(source)

	#  call stop_listening to stop audio
	stop_listening = r.listen_in_background(mic, callback)

	# Check size of corpus
	if len(corpus) > 700:
		print("corpus")
		# Call Stop
		stop_listening(wait_for_stop=False)
		# Run algorithm
		mGen = mpg.MarkovPoemGenerator()
		mGen.add_to_corpus(corpus)
		mGen.make_markov_sonnet()
		# Print poem ??
		time.sleep(1)

	time.sleep(1)
