# By: Azariah Kierson-Galeano
# 4/3/19
# Makes a sonnet from a corpus of words using Markov Chains

import random
from nltk.corpus import stopwords
from nltk.corpus import cmudict

d = cmudict.dict()
extra_words = {
	1 : ['I', 'went', 'cat', 'dog'],
	2 : ['person', 'other', 'after'],
	3 : ['important', 'amazing', 'everything'],
	4 : ['america', 'beautiful', 'alternative'],
	5 : ['alliteration', 'california', 'abomination'],
	6 : ['capitaliztion', 'personification', 'desertification'],
	7 : ['refrigerator', 'decriminalization', 'onomatopoeia'],
	8 : [''],
	9 : [''],
	10 : ['']
}

# Function: word_not_in_text
# Param:
# length, the length of the word in syllables
# @Returns a word of the given syllabic length
def word_not_in_text(length):
	# Should create list from added text
	return extra_words[length]

# Function: remove_stop_words
# Param:
# sentence, a string
# @Returns the sentence without stop words
def remove_stop_words(sentence):
	sentence = sentence.split()
	return [word for word in sentence if word not in stopwords.words('english')]

# Function: find_syllables
# Param:
# word, a string
# @Returns an int of the number of syllables in the word
def find_syllables(word):
	if word in d:
		return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
	return 10

# Function: get_possible_words
# Param:
# start_word, a single word
# text, a string of text
# @Returns an array of words from the text that follow startWord
def get_possible_words(start_word, text, max_length):
	outArray = []
	for i in range(len(text)-1):
		if text[i].lower() == start_word.lower() and find_syllables(text[i+1]) <= max_length:
			outArray.append(text[i+1])
	# Have backup check if list is empty
	if len(outArray) == 0:
		outArray = word_not_in_text(max_length)
	return outArray

# Function: make_line
# Param:
# seedWords, an array with words for starting lines
# text, a array containing the word
# size, th integer number of syllables in the returned line
# @Returns a line with the number of syllables
def make_line(seedWords, text, size):
	seed_word = random.choice(seedWords)
	next_word = random.choice(get_possible_words(seed_word, text, size))
	length = find_syllables(seed_word.lower())
	line = seed_word
	while length < size:
		line += " " + next_word
		seed_word, next_word = next_word, random.choice(get_possible_words(next_word, text, size - length))
		length += find_syllables(next_word)
	return line


# Function: make_markov_haiku
# Param:
# seedWords, list of seed word
# text, Text to use for Markov chains
# @returns a string haiku, lines separated by \n
def make_markov_haiku(seedWords, text):
	# Clean text and make a list
	text = [x.strip().strip(',?!') for x in text.split()]
	# Get random word from seed words
	seedWords = remove_stop_words(seedWords)
	haiku = make_line(seedWords, text, 5) + "\n" +  make_line(seedWords, text, 7) + "\n" + make_line(seedWords, text, 5)
	return haiku + "\n"

# Function: make_markov_haiku
# Param:
# seedWords, list of seed word
# text, Text to use for Markov chains
# @returns a string haiku, lines separated by \n
def make_markov_sonnet(seedWords, text):
	# Clean text and make a list
	text = [x.strip().strip(',?!') for x in text.split()]
	# Get random word from seed words
	seedWords = remove_stop_words(seedWords)
	sonnet = ""
	for x in range(14):
		sonnet += make_line(seedWords, text, 10) + "\n"
	return sonnet + "\n"

# Function: file_to_words
# Param:
# file_name, Name of file to be read into fie
# @returns a string of all words in the file
def file_to_words(file):
	with open(file, 'r') as myfile:
		data = myfile.read().replace('\n', '')
	return data



if __name__ == '__main__':
	seedWords = 'I'
	# print(make_markov_haiku(seedWords, file_to_words('rapLyrics.txt')))
	print(make_markov_sonnet(seedWords, file_to_words('shakespeare.txt')))
