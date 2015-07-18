__author__ = 'nparslow'

import json
import codecs


jsonfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/spelling.json"
with codecs.open(jsonfilename, mode="r", encoding="utf8") as jfile:
    spelling = json.load(jfile)

shortspelling = {}
for y in ["found", "notfound", "foreign", "changed"]:
    shortspelling[y] = {}
    print ""
    print y + " spelling:", sum(len(spelling[y][x]) for x in spelling[y])
    for x in spelling[y]:
        print x, len(spelling[y][x])
        print spelling[y][x]
        tags = x.split("_")
        if len(tags) == 1 and x in [u"DIA", u"OMI", u"PHO", u"SPC", u"SEP", u"EMP",
                                    u"INS", u"HPO", u"SPC", u"PHG", "SUB"]:
            shortspelling[y][x] = len(spelling[y][x])
        else:
            done = False
            for tag in [u"DIA", u"OMI", u"PHO", u"PHG", u"EMP",]:
                if tag in tags:
                    if tag + " +" not in shortspelling[y]: shortspelling[y][tag + " +"] = 0
                    shortspelling[y][tag+" +"] += len(spelling[y][x])
                    done = True
                    break
            if not done:
                if u"other" not in shortspelling[y]: shortspelling[y]["other"] = 0
                print "adding other", x, len(spelling[y][x])
                shortspelling[y][u"other"] += len(spelling[y][x])


print
for y in shortspelling:
    print ""
    print y + " spelling:"
    for x in shortspelling[y]:
        print x, shortspelling[y][x]


tag_counts = {}
#set([x for x in shortspelling[y] for y in shortspelling])
for y in shortspelling:
    for tag in shortspelling[y]:
        if tag not in tag_counts: tag_counts[tag] = 0
        tag_counts[tag] += shortspelling[y][tag]


print tag_counts
print
# add the times to put 'other' last
for tag in sorted(tag_counts.keys(), key= lambda x: tag_counts[x] * (x!="other"), reverse=True):
    print tag + " & ", " & ", # leave space for the example
    for y in ["found", "changed", "notfound"]:
        if tag in shortspelling[y]:
            print shortspelling[y][tag],
        else:
            print "-",
        print " & ",
    print sum(shortspelling[y][tag] if tag in shortspelling[y] else 0 for y in ["found", "changed", "notfound"]),
    print "\\\\"
print "\hline"
print "total &", " & "
for y in ["found", "changed", "notfound"]:
    print sum(shortspelling[y][x] if x in shortspelling[y] else 0 for x in tag_counts), "&",
print sum(shortspelling[y][x]
          if x in shortspelling[y] else 0 for x in shortspelling[y] for y in ["found", "changed", "notfound"]), "\\\\"
print "\hline"

