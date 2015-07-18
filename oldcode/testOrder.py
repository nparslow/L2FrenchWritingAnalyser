__author__ = 'nparslow'

import os
import xml.etree.cElementTree as ET
import codecs
import re


sentenceNumber = 1
processedSentenceFile =  "/home/nparslow/Documents/AutoCorrige/Corpora/crappy/" \
                         "chyFLE_2011_TI_UCY_4_Autoobservation_Aphrodite_Papaioannou" \
                         "/0/0/0/chyFLE_2011_TI_UCY_4_Autoobservation_Aphrodite_Papaioannou.E" \
                         + str(sentenceNumber) + ".passage.xml"
processedTokenFile =  "/home/nparslow/Documents/AutoCorrige/Corpora/crappy/" \
                         "chyFLE_2011_TI_UCY_4_Autoobservation_Aphrodite_Papaioannou" \
                         "/0/0/0/chyFLE_2011_TI_UCY_4_Autoobservation_Aphrodite_Papaioannou.E" \
                         + str(sentenceNumber) + ".tokens"
while ( os.path.isfile(processedSentenceFile) ):

    #with codecs.open(filename, mode='r', encoding='utf8') as sentenceFile:
    tree = ET.parse(processedSentenceFile)
    # 'W' nodes are 'words' which can include multiple tokens, e.g. 'bien que' is one word
    words = [x.get('lemma') for x in tree.iter('W')] # .iter for recursive, .findall for depth of 1
    tokens = [x.text.strip() for x in tree.iter('T')]

    if len(words) == 0:
        #print "len tokens:", len(tokens)
        # a parse wasn't possible
        if os.path.isfile(processedTokenFile):
            print "*** using tokens ***" #processedTokenFile
            # .tokens files are in latin1
            with codecs.open(processedTokenFile, mode="r", encoding='utf8') as tokenFile:
                for tokenline in tokenFile:
                    #tokenline.decode('latin1')
                    #tokenline = tokenline.decode('utf-8')
                    #tokenline = unicode(tokenline)
                    # check for a tab as the last line is empty
                    if '\t' in tokenline:
                        tokenNum, token = tokenline.strip().split('\t')
                        # consider something a word if it has an alphanumeric non-token in it
                        if re.search(ur'[^\W_]', token, flags=re.UNICODE):
                            tokens.append(token)
    #for node in tree.iter('W'):
    #    treeInfo = node.get("tree")
    #    lemma = node.get("lemma")

    print str(sentenceNumber), " ".join(tokens)

    sentenceNumber += 1
    processedSentenceFile =  "/home/nparslow/Documents/AutoCorrige/Corpora/crappy/" \
                         "chyFLE_2011_TI_UCY_4_Autoobservation_Aphrodite_Papaioannou" \
                         "/0/0/0/chyFLE_2011_TI_UCY_4_Autoobservation_Aphrodite_Papaioannou.E" \
                             + str(sentenceNumber) + ".passage.xml"
    processedTokenFile =  "/home/nparslow/Documents/AutoCorrige/Corpora/crappy/" \
                         "chyFLE_2011_TI_UCY_4_Autoobservation_Aphrodite_Papaioannou" \
                         "/0/0/0/chyFLE_2011_TI_UCY_4_Autoobservation_Aphrodite_Papaioannou.E" \
                         + str(sentenceNumber) + ".tokens"