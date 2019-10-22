import nltk

corpus = open('../testCorpus/behemoth_lyrics.txt', 'r')

lineLength = [10,5,8]

poem = [len(lineLength)]

for line in lineLength:
    seed = random.choice(len(corpus))
    while line:
        line +=
