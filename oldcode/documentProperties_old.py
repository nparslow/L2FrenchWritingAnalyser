# -*- coding: utf-8 -*-
__author__ = 'nparslow'

import codecs
import os
import xml.etree.cElementTree as ET
import re

# from the corpus directory, base filename (w/o extension) [can include directory structure] and sentence number
# create the strings for the processed sentence file and the processed token file
# note baseFileName is used twice, once for the directory, once for the file
def getProcessedSentenceTokenPaths(corpus, baseFileName, sentenceNum):
    baseFileName = os.path.basename(baseFileName)

    path1 = sentenceNum/1000000
    path2 = (sentenceNum%1000000)/10000
    path3 = (sentenceNum%10000)/100
    #path4 = (sentenceNum%100)
    #print sentenceNum, path1, path2, path3 #, path4

    processedPath = os.path.join(corpus, baseFileName, str(path1), str(path2), str(path3) )
    baseProcessedSentenceFile = os.path.join(processedPath, baseFileName + ".E" + str(sentenceNum))
    processedSentenceFile = baseProcessedSentenceFile + ".dep.xml"
    processedTokenFile = baseProcessedSentenceFile + ".tokens"
    return processedSentenceFile, processedTokenFile

#allpossibleresults = {'ok', 'robust', 'corrected'}
def getLogFileInfo(logFilename):
    sentenceinfos = []
    with codecs.open(logFilename, mode='r', encoding='latin-1') as infile:
        for line in infile:
            # each line of interest has 'analysis sentencenumber sentence'
            # we take the first 2
            #sentenceinfo = re.match(ur'(ok|robust|corrected)\s(\d+)', line, flags=re.UNICODE)
            sentenceinfo = re.match(ur'(\w+)\s(\d+)\s', line, flags=re.UNICODE)
            if sentenceinfo:
                #allpossibleresults.add(sentenceinfo.groups()[0])
                sentenceinfos.append(sentenceinfo.groups())
    return sentenceinfos

def getTokensFromFile( processedTokenFile ):
    tokens = []
    if os.path.isfile(processedTokenFile):
        #print "*** using tokens ***", processedTokenFile
        # .tokens files are in utf-8 if run individually, latin-1 if run over corpus
        with codecs.open(processedTokenFile, mode="r", encoding='utf8') as tokenFile:
            for tokenline in tokenFile:
                # check for a tab as the last line is empty
                if '\t' in tokenline:
                    #print tokenline
                    tokenNum_token = tokenline.strip().split('\t')
                    # can have empty tokens, ignore them:
                    if len(tokenNum_token) > 1:
                        tokenNum, token = tokenline.strip().split('\t')
                        # take all tokens at this point, including punctuation
                        #if re.search(ur'[^\W_]', token, flags=re.UNICODE):

                        # hack to fix the euro problem:
                        token = re.sub(ur'\&\#226;\&\#130;\&\#172;', u'€', token, flags=re.UNICODE)
                        tokens.append(token)
    return tokens

