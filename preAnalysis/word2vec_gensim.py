#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'nparslow'


import gensim, logging
import os
import codecs

import gensim.models.word2vecExtended

categoriesToKeep = {'v', 'nc', 'adj', 'adv'}
ends_categoriesToKeep = tuple(["_" + y for y in categoriesToKeep])

# do all preprocessing here:
# note: will run 2 passes over this, one to get frequencies, one to train model
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in codecs.open(os.path.join(self.dirname, fname), encoding="utf-8", mode="r"):
                # todo clean up here
                tokens = line.split()
                #print [x for x in tokens if x.endswith(ends_categoriesToKeep)]
                yield [x for x in tokens if x.endswith(ends_categoriesToKeep)]
                #yield line.split()





if __name__=='__main__':

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # expected input format is a sequence of sentences, each sentence is a list of utf-8 strings
    sentences = [['first', 'sentence'], ['second', 'sentence']]

    #sentences = MySentences('wikiPreTreated') # a memory-friendly iterator
    #print type(sentences)

    import createKnownDict
    #corpusdirectory = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/divided/"
    #corpusfilename = "mini_frwiki_net_train.tok"
    corpusdirectory = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/"
    corpusfilename = "frwiki_net.tok"
    fullfilename = os.path.join(corpusdirectory, corpusfilename)
    sentences = createKnownDict.Tokeniser(fullfilename, mincount=5)

    #print sentences
    #print type(sentences)

    # re http://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.Word2Vec
    # min_count = 5 by default (i.e. must see a word 5 times to consider it), normal = 0 to 100
    # size = 100 by default, basically is no. of degrees of freedom that training algo has,
    #      = no. of elements in each neural network layer I think
    # higher requires more data, reasonable 10s to 100s
    # workes = 1 by default, can speed up by putting no. of processors, e.g. workers=4
    # sg = 1 by default - defines the training algorithm, sg =1 => skip-gram
    #  otherwise cbow
    # window = max distance between current and predicted word in the sentence
    # alpha = learning parameter (for gradient descent?) will drop to zero as training progresses
    # seed = (for random no. gen)
    # sample = 0 (off) threshold for configuring which high freq words are downsampledt
    # hs = 1 use hierarchical sampling
    # negative (>0)  how many 'noise words' should be drawn (usually 5-20) ???
    # cbow_mean = 0 (use the sum of the context word vectors, if 1 use the mean, only applies to cbow)
    # hashfxn = hash function to init weights (default = python's)
    # iter = no. of iterations
    # requires Cython [word2vec is very slow w/o it]

    #model = gensim.models.Word2Vec(sentences, workers=4)
    model = gensim.models.word2vecExtended.Word2VecExtended(sentences, workers=4)

    #model.save('mymodel.word2vec')
    modelsavedir = u"/home/nparslow/Documents/AutoCorrige/SpellChecker/word2vec_models"
    #modelfile = u'miniwiki_withcats.word2vec'
    modelfile = u'fullwiki_withcats.word2vec'
    model.save(os.path.join(modelsavedir, modelfile ))
    #new_model = gensim.models.Word2Vec.load('/tmp/mymodel')
    # note can load and continue training

    '''
    print model.most_similar(positive=['femme_nc', 'roi_nc'], negative=['homme_nc'], topn=5)
    print model.similarity('femme_nc', 'homme_nc')
    print model.doesnt_match(u"déjeuner_nc diner_nc céréale_nc".split())
    print model['homme_nc']
    print len(model['homme_nc'])
    '''