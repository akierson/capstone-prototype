# By: Azariah Kierson-Galeano
# 9/25/19
# Mk III of Class based Poem Generator
# Added Poem types:
# Sonnets
# haiku

import random
import string
import types
import re
import os
from nltk.corpus import stopwords
from nltk.corpus import cmudict
from nltk import pos_tag
from collections import Counter

d = cmudict.dict()

class MarkovPoemGenerator(object):
	"""docstring for MarkovPoemGenerator."""

	def __init__(self, file_name=None):
		super(MarkovPoemGenerator, self).__init__()

		# Init if no file name
		self.corpus = []
		self.corpus_noStop = []

		# Open File
		if file_name != None:
			self.corpus = []
			self.corpus_noStop = []
			try:
				with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as myfile:
					self.add_to_corpus( myfile.read() )
			except Exception as e:
				raise

		# Placeholders
		self.poem = ""
		self.title = ""

		# Schema for title
		self.schema = [['to', 'VB', 'the', 'NN']]

	def add_to_corpus(self, newCorpus):
		"""
		Function: add_to_corpus
		Param:
		newCorpus, string to add to corpus
		@Returns none
		"""
		custpunct = '!"#$%&()*+, -./:;<=>?@[\\]^_`{|}~'
		# Added Error checking for lists
		if isinstance(newCorpus, str):
			newCorpus = [word.translate(str.maketrans('','', custpunct)) for word in newCorpus.replace('\n', ' ').lower().split(" ") if word]

		elif isinstance(newCorpus, list):
			newCorpus = [word.translate(str.maketrans('','', custpunct)).lower() for word in newCorpus if word]

		else:
			return -1

		self.corpus += newCorpus

		self.corpus_noStop += [word for word in newCorpus if word not in stopwords.words('english')]

	def make_title(self, schema = []):
        # Select schema
		if schema == []:
			schema = random.choice(self.schema)
        # if schema is given
		else:
			# check if schema is valid
			for place in schema:
                # check against nltk.help.upenn_tagset()
				if place.isupper() and place not in nltk.help.upenn_tagset():
                    # TODO: work regex to find nearest tag
					pass
		n = 5 # Length of phrase to test
		for i,x in enumerate(self.corpus):
			# TODO: add error reporting here
			text = pos_tag(self.corpus[i:i+n])
			print("Testing phrase: ", text)
			for i, place in enumerate(schema):
				if place.isupper():
					for word in text:
						if place in word[1]:
							# TODO: change word to word type
							schema[i] = word[0]
							if all([x.islower() for x in schema]):
								i += 1
								self.title = schema
								return 0
		print("Error: corpus not longer enough")
		return 1

	def find_syllables(self, word):
		"""
		Function: find_syllables
		Param:
		word, a string
		@Returns an int of the number of syllables in the word
		@Returns 0 if word not available
		"""
		if word in d:
			return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
		return -1

	def get_possible_words(self, start_word, max_length):
		"""
		Function: get_possible_words
		Param:
		start_word, a single word
		max_length, maximum number of syllables for words in outArray
		@Returns an array of words from the text that follow startWord
		"""
		outArray = []
		for i in reversed(range(1, len(self.corpus))):
			if self.corpus[i].lower() == start_word.lower() and self.find_syllables(self.corpus[i-1]) <= max_length and self.find_syllables(self.corpus[i-1]) != 0:
				outArray.append(self.corpus[i-1])
		if len(outArray) == 0:
			print("Error: no possible words for '"+ start_word+"'")
			# TODO: use words type to get better replacement words
			print("Selecting words less than", max_length )
			outArray = [word for word in self.corpus_noStop if (self.find_syllables(word) < max_length)]
		return outArray

	# TODO: increase length of markov chain based on corpus
	# Size of Corpus
	def make_line(self, last_word = None, size = 10, type="MARKOV", chain_length=0):
		"""
		Function: make_line
		Param:
		last_word, a word that the line should rhyme with
		size, an integer number of syllables in the returned line
		type, MARKOV or LINE
		chain_length, length of chains if using MARKOV
		@Returns a line with the number of syllables
		"""
		# TODO: Use iambic pentameter
		# ie unstressed, stressed syllable (1,2)

		# TODO: select word based on rhyme scheme
		# If no rhyme given, rhyme is randomly choosen such that last sylable in word is stressed
		# TODO: Make lines forwards if used in haiku
		if last_word == None:
			last_word = random.choice(self.corpus_noStop)
			length = self.find_syllables(last_word.lower())

			while length == -1:
				last_word = random.choice(self.corpus_noStop)

		else:
			last_word = random.choice(self.rhyme(last_word))
			length = self.find_syllables(last_word.lower())


		# Initialize line from end

		prev_word = random.choice(self.get_possible_words(last_word, size - length))

		line = last_word

		if type == "MARKOV":
			# Markov chain through line to start
			while length < size:
				line = prev_word + " " + line
				# if there is a break here b/c no words have one syllable etc.
				last_word, prev_word = prev_word, random.choice(self.get_possible_words(prev_word, size - length))
				length += self.find_syllables(prev_word)

		if type == "LINE":
			# By full line
			while length < size:
				prev_word, last_word = last_word, self.corpus[self.corpus.index(last_word) - 1 ]
				if self.find_syllables(last_word) > (size - length):
					last_word = random.choice(self.get_possible_words(prev_word, size - length))
				line = last_word + " " + line
				length += self.find_syllables(last_word)

		return line

	def rhyme(self, inp, level = 0):
		"""
		Function: rhyme
		Param:
		inp, string that should be rhymed with
		level, int indicating accuracy of rhyme
		@Returns a word from the corpus that matches inp
		"""
		# Get dictionary from Carnegie Mellon University API
		entries = cmudict.entries()
		# Get number of syllables for the inp word from dictionary
		syllables = [(word, syl) for word, syl in entries if word == inp]
		print(inp, " - ", syllables)
		# Create empty rhyming list
		rhymes = []

		for (word, syllable) in syllables:
 			rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:] and word in self.corpus_noStop]

		print(inp, " rhymes with ", rhymes)
		# If there are still no rhymes, increase level
		# if 0, word not in dictionary
		# if 1, only rhyme is self
		if len(rhymes) <= 1 and level < 3:
			level += 1
			print("Rhyme Level increased to: ", level)
			rhymes = [self.rhyme(inp, level)];

		# If there are no rhymes in corpus, get any rhyme
		if len(rhymes) <= 1:
			print(inp + " has no rhyme in the corpus")
			for (word, syllable) in syllables:
	 			rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
			if len(rhymes) <= 1:
				print(inp + " has no rhymes. Choosing random word")
				rhymes = random.choice(self.corpus_noStop)

		return rhymes

	# for Round 3
	def make_markov_poem(self, lines = 5, line_length = 10, lineStruct = [], rhyme = True, rhymeScheme = [1,2,1,2], type="MARKOV"):
		# TODO: Add Rhyme Scheme
		# TODO: finish me
		"""
		Function: make_markov_poem
		creates a sonnet from the given corpus
		Param:
		none
		@Returns none
		"""
		# Get number of rhymes
		rhyme_num = Counter(rhyme).keys()
		if type == "MARKOV":
			self.make_markov_sonnet(type="MARKOV")
		if type == "LINE":
			self.make_markov_sonnet(type="LINE")

	def make_markov_sonnet(self):
		"""
		Function: make_markov_sonnet
		creates a sonnet from the given corpus
		Param:
		none
		@Returns none
		"""
		# Sonnet rhyme scheme
		# ABBA - CDCD - EFEF - GG
		# Write 1st line
		line1 = self.make_line()
		# Write 4th line to rhyme with first
		line4 = self.make_line(line1.split()[-1])
		# Write 2,3
		line2 = self.make_line()
		line3 = self.make_line(line2.split()[-1])
		# Write 6,8
		line6 = self.make_line()
		line8 = self.make_line(line6.split()[-1])
		# Write 5,7
		line5 = self.make_line()
		line7 = self.make_line(line5.split()[-1])
		# Write line 9, 11
		line9 = self.make_line()
		line11 = self.make_line(line9.split()[-1])
		# Write line 10,12
		line10 = self.make_line()
		line12 = self.make_line(line10.split()[-1])
		# Write line 13,14
		line13 = self.make_line()
		line14 = self.make_line(line13.split()[-1])

		self.make_title()
		self.poem = "\n".join([line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12, line13, line14])

	def make_markov_haiku(self):
		line1 = self.make_line(size=5)
		line2 = self.make_line(size=7)
		line3 = self.make_line(size=5)

		if self.title == "":
			self.make_title()

		self.poem = "\n".join([line1, line2, line3])

	def print_poem(self):
		if self.title == "":
			self.make_title()
		print('\n', " ".join(self.title))

		print('#####')

		if self.poem == "":
			self.make_markov_haiku()
		print(self.poem)

		print('#####')

if __name__ == '__main__':
	mGen = MarkovPoemGenerator('../testCorpus/behemoth_lyrics.txt')

	# mGen.make_markov_sonnet()
	mGen.make_markov_haiku()
	print(" ".join(mGen.title))
	print('###')
	print(mGen.poem)
