__author__ = 'nparslow'

from gensim import corpora, models, similarities, matutils

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# to avoid having whole corpus in memory at once:

stoplist = set('for a of the and to in'.split())

class MyCorpus(object):
    def __iter__(self):
        for line in open('mycorpus.txt'):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.lower().split())

corpus_memory_friendly = MyCorpus()

# collect statistics about all tokens
dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))
# remove stop words and words that appear only once
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
            if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
dictionary.compactify() # remove gaps in id sequence after words that were removed
print(dictionary)
dictionary.save('dictionary.dict')

# to save the corpus in Market Matrix format, also SVMlight, Blei, Low possible
corpora.MmCorpus.serialize('corpus.mm', corpus_memory_friendly)

print(corpus_memory_friendly)

# convert from/to sparse (also numpy conversion possible)
#corpus = matutils.Sparse2Corpus(scipy_sparse_matrix)
scipy_csc_matrix = matutils.corpus2csc(corpus_memory_friendly)
#print scipy_csc_matrix