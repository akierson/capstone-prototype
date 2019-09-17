#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Sphinx
try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

# recognize speech using Google Cloud Speech
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "symbolic-path-231420",
  "private_key_id": "230deb51df80c301e7aa3a40ec0b85f9c5ca8e13",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDCxiOqv5qB/NnM\ntq8GAlUS/yCWQ8kORGIsq3FfUCkX2RI+OZgf6HfJqiGq6Lb2/S8JDqdS+VqxCe+o\ncm8Z9fXHXOlvaxVrETdQRm77P1HlclXjsdb8VCZrWG/HBTs8xATczTRE9qyTfUhW\nyPJP2q6/qeOJ2ms8mlbxFW7kuWhKIOn7AuIe+bz4qUN0dOl+sJSgDHHC2dDELdW3\nRbW97Oxs5pw4FFuXg9Susiabrh7+/2Jcsgpo2tRwb8T+hwkDz9+7UXoqze2Li5mr\nOH4mItwYLRfK7+2obmQ1+rsDJZ4Lk1MPe2A2SzFYqN/mzZsuIGXjvFv8ghbueG5A\n4/EDZ4qnAgMBAAECggEAAUWh/f96Vtb75SZcRkHFpHYeFF0k9v7jVT9ZYjH30rwM\nLnPZ1nuCLML7rU4Pw9UrdXevCA+w0+8orYTxzM2aaU7mB2A/p49ZOSD8oI9tTX5N\nqUsECGnURmcxc69JD8CH95kvejPSNLRgwJBXZMYc1guZ/NB8Wsz3PGPTcZL0Z2eE\ns+Sl2gr+kMqpFGqxA9/vXgt+0t4b2yCyKdsbelqMBzPOZ9FvsQXKxGJ/wY5TdELU\n4JNIlRR7vBXoK+58sxIgI25aV9tjdLaJR3/KKTYicRImsMIrnH7Cjgs0Re3+2p85\n1LOfim2Ii2gb0wtdLx0TQCy/Tu5XCwoWO2y4oV6RAQKBgQDr36cg9Pzb+SV7QbXL\n5dylZ0Dhf8u+iuQ5Cs5ierUDSij0HWYhI1JStX48ulylRjznJknjXW2tdPQlENYS\nW1NhAa6madSkeVw7dcLKkUFe0LLxXIeuMXyCScEEhKci/MCdAI5IpoIGesT99zaW\nYeyXmyKQWMaVdFO7lGv1DVO2IQKBgQDTZLgE8A+ntJz6/j90ld31NxU2Uz6vZAXZ\nWlw1rau4PShbxKTzmZYek/WfrdR1yCPk1pwYeNhUGZqS3b7w8Pb8mQsJdcUPlvmK\ncwanBScUe8IRjP7BdYbJhEt3nD1p8N5nJftNXOZ+CvUXE/aVQnoq2CdDdUngWl1b\no4ZOcvgXxwKBgGs9D9soBx5rs+LKCUFejGaW/ySG2bcTppdYlmSnrUyFlwEFrL08\nNd1srqwlfqGVwXLGMamxfH/0QFvpv6ow40OjZCg8zXTJyGkwLROz3qig8fpSO02z\nKgyCQ8MuHF8H0vqOmiHlshAIGS/uCV9tvgdffONruT2R2c/atwp+uKSBAoGAedu+\npMIKFD/umlWEGN3npFrLdJSKNyruoDwRmbPyoHNI15XFDNQFkLz0Q8c+CWOFJX59\nXzISanCUBYOkdVpC1pwWm65zGaiLUz85n4A95fXtipZ/qN/qAjKsGlhLos2CN23S\nrucVy6TfYh1U8PfwWtBd2eo72wPce14JpyFpWLMCgYEAlLazrQBzSp+Y97m2psiT\nvfdMs2f/bp6hpmEJ7nqmbIaLn1YNlzZGfbrFh3MLBsaAiGX8aZKRpmYfOkeNi1pQ\nW2+B9NBqeb+99mDWyFMY2/C4B6PvBN0si28LXiMMSAd6/ifnhrzUF6UtEwq+CUt4\neZIRXzsF5FsoP7zeCnhopZY=\n-----END PRIVATE KEY-----\n",
  "client_email": "capstone-python-test@symbolic-path-231420.iam.gserviceaccount.com",
  "client_id": "101640386256386769525",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/capstone-python-test%40symbolic-path-231420.iam.gserviceaccount.com"
}
"""
try:
    print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
except sr.UnknownValueError:
    print("Google Cloud Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))

# recognize speech using Houndify
# Has free level for 12 things/day
HOUNDIFY_CLIENT_ID = "KVXJVsAp-z_JAZlxwKHq_g=="  # Houndify client IDs are Base64-encoded strings
HOUNDIFY_CLIENT_KEY = "zUmSQKKcHAn_VEd8LsPnpUluwK5Db9YMblgDicyPm5yD7tp20WswAHDTKb1LsAHHL2laMDmzgyDVBkQNX-AKEg=="  # Houndify client keys are Base64-encoded strings
try:
    print("Houndify thinks you said " + r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY))
except sr.UnknownValueError:
    print("Houndify could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Houndify service; {0}".format(e))
