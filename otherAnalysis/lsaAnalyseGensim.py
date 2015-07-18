#!/usr/bin/python
__author__ = 'nparslow'

from gensim import corpora, models, similarities
import os
import re
import sys
import json
import xml.etree.cElementTree as ET
import matplotlib.pyplot as plt


def analyseDirectory(inbasepath, results):
    for element in os.listdir(inbasepath ):
        in_full_element = inbasepath + os.sep + element # note don't use 'pathsep' as it's a colon

        if os.path.isfile(in_full_element):
            analyseFile(in_full_element, results)
        else:
            # analyse the directory
            analyseDirectory(in_full_element, results)

# doesn't overwrite output
def analyseFile( filename, results ):
    categoriesToKeep = {'v', 'nc', 'adj', 'adv'}

    basefilename = os.path.split(filename)[-1]
    #print basefilename
    info = re.search(r"(?<=FRMG)\w+(?=Sentence(\d+)\.xml)", basefilename)
    if info:
        student = info.group(0)
        sentenceNum = int(info.group(1))
        if student not in results: results[student] = {}

        tree = ET.parse(filename)

        sentence = []
        for node in tree.findall('node'):
            cat = node.get("cat")
            lemma = node.get("lemma")
            if cat in categoriesToKeep:
                sentence.append(lemma + "_" + cat)

        if len(sentence) > 0:
            results[student][sentenceNum] = sentence




def analyseSequence( sequence ):
    #sequence = ["aller_v", "parc_nc", "jouer_v"]
    vec_bow = dictionary.doc2bow(sequence)
    #print "sequence", sequence
    vec_lsi = lsi[vec_bow]
    #print("vec", vec_lsi)
    return vec_lsi

def analyseResults( results, lsi ):
    outResults = {}
    for student in results:
        if student not in outResults: outResults[student] = {}
        for sentenceNum in range(max(results[student])+1):
            # we need the current sentence and the previous one to have both been analysed
            if sentenceNum in results[student] and (sentenceNum-1) in results[student]:
                previousSentence = results[student][sentenceNum-1]
                currentSentence = results[student][sentenceNum]
                #print previousSentence, lsi[previousSentence]
                #prev_vec_bow = dictionary.doc2bow(previousSentence)
                prevProjection = analyseSequence(previousSentence)
                currProjection = analyseSequence(currentSentence)
                # the projection can have zero length if there are only lemmas in it not in the corpus used as a reference
                if len(prevProjection) > 0 and len(currProjection) > 0:
                    index = similarities.MatrixSimilarity([prevProjection])
                    # we put the prevProjection as a one element corpus
                    vec_lsi = lsi[currProjection]
                    sims = index[vec_lsi]
                    #print sentenceNum, sims
                    outResults[student][sentenceNum] = sims[0] # since corpus of 1, only 1 element

            else:
                # can't do anything
                pass
    return outResults

def displayResults( outResults):
    grouped = {}
    for student in outResults:
        if len(outResults[student]) > 0:
            print student[0], student, sum(outResults[student].values())/len(outResults[student].values())
            if student[0] not in grouped: grouped[student[0]] = []
            grouped[student[0]].append(
                (sum(outResults[student].values())/len(outResults[student].values()),
                 max(outResults[student].values()),
                 min(outResults[student].values())
                 )
            )
    return grouped



if __name__=='__main__':
    if len(sys.argv) != 1: # first argument is always the name of the script
        print len(sys.argv)
        print("Usage: ./lsaAnalyseGensimXML ")
        exit(1)
    #inpath = sys.argv[1]
    #outpath = sys.argv[2]
    #script = " ".join(sys.argv[1:])
    #script = sys.argv[1]

    dictionary = corpora.Dictionary.load('dictionary_test.dict')
    lsi = models.LsiModel.load('model_test.lsi')

    inbasepath = "/home/nparslow/Documents/fouille_de_textes/projet/lund/frmgXml"

    results = {}

    analyseDirectory(inbasepath, results)

    # now we have all the sentences we can analyse them:
    outResults = analyseResults(results, lsi)

    groupedResults = displayResults(outResults)

    # close to 1 is very similar, close to 0 is orthogonal, close to -1 is opposite

    #plt.boxplot([groupedResults[x][0] for x in ['A', 'B', 'C', 'D', 'E']])
    #plt.show()
    #plt.boxplot([groupedResults[x][1] for x in ['A', 'B', 'C', 'D', 'E']])
    #plt.show()
    #plt.boxplot([groupedResults[x][2] for x in ['A', 'B', 'C', 'D', 'E']])
    #plt.show()

    outfilename = "/home/nparslow/Documents/fouille_de_textes/projet/lund/lsaSentence.json"
    print outResults
    jsonResults = {}
    # the decimal/float numbers are not serializable so convert them to strings:
    for student in outResults:
        jsonResults[student] = {}
        for sentNum in outResults[student]:
            jsonResults[student][sentNum] = str(outResults[student][sentNum])
    print jsonResults
    with open(outfilename, 'w') as outfile:
        json.dump(jsonResults, outfile)