# coding=utf-8

from compareCorrectedCorpus import getFinalTokenFormsAndTreesAndWeight
import os
import glob

import classifyVerbs

__author__ = 'nparslow'

xmlfiles = [
"analysed_SpellCheckerCorrected/entrycorrected_40/0/0/0/entrycorrected_40.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_40/0/0/0/entrycorrected_40.E4.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_40/0/0/0/entrycorrected_40.E5.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_41/0/0/0/entrycorrected_41.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_41/0/0/0/entrycorrected_41.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_41/0/0/0/entrycorrected_41.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_42/0/0/0/entrycorrected_42.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_42/0/0/0/entrycorrected_42.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_42/0/0/0/entrycorrected_42.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_42/0/0/0/entrycorrected_42.E4.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_43/0/0/0/entrycorrected_43.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_43/0/0/0/entrycorrected_43.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_43/0/0/0/entrycorrected_43.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_43/0/0/0/entrycorrected_43.E4.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_44/0/0/0/entrycorrected_44.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_44/0/0/0/entrycorrected_44.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_44/0/0/0/entrycorrected_44.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_45/0/0/0/entrycorrected_45.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_45/0/0/0/entrycorrected_45.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_45/0/0/0/entrycorrected_45.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_46/0/0/0/entrycorrected_46.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_46/0/0/0/entrycorrected_46.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_47/0/0/0/entrycorrected_47.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_47/0/0/0/entrycorrected_47.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_48/0/0/0/entrycorrected_48.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_48/0/0/0/entrycorrected_48.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_49/0/0/0/entrycorrected_49.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_50/0/0/0/entrycorrected_50.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_5/0/0/0/entrycorrected_5.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_51/0/0/0/entrycorrected_51.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_51/0/0/0/entrycorrected_51.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_51/0/0/0/entrycorrected_51.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_52/0/0/0/entrycorrected_52.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_52/0/0/0/entrycorrected_52.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_53/0/0/0/entrycorrected_53.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_53/0/0/0/entrycorrected_53.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_54/0/0/0/entrycorrected_54.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_54/0/0/0/entrycorrected_54.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_55/0/0/0/entrycorrected_55.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_55/0/0/0/entrycorrected_55.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_56/0/0/0/entrycorrected_56.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_56/0/0/0/entrycorrected_56.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_57/0/0/0/entrycorrected_57.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_58/0/0/0/entrycorrected_58.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_59/0/0/0/entrycorrected_59.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_60/0/0/0/entrycorrected_60.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_60/0/0/0/entrycorrected_60.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_6/0/0/0/entrycorrected_6.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_61/0/0/0/entrycorrected_61.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_61/0/0/0/entrycorrected_61.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_61/0/0/0/entrycorrected_61.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_62/0/0/0/entrycorrected_62.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_62/0/0/0/entrycorrected_62.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_63/0/0/0/entrycorrected_63.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_65/0/0/0/entrycorrected_65.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_66/0/0/0/entrycorrected_66.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_67/0/0/0/entrycorrected_67.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_68/0/0/0/entrycorrected_68.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_69/0/0/0/entrycorrected_69.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_69/0/0/0/entrycorrected_69.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_70/0/0/0/entrycorrected_70.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_70/0/0/0/entrycorrected_70.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_70/0/0/0/entrycorrected_70.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_7/0/0/0/entrycorrected_7.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_71/0/0/0/entrycorrected_71.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_71/0/0/0/entrycorrected_71.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_71/0/0/0/entrycorrected_71.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_72/0/0/0/entrycorrected_72.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_72/0/0/0/entrycorrected_72.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_73/0/0/0/entrycorrected_73.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_73/0/0/0/entrycorrected_73.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_74/0/0/0/entrycorrected_74.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_75/0/0/0/entrycorrected_75.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_76/0/0/0/entrycorrected_76.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_77/0/0/0/entrycorrected_77.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_78/0/0/0/entrycorrected_78.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_78/0/0/0/entrycorrected_78.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_78/0/0/0/entrycorrected_78.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_79/0/0/0/entrycorrected_79.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_80/0/0/0/entrycorrected_80.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_8/0/0/0/entrycorrected_8.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_81/0/0/0/entrycorrected_81.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_82/0/0/0/entrycorrected_82.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_83/0/0/0/entrycorrected_83.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_83/0/0/0/entrycorrected_83.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_84/0/0/0/entrycorrected_84.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_84/0/0/0/entrycorrected_84.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_84/0/0/0/entrycorrected_84.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_85/0/0/0/entrycorrected_85.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_86/0/0/0/entrycorrected_86.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_86/0/0/0/entrycorrected_86.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_87/0/0/0/entrycorrected_87.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_88/0/0/0/entrycorrected_88.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_88/0/0/0/entrycorrected_88.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_89/0/0/0/entrycorrected_89.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_9/0/0/0/entrycorrected_9.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_91/0/0/0/entrycorrected_91.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_92/0/0/0/entrycorrected_92.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_92/0/0/0/entrycorrected_92.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_93/0/0/0/entrycorrected_93.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_93/0/0/0/entrycorrected_93.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_93/0/0/0/entrycorrected_93.E3.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_94/0/0/0/entrycorrected_94.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_94/0/0/0/entrycorrected_94.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_95/0/0/0/entrycorrected_95.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_96/0/0/0/entrycorrected_96.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_97/0/0/0/entrycorrected_97.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_98/0/0/0/entrycorrected_98.E1.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_98/0/0/0/entrycorrected_98.E2.dep.xml",
"analysed_SpellCheckerCorrected/entrycorrected_99/0/0/0/entrycorrected_99.E1.dep.xml"]


xmlfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellCheckerCorrected/entrycorrected_342/0/0/0/entrycorrected_342.E4.dep.xml"
xmlfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellCheckerCorrected/entrycorrected_334/0/0/0/entrycorrected_334.E2.dep.xml"
xmlfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellCheckerCorrected/entrycorrected_367/0/0/0/entrycorrected_367.E1.dep.xml"


def addToCount( info2count, base, tense, mood):
    if tense not in info2count[base]: info2count[base][tense] = {}
    if mood not in info2count[base][tense]: info2count[base][tense][mood] = 0
    info2count[base][tense][mood] += 1

info2count = {
    "single": {},
    "aux": {},
    "compound":{},
    "clause": {},
}

#for xmlfilename in xmlfiles:
#for xmlfilename in glob.glob('/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellCheckerCorrected/entrycorrected_*/0/0/0/entrycorrected_*.E*.dep.xml'):
for xmlfilename in glob.glob('/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellCheckerCorrected/entrycorrected_394/0/0/0/entrycorrected_*.E*.dep.xml'):

    #xmlfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/" + xmlfilename
    print "analysing", xmlfilename
    tok2finalforms, tok2lemmacats, verb2info, trees, (weight, maxweight) = getFinalTokenFormsAndTreesAndWeight(xmlfilename)
    print
    print "verb2info"
    print verb2info
    print

    info  = classifyVerbs.classifyVerbs(verb2info)

    print "info"
    print info
    print
    '''
    for verb, info in verb2info.items():

        if len(info) == 1:
            tense = "notense"
            if "tense" in info[0]:
                tense = info[0]["tense"]
            mood = "infinitive" # sometimes mood is not there
            if "mode" in info[0]:
                mood = info[0]["mode"]
            if mood == "indicative" and tense == "notense":
                mood = "infinitive" # coordination screws it up
            addToCount(info2count, "single", tense, mood)
            if "extraction" in info[0]:
                base = "clause"
                extr = info[0]["extraction"]
                xarg = "noxarg"
                if "xarg" in info[0]:
                    xarg = info[0]["xarg"]
                addToCount(info2count, base, extr, xarg)

        elif len(info) ==2:
            v1info, v2info = info
            base = "compound"
            if verb in [u"être", u"avoir"]:
                base = "aux"
            tense = "notense"
            if "tense" in info[1]:
                tense = info[1]["tense"]
            mood = "infinitive" # sometimes mood is not there
            if "mode" in info[1]:
                mood = info[1]["mode"]
            addToCount(info2count, base, tense, mood)
            if mood == "indicative" and tense == "notense":
                mood = "infinitive" # coordination screws it up
            if "extraction" in info[1]:
                base = "clause"
                extr = info[1]["extraction"]
                xarg = "noxarg"
                if "xarg" in info[1]:
                    xarg = info[1]["xarg"]
                addToCount(info2count, base, extr, xarg)
        else:
            assert("problem chain of 3 verbs!")




        #tinfo = tuple(tuple(x) for x in info)
        print info
        #if tinfo not in info2count: info2count[tinfo] = 0
        #info2count[tinfo] += 1
    '''

print
print "final output:"
for x in info2count:
    print x, info2count[x]
    for y in info2count[x]:
        print y, info2count[x][y]

