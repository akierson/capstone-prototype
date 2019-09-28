import nltk
import random
# CC -> coordinating conjunction
# RB -> adverb
# IN -> preposition
# NN -> listen
# JJ -> adjective
# VB* -> verb

class TitMaker(object):
    """docstring for TitMaker."""

    def __init__(self, corpus=[]):
        super(TitMaker, self).__init__()
        self.corpus = corpus
        self.schema = [['to', 'VB', 'the', 'NN']]

    def make_tit(self, schema = []):
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

        n=5 # Length of phrase to test
        for i, x in enumerate(corpus):
            text = nltk.pos_tag(corpus[i:i+n])
            for place in title:
                if place.isupper():
                    for word in text:
                        if place in word[1]:
                            title[title.index(place)] = word[0]
                            break # takes first word for place and returns to loop
                        # else if place is the last place and
                        elif :

if __name__ == '__main__':
    corpus = open("../testCorpus/behemoth_lyrics.txt").read().split(" ")
    tm = TitMaker()
    tm.make_tit()
