# By: Azariah Kierson-Galeano
# 4/3/19
# Same as previous but now as a class

import random
import string
from nltk.corpus import stopwords
from nltk.corpus import cmudict

# TODO: Add error reporting

d = cmudict.dict()

class MarkovPoemGenerator(object):
	"""docstring for MarkovPoemGenerator."""

	def __init__(self, file_name=None):
		super(MarkovPoemGenerator, self).__init__()

		# Init if no file name
		self.corpus = ""
		self.corpus_noStop = ""

		# Open File
		if file_name != None:
			with open(file_name, 'r') as myfile:
				self.corpus = myfile.read().replace('\n', ' ')

			# TODO: Translate punctuation is removing apostrophes and making some words unreadable
			# contractions are also not readable
			self.corpus_noStop = [word.translate(str.maketrans('','', string.punctuation)).lower() for word in self.corpus.split() if word not in stopwords.words('english')]

		# Placeholder for sonnet
		self.sonnet = ""

	def add_to_corpus(self, string):
		"""
		Function: add_to_corpus
		Param:
		string, string to add to corpus
		@Returns none
		"""

		self.corpus += string.replace('\n', ' ')

		# TODO: Translate punctuation is removing apostrophes and making some words unreadable
		# contractions are also not readable
		self.corpus_noStop += [word.translate(str.maketrans('','', string.punctuation)).lower() for word in string.split() if word not in stopwords.words('english')]


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
		return 0

	def get_possible_words(self, start_word, max_length):
		"""
		Function: get_possible_words
		Param:
		start_word, a single word
		max_length, maximum number of sylables for words in outArray
		@Returns an array of words from the text that follow startWord
		"""
		outArray = []
		for i in reversed(range(1, len(self.corpus_noStop))):
			if self.corpus_noStop[i].lower() == start_word.lower() and self.find_syllables(self.corpus_noStop[i-1]) <= max_length and self.find_syllables(self.corpus_noStop[i-1]) != 0:
				outArray.append(self.corpus_noStop[i-1])
		if len(outArray) == 0:
			print("outArray is empty for:" + start_word)
			outArray = [word for word in self.corpus_noStop if (self.find_syllables(word) < max_length)]
		return outArray

	# TODO: increase length of markov chain based on corpus 
	def make_line(self, last_word = None, size = 10):
		"""
		Function: make_line
		Param:
		last_word, a word that the line should rhyme with
		size, th integer number of syllables in the returned line
		@Returns a line with the number of syllables
		"""
		# If no rhyme given, rhyme is randomly choosen
		if last_word == None:
			last_word = random.choice(self.corpus_noStop)
		else:
			# TODO: Should start from zero and only increase if only rhyme is self
			last_word = random.choice(self.rhyme(last_word, 1))

		# Initialize line from end
		prev_word = random.choice(self.get_possible_words(last_word, size))
		length = self.find_syllables(last_word.lower())
		line = last_word

		# Markov chain through line to start
		while length < size:
			line = prev_word + " " + line
			# if there is a break here b/c no words have one syllable etc.
			last_word, prev_word = prev_word, random.choice(self.get_possible_words(prev_word, size - length))
			length += self.find_syllables(prev_word)

		return line

	def rhyme(self, inp, level):
		"""
		Function: rhyme
		Param:
		inp, string that should be rhymed with
		level, int indicating accuracy of rhyme
		@Returns a word from the corpus that matches inp
		"""
		entries = cmudict.entries()
		syllables = [(word, syl) for word, syl in entries if word == inp]
		rhymes = []
		for (word, syllable) in syllables:
 			rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:] and word in self.corpus_noStop]

		# If there are still no rhymes, increase level
		if len(rhymes) == 0 and level < 10:
			print("Rhyme Level increased to: " + level)
			rhymes = self.rhyme(inp, level + 1);

		# if there are no rhymes in corpus, get any rhyme
		if len(rhymes) == 0:
			print(inp + " is rhymeless")
			for (word, syllable) in syllables:
	 			rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]

		return rhymes

	def make_markov_sonnet(self):
		"""
		Function: make_markov_sonnet
		creates a sonnet from the given corpus
		Param:
		none
		@Returns none
		"""
		# TODO: Should add to
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

		print("\nABBA - CDCD - EFEF - GG")
		print("----Poem----")
		print(line1)
		print(line2)
		print(line3)
		print(line4)
		print(line5)
		print(line6)
		print(line7)
		print(line8)
		print(line9)
		print(line10)
		print(line11)
		print(line12)
		print(line13)
		print(line14)
		self.sonnet = "\n".join([line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12, line13, line14])

if __name__ == '__main__':
	mGen = MarkovPoemGenerator('../testCorpus/shakespeare.txt')
	# increase defaults
	print(mGen.sonnet)
