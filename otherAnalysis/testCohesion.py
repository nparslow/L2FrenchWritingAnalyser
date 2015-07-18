
import gensim
import getCohesionVariables
import readDdag

__author__ = 'nparslow'

gensimModelFile = '/home/nparslow/Documents/AutoCorrige/SpellChecker/' \
                      'word2vec_models/orig/gensim_output/fullwiki_withcats.word2vec'
print "loading word2vec model"
word2vecModel = gensim.models.Word2Vec.load(gensimModelFile)

ddagfile = "/home/nparslow/Documents/AutoCorrige/Corpora/ddaged_CORPUS_CEFLE/Edna.ddag"
ddagfile = "/home/nparslow/Documents/AutoCorrige/Corpora/ddaged_CORPUS_CEFLE/Berthold.ddag"
ddagfile = "/home/nparslow/Documents/AutoCorrige/Corpora/ddaged_CORPUS_CEFLE/Crysmynta.ddag"


sentences = readDdag.readDdag(ddagfile)

a,b,c,d = getCohesionVariables.getCohesionVariables(word2vecModel, sentences)
