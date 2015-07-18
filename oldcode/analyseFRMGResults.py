__author__ = 'nparslow'

import json

results_frmg = {}

infilename = "parse_tally.txt"
with open("/home/nparslow/PycharmProjects/DownloadCEFLE/" + infilename, 'r') as infile:
    results_frmg = json.load(infile)

sumResults = {}


#for level in results_frmg:
for level in ['A', 'B', 'C', 'D', 'E']:
    nSentences = 0
    nSentencesSolution = 0
    nSentencesSolutionCorrected = 0
    nNoSolutionFull = 0
    nNoSolutionCorr = 0
    for student in results_frmg[level]:
        a,b,c,d,e = results_frmg[level][student]
        nSentences += a
        nSentencesSolution += b
        nSentencesSolutionCorrected += c
        nNoSolutionFull += d
        nNoSolutionCorr += e
    sumResults[level] = nSentences, nSentencesSolution, nSentencesSolutionCorrected
    print nSentences, nSentencesSolution, nSentencesSolutionCorrected, nNoSolutionFull, nNoSolutionCorr
    print level, round(1.0* nSentencesSolution/nSentences, 2), round(1.0* nSentencesSolutionCorrected/nSentences, 2), \
    round(1.0*nNoSolutionFull/nSentences, 2), round(1.0*nNoSolutionCorr/nSentences, 2)