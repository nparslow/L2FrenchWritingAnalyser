__author__ = 'nparslow'

#!/usr/bin/python
__author__ = 'nparslow'

import os
import sys

#print "num args", len(sys.argv)
if len(sys.argv) > 2: # first argument is always the name of the script
    print len(sys.argv), "input arguments"
    print("Usage: ./yaencodeAll corpus_base_directory")
    print("e.g. ./yaencodeAll /home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS")
    exit(1)

# e.g. ./corpusLoopShell.py /home/nparslow/Documents/AutoCorrige/Corpora/test_Corp /home/nparslow/Documents/AutoCorrige/Corpora/test_CorpOut

inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS"
if len(sys.argv) > 1:
    inpath = sys.argv[1]

def analyse( path ):
    if os.path.isdir(path):
        for element in os.listdir(path):
            analyse(os.path.join(path, element))
    else:
        analyseFile(path)

# will overwrite output
def analyseFile( filename ):
    command = 'cat ' + filename + ' | yadecode -u -l=fr > ' + " this_doesnt_work.txt"
    print command
    os.system(command)

#analyseDirectory(inpath, ".")
analyse(inpath)
