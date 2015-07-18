__author__ = 'nparslow'


import json
import codecs
import os

jsonfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellCheckerJson/entry.json"
outcorpus = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellCheckerCorrected"

with codecs.open(jsonfilename, mode="r", encoding='utf8') as jsonfile:
    entries = json.load(jsonfile)

for entry in entries:
    #print entry
    entrynum = entry[0]
    original = entry[1]
    corrected = entry[2]
    if original == corrected:
        print "zero changes", entrynum, original
        # only 6 times the whole entry is unchanged
    with codecs.open(os.path.join(outcorpus, "entrycorrected_" + str(entrynum)), mode='w', encoding='utf8') as outfile:
        outfile.write(corrected)

