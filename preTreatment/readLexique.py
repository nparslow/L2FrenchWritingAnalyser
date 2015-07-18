import operator

__author__ = 'nparslow'

import codecs
import json


# the goal here is to read the lexique file and retain only the information we might be interested in
# and also to compute the frequency rank(s)
# the problem is the difference in segmentation and categories which are hard to compare

lexique_filename_path = "/home/nparslow/Documents/AutoCorrige/vocabulary/AntProfiler/vocabProfil3or5" \
                        "/Lexique380/Bases+Scripts/Lexique380.txt"

# todo this is all a bit hard-wired
lexique = {}
with codecs.open(lexique_filename_path, 'r', encoding="latin-1") as f:
    header = True
    for line in f:
        if not header:
            elements = line.strip().split("\t")
            lemma = elements[3-1]
            catgram = elements[4-1]
            # for the moment only look at lemmas
            freqfilms = float(elements[7-1])
            freqbooks = float(elements[8-1])
            #freqrecognised = 0 # sometimes recognised frequency has not been measured
            #if elements[30-1] != "":
            #    freqrecognised = float(elements[30-1])

            if (lemma, catgram) in lexique:
                pass
                # we have a gramophone, so just add to it
                #lexique[(lemma,catgram)] = (lexique[(lemma,catgram)][0] + freqfilms,
                #                            lexique[(lemma,catgram)][1] + freqbooks,
                #                            lexique[(lemma,catgram)][2] + freqrecognised)
                #print "gramophone", lemma, catgram
            else:
                # json can't stock tuples as keys so transform to string with "_" as separator:
                # note there can be spaces in the lemma!!!!
                #print lemma + u"_" + catgram
                #lexique[lemma + u"_" + catgram] = (freqfilms, freqbooks, freqrecognised)
                lexique[lemma + u"_" + catgram] = (freqfilms, freqbooks)

        else:
            header = False

# now we need to sort and assign ranks to each lemma
for i in range(2):
    rankCounter = 1 # start with 1 not 0
    #print lexique.items()[0][1][i]
    #print(lexique.items()[0])
    for key, freqs in sorted(lexique.items(), key=lambda x: x[1][i], reverse=True ):
        #print key, freqs, list(freqs) + [rankCounter]
        freqs = tuple(list(freqs) + [rankCounter]) # add the rankCounter to the end of the tuple
        lexique[key] = freqs # this should be ok as we make a separate list by items
        if rankCounter < 100:
            print rankCounter, key, freqs
        rankCounter += 1



outfilename = "/home/nparslow/Documents/fouille_de_textes/projet/lund/lexique_ranks.json"
with open(outfilename, 'w') as outfile:
    json.dump(lexique, outfile)