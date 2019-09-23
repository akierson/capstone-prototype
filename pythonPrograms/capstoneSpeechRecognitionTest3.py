# By: Azariah Kierson-Galeano
# 4/12/19
# Using previous and listen_in_background from Speech Recognition
# Made call callable from

# Based on https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py

import speech_recognition as sr
import time
import sys
import MarkovPoemGeneratorMKII as mpg

GOOGLE_KEY = ""

# Need to instanstiate variable before in order to call from callback

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

	while True:
		with mic as source:
			r.adjust_for_ambient_noise(source)

		# Start audio recording
		# Will start a phrase when energy passes set energy threshold
		# Stops when below recognizer_instance.pause_threshold
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
		# try:
		# 	text = r.recognize_ibm(audio, username = "", password = "")
		# 	print("IBM Watson thinks you said " + text)
		# except sr.UnknownValueError:
		#     print("IBM Watson could not understand audio")
		# except sr.RequestError as e:
		#     print("Could not request results from IBM Watson service; {0}".format(e))

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
