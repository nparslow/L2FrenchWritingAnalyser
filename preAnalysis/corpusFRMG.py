#!/usr/bin/python
__author__ = 'nparslow'

import os
import sys


'''
Runs frmg over a corpus
'''
if len(sys.argv) != 3: # first argument is always the name of the script
    print "Usage: ./corpusFRMG inDirectory outDirectory"
    print "e.g. corpusFRMG /home/nparslow/Documents/fouille_de_textes/projet/lund/all" \
          " /home/nparslow/Documents/fouille_de_textes/projet/lund/frmg"
    exit(1)
inDirectory = sys.argv[1]
outDirectory = sys.argv[2]

# e.g.
# python removeCrudXml.py /home/nparslow/Documents/fouille_de_textes/projet/lund/frmg
#  /home/nparslow/Documents/fouille_de_textes/projet/lund/frmgXml


def analyseDirectory( inpath, outpath ):
    # make the out directory if need be:
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for element in os.listdir(inpath):
        full_element = inpath + "/" + element
        if os.path.isfile(full_element):
            analyseFile(inpath, outpath, element)
        else:
            # it's a directory:
            analyseDirectory(full_element, outpath+"/"+element)


def analyseFile( inpath, outpath, filename ):
    # might be better to use subprocess.Popen() (as can use parallel)
    os.system("frmg_lexer < " + inpath + "/" + filename + \
            " | frmg_parser -loop -depxml -multi -disamb > " + outpath + "/" + "FRMG" + filename)

analyseDirectory(inDirectory, outDirectory)