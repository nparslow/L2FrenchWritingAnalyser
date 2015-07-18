
import numpy as np
import gensim

import createKnownDict
#from compareCorrectedCorpus import rollingMean
from utils import rollingMean

__author__ = 'nparslow'


def cosTheta( vec1, vec2 ):
    return np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))

# prob load model externally so only load once ...
#def getCohesionVariables( word2vecModelFilename, Word2vecVocabulary, listSentences):
def getCohesionVariables( word2vecModel, listSentences):

    vectors = []
    totalvec = np.zeros( word2vecModel.layer1_size ) # hopefully this is the right size
    meanWordWordCosTheta = 0
    meanWordSentCosTheta = 0

    # loop over the sentences
    totaltokenssofar = 0
    for i_sentence in range(len(listSentences)):
        sentence = listSentences[i_sentence]
        # for each sentence get the total vector
        vector, mwordsent_ct, mwordword_ct = getVector(word2vecModel, sentence)

        # rolling mean the wordword and wordsent values:
        #print "int vals", mwordsent_ct, mwordword_ct
        #print meanWordWordCosTheta, totaltokenssofar, mwordword_ct, len(sentence)
        meanWordWordCosTheta, ignorethis = rollingMean(meanWordWordCosTheta, totaltokenssofar, mwordword_ct, len(sentence) )
        meanWordSentCosTheta, totaltokenssofar = rollingMean(meanWordSentCosTheta, totaltokenssofar, mwordsent_ct, len(sentence) )
        #print "prog", totaltokenssofar, meanWordWordCosTheta, meanWordSentCosTheta
        #totaltokenssofar += len(sentence)


        # stock it in an array for later
        vectors.append(vector)

        # add to the wholetext vector
        totalvec += vector

    #print totalvec
    #exit(20)
    # loop over stocked sentences:
    costhetaTotals = []
    costhetaPrevs = []
    for i_vec in range(len(vectors)):
        vec = vectors[i_vec]
        # compare with previous, compare with total & stock answers
        costhetaTotal = cosTheta(vec, totalvec)
        #costhetaPrev = None
        if i_vec > 0:
            lastvec = vectors[i_vec-1]
            costhetaPrev = cosTheta(vec, lastvec)
            costhetaPrevs.append(costhetaPrev)
        costhetaTotals.append(costhetaTotal)

        #print "ctt", costhetaTotal


    # calculate averages
    meanSentTextCosTheta = np.mean(costhetaTotals, axis=0)
    meanSentSentCosTheta = np.mean(costhetaPrevs, axis=0)

    #print "cohesion", meanWordWordCosTheta, meanWordSentCosTheta, meanSentSentCosTheta, meanSentTextCosTheta
    #exit(10)
    # return averages
    return meanWordWordCosTheta, meanWordSentCosTheta, meanSentSentCosTheta, meanSentTextCosTheta


def getVector( word2vecModel, sentence ):

    totalvec = np.zeros( word2vecModel.layer1_size ) # np zeros?
    costhetaTotals = []
    costhetaPrevs = []
    # loop over tokens
    lastvec = None
    for i_token in range(len(sentence)):
        token = sentence[i_token]
        vec = None
        # if token in vocab, use word2vec of it
        if token in word2vecModel.vocab:
            vec = word2vecModel[token]

        # if not, get its type then use word2vec on it
        else:
            wordtype = createKnownDict.categoriseWord(token)
            #print wordtype
            #print wordtype in word2vecModel.vocab
            if wordtype in word2vecModel.vocab:
                vec = word2vecModel[wordtype]
            else:
                vec = word2vecModel["_UKN"]
        #print "vec", vec
        #print "tot", totalvec
        totalvec += vec
        costhetaTotal = cosTheta(vec, totalvec)
        costhetaTotals.append(costhetaTotal)
        if i_token > 0:
            costhetaPrev = cosTheta(vec, lastvec)
            costhetaPrevs.append(costhetaPrev)
        # add to the total
        totalvec += vec
        lastvec = vec

    # calculate averages
    meanWordSentCosTheta = np.mean(costhetaTotals, axis=0)
    # as a sentence may have only 1 word: (this will be nan otherwise)
    meanWordWordCosTheta = 1.0
    if len(sentence) > 1:
        meanWordWordCosTheta = np.mean(costhetaPrevs, axis=0)
    #print "avg", meanWordSentCosTheta, meanWordWordCosTheta



    # return the total vector
    return totalvec, meanWordSentCosTheta, meanWordWordCosTheta