def makeRegexFromTokens( tokens ):
    # œ changes to oe, but æ is not changed ... so allow for it in the regex
    # we have to account for changes in punctuation e.g. ` -> ' and ... from a single character
    # we if the first token has punctuation we allow that it may have been 'eaten' by the previous sentence
    #matchregex = ur'\s*' + ur'\s*'.join([re.sub(ur'oe', ur'[œ|oe]', re.sub(ur'[^\w\s]+', ur'[^\w\s]+', tokens[i], flags=re.UNICODE), flags=re.UNICODE)
    #                            if i > 0 else re.sub(ur'oe', ur'[œ|oe]', re.sub(ur'[^\w\s]+', ur'[^\w\s]*', tokens[i], flags=re.UNICODE), flags=re.UNICODE)
    #                                     for i in range(len(tokens))])
    nPuncTokensAtStart = -1
    for i in range(len(tokens)):
        if re.match(ur'(?:_|[^\w\s])+', tokens[i], flags=re.UNICODE):
            nPuncTokensAtStart = i
        else:
            break

    # a space can be removed before a - e.g. 'verbe en -er' goes to 'verbe', 'en-', 'er', I hope there's a good reason for that
    # so we allow space or - between tokens by swapping - for ' - ' and then making the spaces added optional
    # -ci is changed to _-ci
    # Chaque` un ->  Chaque'un (i.e. space removed and reduced to one token)
    # 1h:00 is changed to '1h', ':', '0' yup 1 zero is removed  <- not yet treated
    # 6:00-8:00 becomes: 6 : 0 - 8 : 0 <- this problem seems to have disappeared somehow ...
    # so allow sequences of numbers to vary in length and composition
    # allow a . at the start due to bad tokenisation
    '''
    matchregex = ur'\s*\.?' + ur'\s*'.join([re.sub(ur'oe', ur'(œ|oe)',
                                                re.sub(ur'\d+', ur'\d+',
                                                    re.sub(ur'(?<!\\s\\)\-', ur'\s?\-\s?',
                                                           re.sub(ur'_', ur'_?',
                                                               re.sub(ur'[^\w\s\-]+', ur'\s?[^\w\s\-]+\s?',
                                                                      tokens[i],
                                                                      flags=re.UNICODE),
                                                               flags=re.UNICODE),
                                                           flags=re.UNICODE),
                                                    flags=re.UNICODE),
                                                flags=re.UNICODE)
                                if i > nPuncTokensAtStart or len(tokens) == 1 else
                                         re.sub(ur'oe', ur'(œ|oe)',
                                                re.sub(ur'\d+', ur'\d+',
                                                    re.sub(ur'(?<!\\s)\\-', ur'\s?\-\s?',
                                                           re.sub(ur'_', ur'_?',
                                                               re.sub(ur'[^\w\s\-]+', ur'\s?[^\w\s\-]*\s?',
                                                                      tokens[i],
                                                                      flags=re.UNICODE),
                                                               flags=re.UNICODE),
                                                        flags=re.UNICODE),
                                                    flags=re.UNICODE),
                                                flags=re.UNICODE)
                                         for i in range(len(tokens))])
    '''
    matchregex = ur'\s*\.?' + ur'\s*'.join([re.sub(ur'oe', ur'(œ|oe)',
                                                re.sub(ur'(?<!\\s\\)\-', ur'\s?\-\s?',
                                                       re.sub(ur'_', ur'_?',
                                                           re.sub(ur'[^\w\s\-]+', ur'\s?[^\w\s\-]+\s?',
                                                                  tokens[i],
                                                                  flags=re.UNICODE),
                                                           flags=re.UNICODE),
                                                       flags=re.UNICODE),
                                                flags=re.UNICODE)
                                if i > nPuncTokensAtStart or len(tokens) == 1 else
                                         re.sub(ur'oe', ur'(œ|oe)',
                                                re.sub(ur'(?<!\\s)\\-', ur'\s?\-\s?',
                                                       re.sub(ur'_', ur'_?',
                                                           re.sub(ur'[^\w\s\-]+', ur'\s?[^\w\s\-]*\s?',
                                                                  tokens[i],
                                                                  flags=re.UNICODE),
                                                           flags=re.UNICODE),
                                                    flags=re.UNICODE),
                                                flags=re.UNICODE)
                                         for i in range(len(tokens))])
    return matchregex

class SentenceInfo:
    def __init__(self):
        self.words = []
        self.forms = []
        self.tokens = []



def getNextSentenceInfo( corpus, baseFileName, sentenceNum ):

    return None


