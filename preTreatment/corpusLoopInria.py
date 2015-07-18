#!/usr/bin/python
import os
import sys

__author__ = 'nparslow'
#print "num args", len(sys.argv)
if len(sys.argv) != 4: # first argument is always the name of the script
    print len(sys.argv)
    print("Usage: ./corpusLoopInria corpus_base_directory output_base_dir script_to_call_and_parameters")
    print("e.g. corpusLoopInria /home/pinot/alpage/nparslow/Documents/lund/all ")
    exit(1)

# "frmg_lexer | frmg_parser - -loop -disamb -xml -passage"
# e.g. python corpusLoopInria.py ~/Documents/AutoCorrige/Corpora/CORPUS\ ECRIT\ VALETOPOULOS ~/Documents/AutoCorrige/Corpora/analysed_CORPUS_ECRIT_VALETOPOULOS/
#  "frmg_lexer | frmg_parser - -loop -disamb -xml -passage"

# on cognac, need to use erics versions:
# ./corpusLoopInria.py  /home/pinot/alpage/nparslow/Documents/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS
#  /home/pinot/alpage/nparslow/Documents/Corpora/analysed_CORPUS_ECRIT_VALETOPOULOS
# "/home/pinot/alpage/clergeri/Work/frmg/frmg_lexer | /home/pinot/alpage/clergeri/Work/frmg/frmg_parser - -loop -disamb -xml -passage"

# e.g.
# ./corpusLoopInria.py  /home/pinot/alpage/nparslow/Documents/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS
#  /home/pinot/alpage/nparslow/Documents/Corpora/analysed_CORPUS_ECRIT_VALETOPOULOS
# "frmg_lexer | frmg_parser - -loop -disamb -xml -passage"



inpath = sys.argv[1]
outpath = sys.argv[2]
script = " ".join(sys.argv[3:])
#script = sys.argv[3]
#print "script:"
#print script
#exit(0)

def analyseDirectory( inbasepath, outbasepath, relativepath ):
    outdir = outbasepath + "/" + relativepath
    # it's a directory:
    # make an output dir if necessary
    try:
        os.stat(outdir)
    except:
        os.mkdir(outdir)
    for element in os.listdir(inbasepath + "/" + relativepath):
        in_full_element = inbasepath + "/" + relativepath + "/" + element
        #out_full_element = outbasepath + "/" + relativepath + "/" + element
        if os.path.isfile(in_full_element):
            analyseFile(inbasepath + "/" + relativepath, outbasepath + "/" + relativepath, element )
        else:

            # analyse the directory
            #print "analysing directory: ", inba
            analyseDirectory(inbasepath, outbasepath, relativepath + "/" + element )

# doesn't overwrite output
def analyseFile( inbasepath, outbasepath, filename ):
    basefilename = os.path.splitext(filename)[0]
    outfile = outbasepath + "/" + basefilename + ".out"
    # keep changing the name until we find a filename that doesn't exist yet:
    outnum = 1
    while os.path.exists(outfile):
        outfile = outbasepath + "/" + basefilename + "_" + str(outnum) + ".out"
        outnum += 1
    in_full_filename = inbasepath + "/" + filename
    #print "running"
    #print "cat " + in_full_filename + " | " + script + " > " + outfile
    #print in_full_filename, script, outfile
    # the '"' is to allow for spaces in filenames:
    command = "cat " + '"' + in_full_filename + '"' + " | " + script + " > " + '"' + outfile + '"'
    print command
    os.system(command)

analyseDirectory(inpath, outpath, ".")


