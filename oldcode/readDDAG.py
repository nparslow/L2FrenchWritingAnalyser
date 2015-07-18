# coding=utf-8
__author__ = 'nparslow'

import codecs
import re
import bz2
import os
import documentProperties

# for the wiki, check if its a useful sentence or not (i.e. if its not just meta garbage)
def checkSentence(sentence):
    npunct = 0
    nmeta = 0
    nrealword = 0
    nwordish = 0
    nnumber = 0
    nother = 0
    for token in sentence:
        #print token[0], token
        if re.match(ur'(_SENT_BOUND|_META_TEXTUAL.*)$', token, flags=re.UNICODE):
            nmeta += 1
            #print "meta", token
        elif re.match(ur'[\W_]+$', token, flags=re.UNICODE):
            npunct += 1
            #print "punct", token
        elif token == "_NUMBER":
            nnumber += 1
        elif token[0] == '_':
            nwordish += 1
            #print "wordish", token
        elif  re.match(ur"[\w\-\'\s]+\.?$", token, flags=re.UNICODE):
            nrealword += 1
            #print "real word", token
        else:
            nother += 1
            #print "other", token

    ntypes = len(set(sentence))

    #print " ".join(sentences[sent])
    #print npunct, nrealword, nwordish, nother
    #print len(sentence), nmeta, npunct, nrealword, nwordish, nother
    # to avoid repeating style sentence
    test = nrealword + nwordish >= min(3, npunct + nother + nmeta + nnumber) and 1.0*ntypes/len(sentence) > 0.5
    if test:
        print "keep                ", " ".join(sentence)

        pass
    else:
        print "chuck out           ", " ".join(sentence)
        #print "chucking out:", " ".join(sentence), nrealword+nwordish, npunct + nother + nmeta +nnumber, 1.0*ntypes/len(sentence)

    return test


def analyse( path, outpath, nSentences, token2count ):

    if os.path.isdir(path):
        for element in os.listdir(path):
            nSentences += analyse(os.path.join(path, element), outpath, nSentences, token2count)
    else:
        nSentences += analyseFile(path, outpath, token2count)
    return nSentences



# will overwrite output
# todo make directory if it doesn't exist
# note : have to remove INTITULES
def analyseFile( filename, outpath, token2count ):

    ignoretokens = [
        #"_SENT_BOUND",
        #"_META_TEXTUAL_PONCT",
        #"_META_TEXTUAL_GN",
        "_EPSILON",
    ]

    basefileName, fileExtension = os.path.splitext(filename)
    basefileName =  os.path.basename(basefileName) # remove the directories
    outfilename = os.path.join(outpath, basefileName + ".tokens" )

    # one token per line, empty line for end of phrase

    sentences = []
    #with bz2.BZ2File("ep_001.udag.bz2") as dagfile: # , encoding="latin-1" # not supported ...
    #with bz2.BZ2File("estrep_001.udag.bz2") as dagfile: # , encoding="latin-1" # not supported ...
    #with bz2.BZ2File("frwikipedia_002.udag.bz2") as dagfile: # , encoding="latin-1" # not supported ...
    with codecs.open(filename, mode="r", encoding="utf8") as ddagfile: # todo not sure if utf8 or latin-1?

        sentence = []
        linenum = 0
        for line in ddagfile:
            #line = line.decode('latin-1')
            linenum += 1
            #print line.strip()
            if "##DAG END" in line:
                # check if sentence has some real words in it: # only for wiki
                #if checkSentence(sentence):
                if True:
                    sentences.append(sentence)
                    for token in sentences[-1]:
                        if token not in token2count: token2count[token] = 0
                        token2count[token] += 1
                sentence = []

            #elif "##DAG BEGIN" in line: # also skip ##OFFSET lines
            #    pass
            elif line[0] != "#":
                dagstart, info, dagend = line.strip().split('\t')
                dagstart, dagend = int(dagstart), int(dagend)

                #print info
                detailed_info, token = re.match(ur'\{(.+)\} (.+)', info, flags=re.UNICODE).groups()
                tknums_tks = re.findall(ur'<F id="E\d+F(\d+)">([^<]+)</F>', detailed_info, flags=re.UNICODE)
                # this gives a list of pairs token_number, token (one line can have a goup of multiple tokens
                start = int(tknums_tks[0][0])
                end = int(tknums_tks[-1][0])
                orig_tokens = [x[1] for x in tknums_tks ]

                # remove any any extra stuff:
                if " " in token:
                    token, crud = token.split(' ', 1)
                # require no split amalgams: (i.e. no double underscore in the token)
                #if "__" not in token:

                    # never add _EPSILON:
                #    if token != "_EPSILON":


                sentence.append( token )




    #print sentences
    #print token2count
    print "no. of sentences", len(sentences)
    test_sentences = [11, 21, 31, 111, 121, 131, 1001, 1011, 1021, 1031, 2010, 2020, 2030]
    #for sent in test_sentences:
    for sent in range(len(sentences)):
        if sent < len(sentences):
            print u" ".join(sentences[sent])  #, len(set(sentences[sent])), len(sentences[sent])

    print len(sentences), len(set([tuple(x) for x in sentences]))

    sent2count = {}
    for sent in sentences:
        sent = tuple(sent)
        if sent not in sent2count: sent2count[sent] = 0
        sent2count[sent] +=1

    print
    print('non-unique sentences:')
    for sent in sent2count:
        if sent2count[sent] > 1:
            print " ".join(sent)


    checkfilename = u"/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_LITTAVANCE/M1_A_JAC-RINC/CorpusTXT/35_JR_A_CorpusV2.txt"
    checkfiletxt = ""
    with codecs.open(checkfilename, mode="r", encoding="utf8") as checkfile:
        checkfiletxt = checkfile.read()

    print "testing testing"
    for sentence in sentences:
        for token in sentence:
            if token not in checkfiletxt:
                print "missing:", token
                # should pick up only _ options and oe changes.


    return len(sentences)










inpath  = "/home/nparslow/Documents/AutoCorrige/Corpora/tokenised/CORPUS_LITTAVANCE/35_JR_A_CorpusV2.ddag"
outpath = "/home/nparslow/Documents/AutoCorrige/Corpora/tokenised/CORPUS_LITTAVANCE"
token2count = {}
analyse(inpath, outpath, 0, token2count) # start with a count of 0 sentences



print
#print [token for token in token2count if token[0] == "_"]
for token in token2count:
    print token, token2count[token]
#print [token for token in token2count]




