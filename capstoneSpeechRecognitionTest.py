import speech_recognition as sr
import datetime
import string
import capstoneTestTwo

# Get Text from Speech

r = sr.Recognizer()
mic = sr.Microphone()

#
with mic as source:
    audio = r.listen(source)

textfromspeech = r.recognize_google(audio)
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
