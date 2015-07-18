#!/usr/bin/python
__author__ = 'nparslow'

import os
import sys

#print "num args", len(sys.argv)
if len(sys.argv) > 3: # first argument is always the name of the script
    print len(sys.argv), "input arguments"
    print("Usage: ./corpusLoopShell corpus_base_directory output_base_dir")
    print("e.g. corpusLoopInria /home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS")
    print("                     /home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_ECRIT_VALETOPOULOS")
    exit(1)

# e.g. ./corpusLoopShell.py /home/nparslow/Documents/AutoCorrige/Corpora/test_Corp /home/nparslow/Documents/AutoCorrige/Corpora/test_CorpOut

inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/"
if len(sys.argv) > 1:
    inpath = sys.argv[1]
outpath = sys.argv[2]

def analyse( path ):
    if os.path.isdir(path):
        for element in os.listdir(path):
            analyse(os.path.join(path, element))
    else:
        analyseFile(path)

        '''
            in_full_element = os.path.join(inbasepath, relativepath, + element)
            if os.path.isfile(in_full_element):
                analyseFile(inbasepath + "/" + relativepath, element )
            else:
                # analyse the directory
                analyseDirectory(inbasepath, relativepath + "/" + element )
        '''

# will overwrite output
#def analyseFile( inbasepath, filename ):
def analyseFile( filename ):
    #in_full_filename = inbasepath + "/" + filename
    command = 'echo "corpus  ' + filename + ' ' + outpath + ' :utf8:robust:xml:dis:transform" | frmg_shell'
    print command
    os.system(command)

#analyseDirectory(inpath, ".")
analyse(inpath)
