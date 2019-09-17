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

		# GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
		#   "type": "service_account",
		#   "project_id": "symbolic-path-231420",
		#   "private_key_id": "230deb51df80c301e7aa3a40ec0b85f9c5ca8e13",
		#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDCxiOqv5qB/NnM\ntq8GAlUS/yCWQ8kORGIsq3FfUCkX2RI+OZgf6HfJqiGq6Lb2/S8JDqdS+VqxCe+o\ncm8Z9fXHXOlvaxVrETdQRm77P1HlclXjsdb8VCZrWG/HBTs8xATczTRE9qyTfUhW\nyPJP2q6/qeOJ2ms8mlbxFW7kuWhKIOn7AuIe+bz4qUN0dOl+sJSgDHHC2dDELdW3\nRbW97Oxs5pw4FFuXg9Susiabrh7+/2Jcsgpo2tRwb8T+hwkDz9+7UXoqze2Li5mr\nOH4mItwYLRfK7+2obmQ1+rsDJZ4Lk1MPe2A2SzFYqN/mzZsuIGXjvFv8ghbueG5A\n4/EDZ4qnAgMBAAECggEAAUWh/f96Vtb75SZcRkHFpHYeFF0k9v7jVT9ZYjH30rwM\nLnPZ1nuCLML7rU4Pw9UrdXevCA+w0+8orYTxzM2aaU7mB2A/p49ZOSD8oI9tTX5N\nqUsECGnURmcxc69JD8CH95kvejPSNLRgwJBXZMYc1guZ/NB8Wsz3PGPTcZL0Z2eE\ns+Sl2gr+kMqpFGqxA9/vXgt+0t4b2yCyKdsbelqMBzPOZ9FvsQXKxGJ/wY5TdELU\n4JNIlRR7vBXoK+58sxIgI25aV9tjdLaJR3/KKTYicRImsMIrnH7Cjgs0Re3+2p85\n1LOfim2Ii2gb0wtdLx0TQCy/Tu5XCwoWO2y4oV6RAQKBgQDr36cg9Pzb+SV7QbXL\n5dylZ0Dhf8u+iuQ5Cs5ierUDSij0HWYhI1JStX48ulylRjznJknjXW2tdPQlENYS\nW1NhAa6madSkeVw7dcLKkUFe0LLxXIeuMXyCScEEhKci/MCdAI5IpoIGesT99zaW\nYeyXmyKQWMaVdFO7lGv1DVO2IQKBgQDTZLgE8A+ntJz6/j90ld31NxU2Uz6vZAXZ\nWlw1rau4PShbxKTzmZYek/WfrdR1yCPk1pwYeNhUGZqS3b7w8Pb8mQsJdcUPlvmK\ncwanBScUe8IRjP7BdYbJhEt3nD1p8N5nJftNXOZ+CvUXE/aVQnoq2CdDdUngWl1b\no4ZOcvgXxwKBgGs9D9soBx5rs+LKCUFejGaW/ySG2bcTppdYlmSnrUyFlwEFrL08\nNd1srqwlfqGVwXLGMamxfH/0QFvpv6ow40OjZCg8zXTJyGkwLROz3qig8fpSO02z\nKgyCQ8MuHF8H0vqOmiHlshAIGS/uCV9tvgdffONruT2R2c/atwp+uKSBAoGAedu+\npMIKFD/umlWEGN3npFrLdJSKNyruoDwRmbPyoHNI15XFDNQFkLz0Q8c+CWOFJX59\nXzISanCUBYOkdVpC1pwWm65zGaiLUz85n4A95fXtipZ/qN/qAjKsGlhLos2CN23S\nrucVy6TfYh1U8PfwWtBd2eo72wPce14JpyFpWLMCgYEAlLazrQBzSp+Y97m2psiT\nvfdMs2f/bp6hpmEJ7nqmbIaLn1YNlzZGfbrFh3MLBsaAiGX8aZKRpmYfOkeNi1pQ\nW2+B9NBqeb+99mDWyFMY2/C4B6PvBN0si28LXiMMSAd6/ifnhrzUF6UtEwq+CUt4\neZIRXzsF5FsoP7zeCnhopZY=\n-----END PRIVATE KEY-----\n",
		#   "client_email": "capstone-python-test@symbolic-path-231420.iam.gserviceaccount.com",
		#   "client_id": "101640386256386769525",
		#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
		#   "token_uri": "https://oauth2.googleapis.com/token",
		#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
		#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/capstone-python-test%40symbolic-path-231420.iam.gserviceaccount.com"
		# }
		# """
		# try:
		# 	text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
		# 	print("Google Cloud Speech thinks you said " + text)
		# except sr.UnknownValueError:
		# 	print("Google Cloud Speech could not understand audio")
		# except sr.RequestError as e:
		#     print("Could not request results from Google Cloud Speech service; {0}".format(e))

		mGen.add_to_corpus(text)

		print(len(mGen.corpus))
		print(mGen.corpus)
		print(len(mGen.corpus_noStop))
		print(mGen.corpus_noStop)
		if len(mGen.corpus_noStop) > 20:
			mGen.make_markov_haiku()
			print(mGen.poem)
			poemResult = input("Did you like my haiku:\n1.Yes\n2.No\n")
			print(poemResult)
			while poemResult not in ["1","2"]:
				print("I'm a lazy coder")
				poemResult = input("Did you like my haiku:\n1.Yes\n2.No\n")

		time.sleep(1)
