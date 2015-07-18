

import json
import codecs

__author__ = 'nparslow'


outfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/outputs/learner_vocab_combined.json"

vocab2count = {}
with codecs.open(outfilename, 'r', encoding="utf8") as infile:
    vocab2count = json.load( infile)


lowervocab2count = {}
for token in vocab2count:
    if token.lower() not in lowervocab2count: lowervocab2count[token.lower()] = 0
    lowervocab2count[token.lower()] += vocab2count[token]


for mincount in range(10):
    print "cutoff", str(mincount)
    print "vocab size with caps", len([x for x in vocab2count if vocab2count[x] > mincount])

    print "vocab size no caps", len([x for x in lowervocab2count if lowervocab2count[x] > mincount])

mincount = 1

for x in sorted(lowervocab2count):
    print x, lowervocab2count[x]
