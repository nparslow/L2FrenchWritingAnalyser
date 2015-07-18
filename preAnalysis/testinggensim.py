# coding=utf-8
__author__ = 'nparslow'

import gensim
import math

model = gensim.models.Word2Vec.load('/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/gensim_output/'
                                    'fullwiki_withcats.word2vec')

print model.most_similar(positive=['femme', 'roi'], negative=['homme'], topn=5)
print model.similarity('femme', 'homme')
print model.similarity("princess", "femme")
print model.doesnt_match(u"déjeuner diner céréale".split())
print model['homme']
print len(model['homme'])

norm = 0
for a in model['homme']:
    #print model['homme'][a]
    norm += math.pow(model['homme'][a],2)
print math.sqrt(norm)
