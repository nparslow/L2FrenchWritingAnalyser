#!/usr/bin/python
import codecs
import os
import json
import re
import sys
import runMElt

__author__ = 'nparslow'


#print "num args", len(sys.argv)
if len(sys.argv) > 3: # first argument is always the name of the script
    print len(sys.argv), "input arguments"
    print("Usage: ./corpusLoopMElt corpus_base_directory output_base_dir")
    print("e.g. corpusLoopMElt /home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS")
    print("                    /home/nparslow/Documents/AutoCorrige/Corpora/melted_CORPUS_ECRIT_VALETOPOULOS")
    exit(1)

#inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker"
#inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellCheckerCorrected"
inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_CEFLE"
inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_CEFLE/Arvid"
#inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_ECRIT_VALETOPOULOS"
if len(sys.argv) > 1:
    inpath = sys.argv[1]
#outpath = "/home/nparslow/Documents/AutoCorrige/Corpora/melted_SpellChecker"
#outpath = "/home/nparslow/Documents/AutoCorrige/Corpora/melted_SpellCheckerCorrected"
outpath = "/home/nparslow/Documents/AutoCorrige/Corpora/melted_CORPUS_CEFLE"
#outpath = "/home/nparslow/Documents/AutoCorrige/Corpora/melted_CORPUS_ECRIT_VALETOPOULOS"
if len(sys.argv) > 2:
    outpath = sys.argv[2]

outjsonfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/outputs/melted_CORPUS_CEFLE_blah.json"
#outjsonfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/outputs/melted_CORPUS_ECRIT_VALETOPOULOS.json"

def loadTokensFile( filename ):
    tokens = []
    with codecs.open(filename, mode="r", encoding="utf8") as tfile:
        for line in tfile:
            if "\t" in line:
                num, token = line.split("\t")
                tokens.append(token.strip())
    return tokens

def analyse( path, meltedCorpus ):
    if os.path.isdir(path):
        for element in os.listdir(path):
            analyse(os.path.join(path, element), meltedCorpus)
    else:
        analyseFile(path, meltedCorpus)
    #return  meltedCorpus


# will overwrite output
def analyseFile( filename, meltedCorpus ):
    #print "analysing file", filename
    baseFileName = os.path.basename(filename)
    #command = 'echo "corpus  ' + filename + ' ' + outpath + ' :utf8:robust:xml:dis:transform" | frmg_shell'
    try:
        filebase, sentNum = re.search(ur'(\w+)\.E(\d+)', baseFileName, flags=re.UNICODE).groups()
        sentNum = int(sentNum)
    except:
        # not a valid tokens file so just return
        return
    baseFileName, fileExtension = os.path.splitext(baseFileName)
    print "looking at", filename
    if fileExtension == ".tokens":
        tokens = loadTokensFile(filename)
        print tokens
        melted = runMElt.getMElt(tokens)
        print melted
        with codecs.open(os.path.join(outpath, baseFileName + ".melted"), mode="w", encoding="utf8") as ofile:
            for m in melted:
                ofile.write("\t".join([unicode(x) for x in m]) + "\n")
        if filebase not in meltedCorpus: meltedCorpus[filebase] = {}
        print filebase, sentNum, melted
        meltedCorpus[filebase][sentNum] = melted

        #print meltedCorpus

        #exit(10)


#analyseDirectory(inpath, ".")

meltedCorpus = {}
analyse(inpath, meltedCorpus)

print meltedCorpus
#outjsonfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/outputs/melted_orig.json"
#outjsonfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/outputs/melted_corr.json"
with codecs.open(outjsonfilename, mode="w", encoding="utf8") as ojfile:
    json.dump(meltedCorpus, ojfile)
