# 9/9/19
# By Azariah Kierson-Galeano
# Produces a poem using aparrish's gutenbergdammit
# to pull text from gutenberg and uses as poem
from gutenbergdammit.ziputils import searchandretrieve
import MarkovPoemGeneratorMKII as mpg


mGen = mpg.MarkovPoemGenerator()

for info, text in searchandretrieve("gutenberg-dammit-files-v002.zip", {'Title': 'The Complete Book of Cheese'}):
    print(info['Title'][0], len(text))
    mGen.add_to_corpus(text)

# print(mGen.corpus)
mGen.make_markov_haiku()