# get the properties of a document
def getDocumentProperties(corpus, filename, debug=False):
    sentenceNum = 1
    paragraphLengths = []
    sentenceLengths = []
    wordSyllableLengths = []
    wordCharacterLengths = []

    baseFileName, extension = os.path.splitext(filename)
    processedLogFile = os.path.basename(baseFileName) + ".log"

    currentSentenceInfo = None
    processedSentenceFile, processedTokenFile = \
        getProcessedSentenceTokenPaths(corpus, baseFileName, sentenceNum)
    #print processedSentenceFile

    #print corpus, processedLogFile
    print "file:", filename
    sentenceinfos = getLogFileInfo(os.path.join(corpus, processedLogFile))
    print "Num sentences:", len(sentenceinfos)

    with codecs.open(filename, mode='r', encoding='utf8') as infile:
        #paragraphLength = 0
        lastParagraphSentenceBreak = 0
        lastParagraphLineBreak = 0

        lineNumber = 0
        for line in infile:
            if debug:
                print
                print "line:", line
            lineNumber += 1
            #print "linenum", lineNumber
            #if len(line) > 80: # we take this to remove headings, conversation lines etc., a sentence count would be better
            #    nparagraphs += 1
            # todo really need the sentence count, if more than one sentence call it a paragraph else not.

            #localParagraphLength = 0

            #print processedSentenceFile, os.path.isfile(processedSentenceFile)
            while ( currentSentenceInfo is None and os.path.isfile(processedSentenceFile) ):

                #with codecs.open(filename, mode='r', encoding='utf8') as sentenceFile:
                tree = ET.parse(processedSentenceFile)
                #latinparser = ET.XMLParser(encoding='latin1')
                #tree = ET.parse(processedSentenceFile, latinparser)
                #utf8parser = ET.XMLParser(encoding='utf-8')
                #tree = ET.parse(processedSentenceFile, utf8parser)
                #tree = ET.parse(processedSentenceFile)
                # 'W' nodes are 'words' which can include multiple tokens, e.g. 'bien que' is one word
                #print [x for x in tree.iter('node')]
                wordsforms = [(x.attrib['lemma'], x.attrib['form'], x.attrib['cluster'])
                              for x in tree.iter('node') if len(x.get('lemma'))>0] # .iter for recursive, .findall for depth of 1
                #tokens = [x.text.strip() for x in tree.iter('T')]
                #print reversed(wordtokens)
                words = [x[0] for x in sorted(wordsforms, key=lambda y: y[2].split('_')[1])]
                forms = [x[1] for x in sorted(wordsforms, key=lambda y: y[2].split('_')[1])]
                #print words
                #print forms
                tokens = getTokensFromFile(processedTokenFile)


                #print tokens
                #for node in tree.iter('W'):
                #    treeInfo = node.get("tree")
                #    lemma = node.get("lemma")
                matchregex = makeRegexFromTokens(tokens)


                #print [re.search(ur'[^\W_]', x, flags=re.UNICODE).group() for x in tokens if re.search(ur'[^\W_]', x, flags=re.UNICODE)]
                #print [x for x in tokens if re.search(ur'[^\W_]',x, flags=re.UNICODE) is None]
                #print [x for x in tokens if (x not in line) and (re.search(ur'[^\W_]',x) is None)]
                #print "not in line:", len([x for x in tokens if x not in line and re.search(ur'[^\W_]',x, flags=re.UNICODE) is None])
                # we ignore any token containing punctuation as it may have been altered by sxpipe
                # the line must contain the sequence of tokens (we allow some spaces in between)
                #print processedSentenceFile
                if debug:
                    print "sentence:", sentenceNum
                    print tokens

                if debug:
                    print "regex", matchregex

                if re.match(matchregex, line, flags=re.UNICODE):
                    # remove it from the line:
                    line = re.sub(ur'^' + matchregex, u'', line, flags=re.UNICODE)
                    if debug: print "newline:", line
                else:

                #if re.search(ur'.+'.join([re.sub(ur'oe', ur'[œ|oe]', x) for x in tokens if re.search(ur'[\W_]',x,
                #                                                                        flags=re.UNICODE) is None] ),
                #        line, flags=re.UNICODE) is None:

                #if len([x for x in tokens if x not in line and re.search(ur'[^\W_]',x, flags=re.UNICODE) is None ]) != 0:
                    #print "tokens:", tokens
                    #print "previous line:", line
                    #if localParagraphLength > 0:
                        #paragraphLength += localParagraphLength
                        #paragraphLengths.append(paragraphLength)
                        #paragraphLength = 0
                    # -1 as we are currently considering the 1st sentence after the break
                    #print "check for para", lastParagraphSentenceBreak, sentenceNum-1
                    if sentenceNum -1 > lastParagraphSentenceBreak :
                        paragraphLengths.append(sentenceNum-1-lastParagraphSentenceBreak)
                        lastParagraphSentenceBreak = sentenceNum -1
                        #print "new paragraph:", paragraphLengths, lastParagraphSentenceBreak
                    break # without increasing sentence number



                #localParagraphLength += 1
                #print "localPara length", localParagraphLength




                sentenceNum += 1
                processedSentenceFile, processedTokenFile = \
                    getProcessedSentenceTokenPaths(corpus, baseFileName, sentenceNum)

            #if localParagraphLength > 0 or paragraphLength > 0:
            #    paragraphLength += localParagraphLength
            #    paragraphLengths.append(paragraphLength)
            #    paragraphLength = 0

            #break
    # wrap up the last paragraph (here minus 1 as the sentence num is one higher than observed
    # even though we want the break after the last sentence unlike previously
    if lastParagraphSentenceBreak < sentenceNum-1:
        paragraphLengths.append(sentenceNum-1-lastParagraphSentenceBreak)
        #print "final paragraph:", paragraphLengths
    print "all paragraphs:        ", paragraphLengths
    print "sum of para lengths:   ", sum(paragraphLengths)
    print "last real sentence:    ", sentenceNum -1
    print "expected no. sentences:", len(sentenceinfos)
    if len(sentenceinfos) != sum(paragraphLengths):
        print "PROBLEM!!!!!"
    #else:
    #    print "Sentene numbers match :)"
    return len(paragraphLengths)

