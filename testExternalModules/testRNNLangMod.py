__author__ = 'nparslow'

from scipy.sparse import *
import theanets
import numpy as np
import codecs


inputfilename = "wikiPreTreated/frwikipedia_001.out"

# builds a dictionary of word_cat -> count
# from a processed wiki file with each line = a sentence
# each token = word_cat (as analysed by the parser) for that sentence
def compileDict(inputfilename):
    word_cat2index = {"_UNK":0 , "_START":1, "_STOP":2}
    # can we merge start and stop ?
    index = 3 # start with unknown word at 0 and a start/stop word at 1 & 2
    # (so that word 1 in a phrase has a probability)

    nlines = 0
    with codecs.open(inputfilename) as infile:
        for line in infile:
            word_cats = line.split("\t")
            for word_cat in word_cats:
                if word_cat not in word_cat2index:
                    word_cat2index[word_cat] = index
                    index += 1
            #print word_cat2index
            nlines += 1
            if nlines > 10: break
    return word_cat2index


# returns 2 coo sparse matrices from training and testing
# cut_point determines the percentage in each (80%)
def addAllFromFile(inputfilename, word2index):
    inputArray = [] #np.array([]) # output is just input displaced by 1

    nlines = 0
    with codecs.open(inputfilename) as infile:
        for line in infile:
	    # add start and stop to the list of tokens
            word_cats = ["_START"] + line.split("\t") + ["_STOP"]
            for word_cat in word_cats:
                if word_cat not in word2index:
                    word_cat = "_UNK"
                oneword = lil_matrix( (len(word2index), 1), dtype=float)
                oneword[word2index[word_cat]] = 1
		# remember numpy starts from 0 indexing unlike matlab

                inputArray.append(oneword)
                #print inputArray[-1]

            nlines += 1
            if nlines > 10: break
    num_examples = len(inputArray)
    train_percentage = 80
    cut_point = (num_examples*train_percentage)/100
    # move the cut point to a start/stop combination:
    while inputArray[cut_point].nonzero()[0] != word2index["_START"]:
	# i.e. we'll stop when the last one would be _STOP
        cut_point += 1
    return hstack(inputArray[:cut_point]).tocsc(), \
	   hstack(inputArray[cut_point:]).tocsc() # hstack returns a coo matrix


word2index = compileDict(inputfilename)

trainarray, testarray = addAllFromFile(inputfilename, word2index)

print "train\n", trainarray[:,0:-1].shape, trainarray.shape

print "test\n", testarray


# Not sure: we don't want a constant batch size?,
# we want a contant no. of sentences but not words
BATCH_SIZE = 32

exp = theanets.Experiment( # Experiment covers training and evaluation
    theanets.recurrent.Regressor, # recurrent regression model
    layers=(len(word2index), ('lstm', 100), len(word2index)),
        # 3 layers, first = no. of input unit matches no. of words,
        # second = LSTM (long short-term-memory) with 10 units (recurrent)
        # output layer also matches no. of words
        # note there are other ways of specifying layers
    batch_size=BATCH_SIZE
    )


# train
exp.train([trainarray[:,0:-1], trainarray[:,1:]], optimize='rmsprop')

