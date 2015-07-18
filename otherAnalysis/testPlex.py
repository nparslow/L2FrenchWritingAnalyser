__author__ = 'nparslow'

from compareCorrectedCorpus import getFinalTokenFormsAndTreesAndWeight

import calcPLex

print "loading freq info"
lemmacat2freqrank = calcPLex.loadLemmaCat2freqrank()


# testxmls = ["analysed_SpellChecker/entry_81/0/0/0/entry_81.E1.dep.xml"

testxmls = [
    "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_350/0/0/0/entry_350.E1.dep.xml",
    "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_350/0/0/0/entry_350.E5.dep.xml",
    "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_350/0/0/0/entry_350.E2.dep.xml",
    "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_350/0/0/0/entry_350.E6.dep.xml",
    "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_350/0/0/0/entry_350.E3.dep.xml",
    "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_350/0/0/0/entry_350.E7.dep.xml",
    "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_350/0/0/0/entry_350.E4.dep.xml",
    ]

wordforms = []
for testxml in testxmls:
    print "loading xml", testxml
    tok2finalforms, tok2lemmacats, verb2info, trees, (weight, maxweight) = getFinalTokenFormsAndTreesAndWeight(testxml)
    # each tok2lemmacat goes to a list to 2-tuples
    # print tok2lemmacats.values()
    for lemmacats in tok2lemmacats.values():
        wordforms.extend([x[0] + u"_" + x[1] for x in lemmacats])

print wordforms
print "tokens", len(wordforms)
print "types", len(set(wordforms))
popt, pcov = calcPLex.calcPLex( wordforms, lemmacat2freqrank)

print "popt", popt
print "pcov", pcov

print "S"
popt, pcov = calcPLex.calcS( wordforms, lemmacat2freqrank)

print "popt", popt
print "pcov", pcov


vocd = calcPLex.getVOCD( wordforms )
mtld = calcPLex.getMTLD( wordforms )

print "vocd:", vocd
print "mtld:", mtld


