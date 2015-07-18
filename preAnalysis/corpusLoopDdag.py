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
    print("Usage: ./corpusLoopDdag corpus_base_directory output_base_dir")
    print("e.g. corpusLoopDdag /home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS")
    print("                    /home/nparslow/Documents/AutoCorrige/Corpora/ddaged_CORPUS_ECRIT_VALETOPOULOS")
    exit(1)

#inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellChecker"
#inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellCheckerCorrected"
#inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_CEFLE"
inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_ECRIT_VALETOPOULOS"
if len(sys.argv) > 1:
    inpath = sys.argv[1]
#outpath = "/home/nparslow/Documents/AutoCorrige/Corpora/ddaged_SpellChecker"
#outpath = "/home/nparslow/Documents/AutoCorrige/Corpora/ddaged_SpellCheckerCorrected"
#outpath = "/home/nparslow/Documents/AutoCorrige/Corpora/ddaged_CORPUS_CEFLE"
outpath = "/home/nparslow/Documents/AutoCorrige/Corpora/ddaged_CORPUS_ECRIT_VALETOPOULOS"
if len(sys.argv) > 2:
    outpath = sys.argv[2]


def analyse( path ):
    if os.path.isdir(path):
        for element in os.listdir(path):
            analyse(os.path.join(path, element))
    else:
        analyseFile(path)
    #return  meltedCorpus


# will overwrite output
def analyseFile( filename ):
    #print "analysing file", filename
    baseFileName = os.path.basename(filename)

    baseFileName, fileExtension = os.path.splitext(baseFileName)
    print "looking at", filename
    ddagcommand = "~/exportbuild/src/sxpipe/sxpipe-tokenise | dag2ddag | dag2udag"
    if fileExtension == ".txt":
        command = 'cat ' + filename + ' | ' + ddagcommand + ' > ' + os.path.join(outpath, baseFileName + ".ddag")
        print command
        os.system(command)



if "/usr/local/bin/" not in os.environ['PATH']:
        os.environ['PATH'] += ":/usr/local/bin/"
if "/home/nparslow/exportbuild/bin" not in os.environ['PATH']:
        os.environ['PATH'] += ":/home/nparslow/exportbuild/bin"

analyse(inpath)

# NB some ddag errors come up like:
'''
, line 47: column 1102: Error:	"%word" is inserted before "?".
, line 47: column 1103: Error:	"%word" is inserted before "?".
, line 48: column 1102: Error:	"%word" is inserted before "?".
, line 48: column 1103: Error:	"%word" is inserted before "?".
WARNING (comments_cleaner.pl): Format error: % Next sentence was not processed (too long)
'''