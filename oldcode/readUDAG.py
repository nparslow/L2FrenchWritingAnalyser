__author__ = 'nparslow'

import codecs
import re
import bz2


ignoretokens = [
    "_SENT_BOUND",
    "_META_TEXTUAL_PONCT",
    "_META_TEXTUAL_GN",
    "_EPSILON",
    ]

sentences = []
token2count = {}
#with bz2.BZ2File("ep_001.udag.bz2") as dagfile: # , encoding="latin-1" # not supported ...
#with bz2.BZ2File("estrep_001.udag.bz2") as dagfile: # , encoding="latin-1" # not supported ...
with bz2.BZ2File("frwikipedia_002.udag.bz2") as dagfile: # , encoding="latin-1" # not supported ...


#with codecs.open("frwikipedia_001.udag", encoding="latin-1") as dagfile:
    currentDAG = {}
    linenum = 0
    for line in dagfile:
        line = line.decode('latin-1')
        linenum += 1
        if "##DAG END" in line:
            #print sorted(currentDAG.items())
            sentences.append([stoptoken[1] for start, stoptoken in sorted(currentDAG.items())])
            # sort will use the end element as it's first in the tuple so this should work
            for token in sentences[-1]:
                if token not in token2count: token2count[token] = 0
                token2count[token] += 1
        if "##DAG BEGIN" in line:
            currentDAG = {}
        if line[0] != "#":
            start, info, end = line.split('\t')
            start = int(start)
            end = int(end)
            if start not in currentDAG or (start in currentDAG and end < currentDAG[start][0] ):
                matches = re.match(ur'^\{(.+)\} (.+)$', info, flags=re.UNICODE)
                if matches:
                    xmlinfo, adjustedtoken =  matches.group(1,2)
                    # the adjusted token can have more info in [], so remove it
                    adjustedtoken = adjustedtoken.split(' ')[0]

                    if adjustedtoken not in ignoretokens:
                        currentDAG[start] = (end, adjustedtoken)
                else:
                    # it can be "_End_Of_Sentence_" without further info
                    if "_End_Of_Sentence" not in info:
                        print "odd line:", linenum
                        print line

            #if linenum > 10000: break

#print sentences
#print token2count
print "no. of sentences", len(sentences)
test_sentences = [11, 21, 31, 111, 121, 131, 1001, 1011, 1021, 1031, 2010, 2020, 2030]
for sent in test_sentences:
    print " ".join(sentences[sent])

print [token for token in token2count if token[0] == "_"]