baseDir = "/home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS/CORPUS_CHY-FLE/"
baseDir = "/home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS/CORPUS_HELLAS-FLE/"
#baseDir = "/home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS/CORPUS_CENTRE-FLE/"

'''
filename = "chyFLE_2011_TI_UCY_4_Autoobservation_Aphrodite_Papaioannou.txt" # 109 sentences
filename = "chyFLE_2011_TI_UCY_4_Autoobservation_Savvia_Leonidou.txt" # 111 sentences

filenames = ["chyFLE_2011_TI_UCY_4_Autoobservation_Neofytos_Antoniou.txt"]
filenames = ["chyFLE_2010_TL_UCY_1A_Autoobservation_Agathe_Chrysse.txt"]
filenames = ['chyFLE_2010_TL_UCY_1A_Strategies_Yiannis_Panayides.txt']
filenames = ["chyFLE_2010_TL_UCY_1A_Strategies_Rafaella_Georgiou.txt"]
filenames = ["chyFLE_2011_TI_UCY_4_Autoobservation_Susanna_Georgiou.txt"]
filenames = ["chyFLE_2011_TI_UCY_4_Autoobservation_Margarita_Epiphaniou.txt"]
fname = baseDir + filename

corpus = "/home/nparslow/Documents/AutoCorrige/Corpora/crappy"
'''
filenames = ['hellasFLE_2010_TL_KPG_B2_Activite2_candidat18.txt'] # frmg bug site electronique -> site

#filenames = ['centreFLE_2005_TL_CFLETP_5_Activite2_CRYAN_Barra.txt'] # frmg bug le Match 1-0. -> the 0 is lost
#filenames = [ 'centreFLE_2004_TL_CFLETP_7_Activite2_ECKER_Susanne_2.txt'] # euro -> &#226;&#130;&#172;



corpus = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_ECRIT_VALETOPOULOS"

#nparagraphs = getDocumentProperties(corpus, fname)
#print "nparas:", nparagraphs


for filename in os.listdir(baseDir):
#for filename in filenames:
    print
    print filename
    fname = baseDir + filename
    nparagraphs = getDocumentProperties(corpus, fname, debug=False)
    print "nparas:", nparagraphs

#print "possible results", allpossibleresults
