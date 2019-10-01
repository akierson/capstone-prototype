import nltk
import random
# CC -> coordinating conjunction
# RB -> adverb
# IN -> preposition
# NN -> listen
# JJ -> adjective
# VB* -> verb

class TitleMaker(object):
    """docstring for TitMaker."""

    def __init__(self, corpus=[]):
        super(TitleMaker, self).__init__()
        self.corpus = corpus
        self.schema = [['to', 'VB', 'the', 'NN']]
        self.title = self.make_title()

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
        n = 3 # Length of phrase to test
        for i,x in enumerate(corpus):
        # TODO: add error reporting here
            text = nltk.pos_tag(corpus[i:i+n])
            print("Testing phrase: ", text)
            for place in schema:
                if place.isupper():
                    for word in text:
                        if place in word[1]:
                            schema[schema.index(place)] = word[0]
                            if all([x.islower() for x in schema]):
                                i += 1
                                self.title = schema
                                print(self.title)
                                return 0
        print("Error: corpus not longer enough")
        return 1



if __name__ == '__main__':
    corpus = open("../testCorpus/behemoth_lyrics.txt").read().split(" ")
    tm = TitleMaker()
    print(tm.title)
