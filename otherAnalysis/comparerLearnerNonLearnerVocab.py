
import codecs
import json
import os
import re

import queryLexique380

__author__ = 'nparslow'


outfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/outputs/learner_vocab_combined.json"

vocab2count = {}
with codecs.open(outfilename, 'r', encoding="utf8") as infile:
    vocab2count = json.load( infile)

print len(vocab2count)


def analyse( path, learnervocabdict, missingwords2count, missingwords ):
    if os.path.isdir(path):
        for element in os.listdir(path):
            analyse(os.path.join(path, element), learnervocabdict, missingwords2count, missingwords)
    else:
        analyseFile(path, learnervocabdict, missingwords2count, missingwords)

def analyseFile( filename, vocab2count, missingwords2count, missingwords):
    basefileName, fileExtension = os.path.splitext(filename)

    if fileExtension == ".ddag":
        with codecs.open(filename, mode='r', encoding='utf8') as tfile:
            sentence = []
            for line in tfile:
                line = line.strip()
                if "##DAG END" in line:
                    if len(sentence) not in missingwords2count: missingwords2count[len(sentence)] = 0
                    missingwords2count[len(sentence)] += 1
                    if len(sentence) > 0:
                        print "missing:", " ".join(sentence)
                    sentence = []
                elif line[0] != "#":
                    tokennum, tokeninfo, nexttokennum = line.split('\t')
                    #print tokeninfo
                    # can have multiple tokens so start from the right:
                    token = re.search(ur'(?: )([^\}]+)$', tokeninfo, flags=re.UNICODE).groups()[0]
                    # some left over space:
                    token = token.strip()

                    # in case some empty tokens arrive here:
                    if len(token) > 0:
                        if token not in vocab2count:
                            sentence.append(token)
                            missingwords.add(token)

nativecorpus = "/home/nparslow/Documents/AutoCorrige/Corpora/tokenised/CORPUS_LITTAVANCE"
missed = {}
missingwords = set([])
analyse(nativecorpus, vocab2count, missed, missingwords)
print missed

lex = {}
queryLexique380.loadLexiqueToDict(u"/home/nparslow/Documents/AutoCorrige/tools/Lexique380/Bases+Scripts/Lexique380.txt", lex)

for mword in missingwords:
    if mword in lex:
        print mword, lex[mword]
    else:
        print "NOT IN LEXIQUE!", mword
print "not in lex:", len([x for x in missingwords if x not in lex]), " of ", len(missingwords)
