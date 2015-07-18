__author__ = 'nparslow'

import operator

import codecs
import json


# the goal here is to read the .lemma file and calculate/stock the frequency rank(s)
# CPL = large mixed corpus, wiki, est-france etc.
freqs_filename_path = "/home/nparslow/Documents/AutoCorrige/vocabulary/frmg_frequencies/" \
                        "CPL.lemma"

# todo this is all a bit hard-wired
# note that the lemma can include spaces, e.g. 'V. L'Homme:_Uv_np'
lexique = {}
with codecs.open(freqs_filename_path, 'r', encoding="latin-1") as f:
    # assumes no header in file
    rank = 1
    for line in f:
        lemma_cat, freq = line.strip().split("\t")
        # don't actually need to split here: need something more complicated too,
        # punctuation is e.g. ':__' i.e. punct + two underscores or can be e.g. '._poncts'
        # and sometimes things like 'Bourgogne:_LOCATION_np'
        #lemma, cat = lemma_cat.rsplit("_",1)

        if lemma_cat in lexique:
            print "double entry", lemma_cat, line.rstrip()
            # can come in here due to a space before the lemma e.g. ' parce:_LOCATION_np'
            # we ignore these as they may change the rank for everything and so require reranking
        else:
            # stock both frequency and rank (we assume list is already ordered)
            lexique[lemma_cat] = (int(freq), rank)
        rank += 1


outfilename = "/home/nparslow/Documents/fouille_de_textes/projet/lund/frmg_freq_ranks.json"
with open(outfilename, 'w') as outfile:
    json.dump(lexique, outfile)