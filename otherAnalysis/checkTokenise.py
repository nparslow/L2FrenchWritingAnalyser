

import os
import codecs
import createKnownDict

__author__ = 'nparslow'

corpusdirectory = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/"
corpusdirectory = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/divided/"

#corpusfilename = "mi-frwiki1" # half wiki
#corpusfilename = "frwiki_net.tok" # full wiki
corpusfilename = "mini_frwiki_net_train.tok" # first 50k lines of dev part
#corpusfilename = "frwiki_net_dev.tok" # 7,000,000 lines
#corpusfilename = "editions.tok"

fullfilename = os.path.join(corpusdirectory, corpusfilename)

tokeniser = createKnownDict.Tokeniser(fullfilename, mincount=5)

tokeniser.saveFiles("/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/word2count.json",
                    "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/token2subtokens.json")

#sentences = createKnownDict.tokeniseFile(fullfilename, MINCOUNT=5)

count = 0
for sentence in tokeniser:
    #print sentence
    count += 1
    for word in sentence:
        print word
    #print sentence
    if count > 20: break

testfilename = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/divided/test.tok"

with codecs.open(testfilename, mode="r", encoding='utf8') as tfile:
    for line in tfile:
        print tokeniser.tokeniseLine(line)

