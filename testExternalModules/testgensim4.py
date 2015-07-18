__author__ = 'nparslow'

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
dictionary = corpora.Dictionary.load('dictionary.dict')
corpus = corpora.MmCorpus('corpus.mm') # comes from the first tutorial, "From strings to vectors"
print(corpus)

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

doc = "Human computer interaction"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print(vec_lsi)


# sorted from most similar to least similar topic

# only use MatrixSimilary if it fits in memory
index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it
# if not use Similarity.Similarity (splits file into 'shards' = files put on disk)
# there's also a sparse version ...
#index = similarities.Similarity(lsi[corpus])

# can save and load:
index.save('/tmp/deerwester.index')
index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')

sims = index[vec_lsi] # perform a similarity query against the corpus
sims = sorted(enumerate(sims), key=lambda item: -item[1]) # sort by the similarity score
print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples