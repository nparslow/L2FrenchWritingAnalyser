#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'nparslow'

from gensim import corpora, models, similarities, matutils

import logging
import codecs

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# to avoid having whole corpus in memory at once:

categoriesToKeep = {'v', 'nc', 'adj', 'adv'} # convert to a tuple for endswith

def splitAndCut( line, categoriesToKeep, minNumLemmas=3):
    #minNumLemmas = 3 # require at least 3 lemmas in a sentence
    word_cats = line.split('\t') # no lower as will only affect the cat
    #if len(word_cats) > 3: print word_cats
    return [x for x in word_cats if x.endswith(tuple(categoriesToKeep)) and len(word_cats) > minNumLemmas]

class MyCorpus(object):
    def __iter__(self):
        for line in open('frwikipedia_001.out'):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(splitAndCut(line, categoriesToKeep))

corpus_memory_friendly = MyCorpus()


# collect statistics about all tokens (a bit annoying that this requires two loops over the data ...
dictionary = corpora.Dictionary(splitAndCut(line, categoriesToKeep) for line in codecs.open('frwikipedia_001.out', encoding="utf-8", mode="r"))
# remove stop words and words that appear only once
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
dictionary.filter_tokens(once_ids) # remove words that appear only once
dictionary.compactify() # remove gaps in id sequence after words that were removed
print(dictionary)
dictionary.save('dictionary_test.dict')

# to save the corpus in Market Matrix format, also SVMlight, Blei, Low possible
corpora.MmCorpus.serialize('corpus_test.mm', corpus_memory_friendly)

#print(corpus_memory_friendly)

# convert from/to sparse (also numpy conversion possible)
#corpus = matutils.Sparse2Corpus(scipy_sparse_matrix)
#scipy_csc_matrix = matutils.corpus2csc(corpus_memory_friendly)
#print scipy_csc_matrix

corpus = corpora.MmCorpus('corpus_test.mm')
print(corpus)

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)

lsi.save('model_test.lsi')