from nltk.corpus import cmudict
import random

d = cmudict.dict()

last_word = random.choice()
while re.sub('[^0-9]','', d[last_word])[-1] != 1 or 2:
    last_word = random.choice()
