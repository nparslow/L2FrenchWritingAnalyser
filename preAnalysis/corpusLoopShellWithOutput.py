#!/usr/bin/python
__author__ = 'nparslow'

import os
import sys
import subprocess

#print "num args", len(sys.argv)
if len(sys.argv) > 3: # first argument is always the name of the script
    print len(sys.argv), "input arguments"
    print("Usage: ./corpusLoopShell corpus_base_directory output_base_dir")
    print("e.g. corpusLoopInria /home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS")
    print("                     /home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_ECRIT_VALETOPOULOS")
    exit(1)

# e.g. ./corpusLoopShell.py /home/nparslow/Documents/AutoCorrige/Corpora/test_Corp /home/nparslow/Documents/AutoCorrige/Corpora/test_CorpOut

inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS"
#inpath = "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_CEFLE"
#inpath = '/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_LITTAVANCE'
if len(sys.argv) > 1: inpath = sys.argv[1]
outpath = "/home/nparslow/Documents/AutoCorrige/Corpora/tokenised/CORPUS_ECRIT_VALETOPOULOS"
#outpath = "/home/nparslow/Documents/AutoCorrige/Corpora/tokenised/CORPUS_CEFLE"
#outpath = "/home/nparslow/Documents/AutoCorrige/Corpora/tokenised/CORPUS_LITTAVANCE"
if len(sys.argv) > 2: outpath = sys.argv[2]

sys.path.append("/home/nparslow/exportbuild/bin/")

def analyse( path, outpath ):
    if os.path.isdir(path):
        for element in os.listdir(path):
            analyse(os.path.join(path, element), outpath)
    else:
        analyseFile(path, outpath)


# will overwrite output
# todo make directory if it doesn't exist
# note : have to remove INTITULES
def analyseFile( filename, outpath ):

    print "processing:", filename
    basefileName, fileExtension = os.path.splitext(filename)
    basefileName =  os.path.basename(basefileName) # remove the directories
    #outfilename = os.path.join(outpath, basefileName + ".ddag" )
    outfilename = os.path.join(outpath, basefileName + ".ddag" )

    #command = 'cat ' + filename  + ' | sxpipe | ' \
    #                              'dag2ddag | ' \
    #                              'dag2udag > ' + outfilename
    command = 'cat ' + filename  + ' | yarecode -u -l=fr | ' \
                                   '/home/nparslow/exportbuild/src/sxpipe/sxpipe-tokenise | ' \
                                   'dag2ddag | ' \
                                   'dag2udag > ' + outfilename

    os.environ['PATH'] += ":/home/nparslow/exportbuild/bin/"
    os.system(command)

    #exit(0)

analyse(inpath, outpath)
