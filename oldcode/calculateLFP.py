__author__ = 'nparslow'

import os
import codecs
import re
import math
import json

import xml.etree.cElementTree as ET

import matplotlib.pyplot as plt
import numpy as np
import operator

# frequency directory contains files of the form:
# lemma frequency (with a tab between them), or just lemma
# individual file names must include the grouping in brackets, and they must be the only brackets in the filename
# and between them must be a number only or leftover
# the 'leftover' file should have one line, containing a tab followed by the frequency of all non-mentioned
# words. the leftover group will have number '-1'
frequency_groups_dir = "/home/nparslow/Documents/AutoCorrige/vocabulary/AntProfiler/vocabProfil3or5/lists"

def load_dicts(frequency_groups_dir, word2groupANDfrequency):

    for filename in os.listdir(frequency_groups_dir):

        # we use the inner brackets to grab the number only, e.g. if (5) is group(0), 5 is group(1)
        group = re.search(ur'\((\d+)\)', filename).group(1)
        if group != "leftover":
            group = int(group)
        else:
            group = -1
        #group = int(group) if group != "leftover" else group = -1

        with codecs.open(frequency_groups_dir + os.path.sep + filename, 'r') as f:
            for line in f:
                lemma = line.strip()
                frequency = 0;
                if "\t" in line:
                    lemma, frequency = lemma.split("\t")
                word2groupANDfrequency[lemma] = (group, frequency)

# the file has format expression rating (with a tab in between), expression can be multi-word
# and there is always a space first on the line
# we don't have the raw frequency info, but we retain the same structure as above for load_dicts
def load_teacher_ratings(teacher_ratings_filename, word2groupANDfrequency):
    with codecs.open(teacher_ratings_filename, 'r') as f:
        for line in f:
            lemma_rating = line.strip()
            #print lemma_rating.split("\t")
            lemma, rating = lemma_rating.split("\t")
            word2groupANDfrequency[lemma] = (rating, 0)


# TODO need to P_Lex too
# runs over a tokenised file, with 2 empty lines between sentences
# if there are existing entries in group2count, it will add to them
def getLFP_parsed( filename, word2groupANDfrequency, group2countANDsumlogfreq):

    # include a leftover group if there's none there already, will include all words not in the frequency profile:
    leftoverGroup = -1
    if leftoverGroup not in word2groupANDfrequency: word2groupANDfrequency[""] = (leftoverGroup, 0)

    tree = ET.parse(filename)

    for node in tree.findall('node'):
        #treeInfo = node.get("tree")
        lemma = node.get("lemma")
        #print treeInfo, lemma

    #with codecs.open(filename, 'r') as f:
    #    for line in f.lines():
    #        # need to remove crap from line
    #        lemma = "le" #

        if lemma not in ["", "cln"]: # TODO are there others apart from these 2?
            # add info to counts:
            group, frequency = -1, 0
            if lemma in word2groupANDfrequency:
                group, frequency = word2groupANDfrequency[lemma]
            else:
                group, frequency = leftoverGroup, word2groupANDfrequency[""][1]
            #group, frequency = word2groupANDfrequency[lemma] if lemma in word2groupANDfrequency \
            #    else leftoverGroup, word2groupANDfrequency[""][1]
            #print "yo", group, "bo",  frequency
            if group not in group2countANDsumlogfreq : group2countANDsumlogfreq[group] = (0,0)
            logfreq = math.log(frequency) if frequency > 0 else 0 # TODO with 0, counts same for words that never appear and words that appear only once
            # todo prob shouldn't use tuples here, as they need continual deletion
            #print "before", group,  group2countANDsumlogfreq[group]
            group2countANDsumlogfreq[group] = (group2countANDsumlogfreq[group][0] + 1, \
                                                group2countANDsumlogfreq[group][1] + logfreq)
            #print "after", group, group2countANDsumlogfreq[group]

