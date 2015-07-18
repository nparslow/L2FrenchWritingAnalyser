# coding=utf-8

import codecs
import os
import re

import queryLexique380

__author__ = 'nparslow'




def getVocabFromFile( filename ):

    words = []
    enc = "utf-16le"
    if "advanced" in filename:
        enc = "utf-8"
    with codecs.open(filename, encoding=enc) as bfile:
        linecount = 0
        for line in bfile:
            linecount +=1
            line = line.strip()
            #print line
            # need to have * for e.g. fac*[ulté], need / for je vous/t'en prie
            # we don't keep '(voir oeil)'
            posswords = re.findall(ur'((?:[^\W\d_]|\[|\])(?:[^\W\d_]| |\[|\]|\'|\-|\*|/)*(?:[^\W\d_]|\[|\]|\*)(?: ?\((?:s[\'e]|\-trice|ime|avoir(?: l\')?|\-[svn]?e|en?|\-i?ère|à(?: l[\'ae])?|épouse|\-esse|yeux|veuve|d[\'])\))?)(?: ?\([^\)]+\))?', line, flags=re.UNICODE) # (?: ?\d+,)*\d*
            if "adj" in posswords:
                print posswords
                print re.findall(ur' ?\((?:s[\'e]|\-trice|ime|avoir(?: l\')?|\-[svn]?e|en?|\-i?ère|à(?: l[\'ae])?|épouse|\-esse|yeux|veuve|d[\'])\)', line, flags=re.UNICODE)
            for possword in posswords:
                print possword

                # remove oe as single chars (could equally do the opposite)
                possword = re.sub(ur'œ', 'oe', possword, flags=re.UNICODE)

                words.append(possword)
            #if linecount > 100:
            #    break
            blah = re.findall(ur'\((?:[^\W\d_]| |\'|\-)+\)', line, flags=re.UNICODE)
            for b in blah:
                print "blah                    ", b
    return words

def checkWordQuality( wordlist, lexicon):
    Simplewords = []
    Entities = []
    Options = []
    Variations = []
    Multi = []
    for word in wordlist:
        if len(word) < 4:
            print "short :", word
        if word.count(' ') > 1:
            print "spaces:", word
        if word not in lexicon:
            # change it if it's got optional elements:
            tmpword = word
            # remove any asterisks:
            tmpword = re.sub(ur'\*', '', word, flags=re.UNICODE)
            tmpword1 = tmpword
            tmpword2 = word
            if "(" in tmpword and ")" in tmpword:
                tmpword = re.sub(ur'\([^\)]+\)', '', tmpword, flags=re.UNICODE)
                tmpword = tmpword.strip()
            if "[" in tmpword and "]" in tmpword:
                tmpword1 = re.sub(ur'\[[^\]]+\]', '', tmpword, flags=re.UNICODE)
                tmpword2 = re.sub(ur'[\[\]]', '', tmpword, flags=re.UNICODE)
                tmpword1 = tmpword1.strip()
                tmpword2 = tmpword2.strip()
            if tmpword not in lexicon and tmpword1 not in lexicon and tmpword2 not in lexicon:
                print "lex   :", word, tmpword, tmpword1, tmpword2

        # there is some overlap, but we keep it exclusive for the moment (e.g. Union européen)
        if "[" in word or "]" in word:
            Options.append(word)
        elif "(" in word or ")" in word:
            Variations.append(word)
        elif " " in word:
            Multi.append(word)
        elif word[0].isupper():
            Entities.append(word)
        else:
            Simplewords.append(word)

    print "Options    :", len(Options)
    print "Variations :", len(Variations)
    print "Multis     :", len(Multi)
    print "Entities   :", len(Entities)
    print "simples    :", len(Simplewords)

    #print Multi


def main():


    lexiquefile = u"/home/nparslow/Documents/AutoCorrige/tools/Lexique380/Bases+Scripts/Lexique380.txt"
    lex = {}
    queryLexique380.loadLexiqueToDict( lexiquefile, lex )

    vocabfiledir = "/home/nparslow/Documents/AutoCorrige/vocabulary/vocab_lists/vocabulaire_progressif_du_francais/"
    beginnerfilename = "001_beginnervocablist.txt"
    intermediatefilename = "002_intermediatevocablist.txt"
    advancedfilename = "003_advancedvocablist.txt"

    beginnerWords = getVocabFromFile(os.path.join(vocabfiledir, beginnerfilename))
    print "beginner vocab size", len(beginnerWords)
    checkWordQuality(beginnerWords, lex)

    intermediateWords = getVocabFromFile(os.path.join(vocabfiledir, intermediatefilename))
    print "intermed vocab size", len(intermediateWords)
    checkWordQuality(intermediateWords, lex)

    advancedWords = getVocabFromFile(os.path.join(vocabfiledir, advancedfilename))
    print "advanced vocab size", len(advancedWords)
    checkWordQuality(advancedWords, lex)

    allintersected = set(beginnerWords).intersection(set(intermediateWords)).intersection(set(advancedWords))

    purebeginner = set(beginnerWords).difference(set(intermediateWords)).difference(allintersected)
    highbeginner = set(beginnerWords).intersection(set(intermediateWords)).difference(allintersected)
    pureintermediate = set(intermediateWords).difference(set(beginnerWords)).difference(set(advancedWords))
    highintermediate = set(advancedWords).intersection(set(intermediateWords)).difference(allintersected)
    highadvanced = set(advancedWords).difference(highintermediate).difference(allintersected)



    print "group sizes:"
    print "pure beginner     :", len(purebeginner)
    print "high beginner     :", len(highbeginner)
    print "all levels        :", len(allintersected)
    print "pure intermediate :", len(pureintermediate)
    print "high intermediate :", len(highintermediate)
    print "high advanced     :", len(highadvanced)
    print "total         :", len(purebeginner) + len(highbeginner) + len(allintersected) + len(highintermediate) + len(highadvanced)
    print "original total:", len(beginnerWords) + len(intermediateWords) + len(advancedWords)
    # overlap is difference

    for samp in [purebeginner, highbeginner, allintersected, pureintermediate, highintermediate, highadvanced]:
        print
        print
        print "Next Sample!!!"
        for word in samp:
            print word


# for beginners:
'''
Options    : 5
Variations : 29
Multis     : 43
Entities   : 69
simples    : 1556
'''
# for intermediate
'''
Options    : 81
Variations : 107
Multis     : 11
Entities   : 3
simples    : 2201
'''
# for advanced
'''
Options    : 47
Variations : 94
Multis     : 7
Entities   : 13
simples    : 2718
'''

if __name__ == "__main__":
    main()