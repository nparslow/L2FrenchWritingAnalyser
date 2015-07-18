__author__ = 'nparslow'



import json
import codecs
import os
import re

import documentProperties

jsonfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellCheckerJson/entry.json"
originalcorpus = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker"
correctedcorpus = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellCheckerCorrected"



baseDirorig = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellChecker/"
baseDircorr = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellChecker/Corrected/"

def getEntryNumFromFileName(filename):
    return int(re.search(ur'_(\d+)\.txt$', filename, flags=re.UNICODE).groups()[0])

def readAnalysedCorpus(baseDir, corpus):
    # stock a dictionary entrynum -> textdata
    texts = {}
    for filename in os.listdir(baseDir):
        print
        print filename
        fname = baseDir + filename
        text = documentProperties.getDocumentProperties(corpus, fname, debug=False)
        print "nparas:", text.nParagraphs()
        print "nsents:", text.getNSentences()
        print "nwords:", text.getNWords()
        print "mean sents/para", text.meanSentencesPerParagraph()
        print "sd   sents/para", text.sdSentencesPerParagraph()
        print "mean words/sent", text.meanWordsPerSentence()
        print "sd   words/sent", text.sdWordsPerSentence()
        print "mean letts/word", text.meanLettersPerWord()
        print "sd   letts/word", text.sdLettersPerWord()
        print "mean sylls/word", text.meanSyllablesPerWord()
        print "sd   sylls/word", text.sdSyllablesPerWord()
        print ""

        entrynum = getEntryNumFromFileName(filename)
        texts[entrynum] = text

#origTexts = readAnalysedCorpus(baseDirorig, originalcorpus)
#corrTexts = readAnalysedCorpus(baseDircorr, correctedcorpus)

with codecs.open(jsonfilename, mode="r", encoding='utf8') as jsonfile:
    entries = json.load(jsonfile)

errorInfo = {}
for entrynum, original, corrected, worderrorlist in entries:
    #print entrynum, worderrorlist
    errorInfo[entrynum] = (worderrorlist)
    #origText = origTexts[entrynum]
    #corrText = corrTexts[entrynum]

    numSentences = worderrorlist.count([u'***', []])
    #print numSentences, origText.nSentences(), corrText.nSentences()
    if entrynum == 225: print worderrorlist

    sentenceNum = 0

    originaldepxml = os.path.join(originalcorpus)

    print numSentences
    if original == corrected:
        print "zero changes", entrynum, original
        # only 6 times the whole entry is unchanged




