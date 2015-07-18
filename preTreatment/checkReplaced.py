__author__ = 'nparslow'

import json
import codecs

corpusdirectory = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/divided/"

replacedFileName = "replaced.txt"
replacedwords = {}
with codecs.open(corpusdirectory + replacedFileName, 'r', encoding='utf-8') as replfile:
    replacedwords = json.load(replfile)

for cat in replacedwords:
    #print cat
    if cat not in [ "_OTHER_", "_ORDINAL_", "_FILENAME_", "_INITIALS_", "_ALLLOWER_", "_NUMUPPERMIX_",
                    "_CHURCH_", "_NUM_", "_MEASURE_", "_PUNCT_", "_FIRSTUPPER_", "_FOREIGN_",
                    "_MIXEDUPPERLOWER_", "_PARTIALISBN_", "_WEBSITE_"]:
        for word in replacedwords[cat]:
            print cat, word