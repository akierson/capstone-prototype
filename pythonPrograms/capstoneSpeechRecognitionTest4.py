# By: Azariah Kierson-Galeano
# 9/24/19
# Using previous and listen_in_background from Speech Recognition
# Made call callable from

# Based on https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py

import speech_recognition as sr
import time
import sys
import MarkovPoemGeneratorMKII as mpg
import serial
import json
import threading
from __future__ import print_function
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource

# Add key locations here
GOOGLE_KEY = open("../keys/google-credentials.txt", "r").read()
IBM_KEY = open("../keys/ibm-credentials.txt", "r").read()
# HOUNDIFY_KEY = open("../keys/houndify-credentials.txt", "r").read()
ARD_PORT = "COM4"

# Example using websockets
# TODO: Move to new file
class MyRecognizeCallback(RecognizeCallback):
	def __init__(self):
		RecognizeCallback.__init__(self)

	def on_transcription(self, transcript):
		print(transcript)

	def on_connected(self):
		print('Connection was successful')

	def on_error(self, error):
		print('Error received: {}'.format(error))

	def on_inactivity_timeout(self, error):
		print('Inactivity timeout: {}'.format(error))

	def on_listening(self):
		print('Service is listening')

	def on_hypothesis(self, hypothesis):
		print(hypothesis)

	def on_data(self, data):
		print(data)


# Create test phrase for script to match ie change params until phrase x is matched. run 5 times

if __name__ == '__main__':
	# TODO: Error reporting
	# Initialize classes
	r = sr.Recognizer()
	# Add settings to Recognizer class
	# r.energy_threshold = 300
	# Can be changed to 150 - 3500
	mic = sr.Microphone()
	mGen = mpg.MarkovPoemGenerator()
	# TODO: Add serial
	ser = serial.Serial(ARD_PORT, 9600)

	# Open  threads here

	while True:

		# Sets energy thresholds
		with mic as source:
			r.adjust_for_ambient_noise(source)

		# Start audio recording
		# Will start a phrase when energy passes set energy threshold
		# Stops when below recognizer_instance.pause_threshold
		# Add passage from book of questions
		print("Talk to me, oh fleshy one")
		with mic as source:
			audio = r.listen(source)

		# Run various audio recognizers here
		text = ""
		try:
		    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
		except sr.UnknownValueError:
		    print("Sphinx could not understand audio")
		except sr.RequestError as e:
		    print("Sphinx error; {0}".format(e))

		try:
			text = r.recognize_google(audio)
			print("Google Speech Recognition thinks you said " + text)
		except sr.UnknownValueError:
		    print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
		    print("Could not request results from Google Speech Recognition service; {0}".format(e))

		# Library not updated for current IBM template
		# Adapted from https://github.com/watson-developer-cloud/python-sdk/blob/master/examples/speech_to_text_v1.py

		# If service instance provides API key authentication
		service = SpeechToTextV1(
		    iam_apikey=IBM_KEY)

		# Example using threads in a non-blocking way
		mycallback = MyRecognizeCallback()

		# TODO: Make sure this works. Should be able to read binary from audio
		# audio_file = open(join(dirname(__file__), '../resources/speech.wav'), 'rb')
		audio_file = audio.get_wav_data()

		audio_source = AudioSource(audio_file)
		# TODO: Change bit rates etc to match output from microphone
		recognize_thread = threading.Thread(
		    target=service.recognize_using_websocket,
		    args=(audio_source, "audio/l16; rate=44100", mycallback))
		recognize_thread.start()




		mGen.add_to_corpus(text)
		if len(mGen.corpus_noStop) > 20:
			mGen.make_markov_haiku()
			print(mGen.poem)
			poemResult = input("Did you like my haiku:\n1.Yes\n2.No\n")
			print(poemResult)
			while poemResult not in ["1","2"]:
				print("I'm a lazy coder")
				poemResult = input("Did you like my haiku:\n1.Yes\n2.No\n")

			if poemResult == "1":
				pass
			if poemResult == "2":
				pass

		time.sleep(1)