def getLFP_nonparsed( filename, word2groupANDfrequency, group2countANDsumlogfreq):

    # include a leftover group if there's none there already, will include all words not in the frequency profile:
    leftoverGroup = -1
    if leftoverGroup not in word2groupANDfrequency: word2groupANDfrequency[""] = (leftoverGroup, 0)

    with codecs.open(filename, 'r') as f:
        for line in f:
            # need to remove crap from line
            lemma = "le" # TODO

            # add info to counts:
            group, frequency = word2groupANDfrequency[lemma] if lemma in word2groupANDfrequency \
                else leftoverGroup, word2groupANDfrequency[""][1]
            if group not in group2countANDsumlogfreq : group2countANDsumlogfreq[group] = (0,0)
            logfreq = math.log(frequency) if frequency > 0 else 0
            # prob shouldn't use tuples here, as they need continual deletion
            group2countANDsumlogfreq[group] = group2countANDsumlogfreq[group][0] + 1, \
                                                group2countANDsumlogfreq[group][1] + logfreq





def analyseDirectory( inpath, word2groupANDfrequency, results, analysis_function ):
    for element in os.listdir(inpath):
        full_element = inpath + "/" + element
        # create the sub-dictionary to match the directory structure
        #results[element] = {}
        if os.path.isfile(full_element):
            student = re.search(r"(?<=FRMG)\w+(?=Sentence\d+\.xml)", element).group(0)
            #if "Agnes" in element: # todo
            if student not in results: results[student] = {}
            analysis_function(full_element, word2groupANDfrequency, results[student])
        else:
            # it's a directory:
            results[element] = {}
            analyseDirectory(full_element, word2groupANDfrequency, results[element], analysis_function)



lemma2ratingANDfreq = {}
load_teacher_ratings(
    "/home/nparslow/Documents/AutoCorrige/vocabulary/Tidball_Treffers-Daller/word_rating_for_teacher1_cleaned.txt",
    lemma2ratingANDfreq)

#print lemma2ratingANDfreq

word2groupANDfrequency = {}
load_dicts(frequency_groups_dir, word2groupANDfrequency)

#print word2groupANDfrequency


group2countANDsumlogfreq ={}
#getLFP_parsed( "/home/nparslow/Documents/fouille_de_textes/projet/lund/frmgXml/A/FRMGAgnesSentence0.xml",
#                  word2groupANDfrequency, group2countANDsumlogfreq)

#print group2countANDsumlogfreq

analyseDirectory("/home/nparslow/Documents/fouille_de_textes/projet/lund/frmgXml",
                 #word2groupANDfrequency,
                 lemma2ratingANDfreq, # remember multiwords are possible, so won't be counted
                 group2countANDsumlogfreq,
                 getLFP_parsed)

print lemma2ratingANDfreq
print group2countANDsumlogfreq

outputs = {}
for level in sorted(group2countANDsumlogfreq.keys()):
    outputs[level] = []
    for student in group2countANDsumlogfreq[level]:
        n_recognised_words = sum([y[0] for x,y in group2countANDsumlogfreq[level][student].iteritems() if x > 0])
        # points should probably be for unique lemmas or maybe not, (currently double-counted) but how to account for length of text?
        points = sum([int(x)*y[0] for x,y in group2countANDsumlogfreq[level][student].iteritems() if x > 0]) / (1.0*n_recognised_words)
        print student, round(points,2), sorted(group2countANDsumlogfreq[level][student].iteritems(), key= lambda x:x[0])
        #for group in sorted(group2countANDsumlogfreq[level][student].iterkeys()):
        #    print group, group2countANDsumlogfreq[level][student][group]

        for group in group2countANDsumlogfreq[level][student]:
            outputs[level].append(points)


outfilename = "/home/nparslow/Documents/fouille_de_textes/projet/lund/lfp_points.json"
with open(outfilename, 'w') as outfile:
    json.dump(outputs, outfile)


def sortAndPlot( indict ):
    #print indict
    #res = sorted(indict.iteritems(), key=operator.itemgetter(0))
    #order = ["A", "B", "C", "D", "E" ]
    #plt.bar(np.arange(len(res)), [math.log(y,10) for x,y in res])
    #print res
    plt.boxplot([indict[x] for x in ['A', 'B', 'C', 'D', 'E']])
    plt.show()

print outputs

sortAndPlot(outputs)
