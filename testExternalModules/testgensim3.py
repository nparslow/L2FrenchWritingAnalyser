__author__ = 'nparslow'

from gensim import corpora, models, similarities

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = corpora.Dictionary.load('dictionary.dict')
corpus = corpora.MmCorpus('corpus.mm')
print(corpus)

# tfidf transform
tfidf = models.TfidfModel(corpus) # step 1, initialize a model

# tfidf can now be used to apply transformations to vectos or a whole corpus
doc_bow = [(0,1), (1,1)]
print(tfidf[doc_bow]) # step 2, use the model to transform vectors

corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print(doc)

# LSI (= LSA?) transformation on top of the previous one
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # num topics = 2 => 2D space
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
lsi.print_topics(2)
#print "yo"

lsi.save('model.lsi') # same for tfidf, lda, ...
lsi = models.LsiModel.load('model.lsi')


# to update lsi with more data in the training corpus:
#model.add_documents(another_tfidf_corpus) # now LSI has been trained on tfidf_corpus + another_tfidf_corpus
#lsi_vec = model[tfidf_vec] # convert some new document into the LSI space, without affecting the model
#...
#model.add_documents(more_documents) # tfidf_corpus + another_tfidf_corpus + more_documents
#lsi_vec = model[tfidf_vec]

# alternatives to lsi:
# random projections RP
#model = rpmodel.RpModel(tfidf_corpus, num_topics=500)

# latent dirichlet allocation LDA
#model = ldamodel.LdaModel(bow_corpus, id2word=dictionary, num_topics=100)

# Hierarchical Dirichlet Process HDP, (relatively experimental in gensim)
#model = hdpmodel.HdpModel(bow_corpus, id2word=dictionary)
