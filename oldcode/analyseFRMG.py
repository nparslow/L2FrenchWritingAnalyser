import json

__author__ = 'nparslow'

import os
import codecs

basedir = "/home/nparslow/PycharmProjects/DownloadCEFLE/lundOut/all/"

results = {}

def analyseDirectory( path, results ):
    for element in os.listdir(path):
        full_element = path + "/" + element
        if os.path.isfile(full_element):
            filenamebase = os.path.splitext(element)[0] # remove the extention
            results[filenamebase] = analyseFile(path, element) # should be a five-tuple

        else:
            # it's a directory:
            results[element] = {}
            analyseDirectory(full_element, results[element])



def analyseFile( path, filename ):
    # might be better to use subprocess.Popen() (as can use parallel)
    #os.system("/home/nparslow/Documents/AutoCorrige/vocabulary/perl/getVOCD.pl " + filename)
    full_filename = path + "/" + filename

    return get_parse_counts(full_filename)


def get_parse_counts( pathfilename ):
    nSentences = 0
    nSentencesSolution = 0
    nSentencesSolutionCorrected = 0
    nNoSolutionFull = 0
    nNoSolutionCorr = 0
    with codecs.open(pathfilename, "r", "latin-1") as infile:

        for line in infile:
            line = line.rstrip()
            #print line
            # for no solution found:
            # mode=corrected best=no
            # otherwise mode=full best=yes or mode=corrected best=yes
            if line.startswith("## sentence="):
                nSentences += 1
                #print "last chars", line[-1]
                if line.endswith("best=yes"):
                    #print "yo"
                    nSentencesSolution += 1
                    if u"mode=corrected" in line:
                        nSentencesSolutionCorrected += 1
                elif line.endswith("best=no"):
                    if u"mode=full" in line:
                        nNoSolutionFull += 1
                    elif u"mode=corrected" in line:
                        nNoSolutionCorr += 1
                    else:
                        print "Warning: strange (inner) line: ", line
                else:
                    print "Warning: strange (outer) line: ", line



    #print nSentences, nSentencesSolution, nSentencesSolutionCorrected
    #print round(1.0* nSentencesSolution/nSentences, 2), round(1.0* nSentencesSolutionCorrected/nSentences, 2)
    return nSentences, nSentencesSolution, nSentencesSolutionCorrected, nNoSolutionFull, nNoSolutionCorr


analyseDirectory(basedir, results)
print results

outfilename = "parse_tally.txt"
with open("/home/nparslow/PycharmProjects/DownloadCEFLE/" + outfilename, 'w') as outfile:
    json.dump(results, outfile)