
import compareCorrectedCorpus

__author__ = 'nparslow'

for fnum in range(1, 18):
    xmlfile = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_CEFLE/Billy4/0/0/0/Billy4.E" + str(fnum) + ".dep.xml"

    finaltokens, origlemmacats, origverb2info, origtrees, origweight, wordsbeforemainverb =\
                compareCorrectedCorpus.getFinalTokenFormsAndTreesAndWeight(xmlfile)

    print fnum, wordsbeforemainverb