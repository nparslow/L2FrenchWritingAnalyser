__author__ = 'nparslow'

import codecs

basedir = "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_ECRIT_VALETOPOULOS/CORPUS_CENTRE-FLE/"
filename = "centreFLE_2006_TL_CFLETP_4_Activite2_OLIAIY_SHIRAZY_Shervin.txt"

outbasedir = "/home/nparslow/Documents/AutoCorrige/Corpora/test_CorpOut/"
outfilename = "modified.txt"

with codecs.open(basedir + filename, encoding='Windows-1250') as infile:
    with codecs.open(outbasedir + outfilename, mode="w", encoding="utf-8") as outfile:
        for line in infile:
            print line
            print type(line)
            outfile.write(line)