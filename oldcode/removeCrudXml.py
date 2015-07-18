#!/usr/bin/python
__author__ = 'nparslow'

import codecs
import os
import sys

#filename = "/home/nparslow/Documents/fouille_de_textes/projet/lund/all/A/test2.xml"
#outBaseName = "/home/nparslow/Software/testSentence"

# e.g.
# python removeCrudXml.py /home/nparslow/Documents/fouille_de_textes/projet/lund/frmg
#  /home/nparslow/Documents/fouille_de_textes/projet/lund/frmgXml

'''
Takes the frmg output, Removes the non-xml stuff and splits into separate xml files
'''
if len(sys.argv) != 3: # first argument is always the name of the script
    print "Usage: ./removeCrudXml inputDirectory outputDirectory"
    print "e.g. removeCrudXml /home/nparslow/Documents/fouille_de_textes/projet/lund/all" \
          "/home/nparslow/Documents/fouille_de_textes/projet/lund/sentences"
    exit(1)
inpath = sys.argv[1]
outpath = sys.argv[2]


def processFile( baseInputDir, baseOutputDir, inFilename):
    pathedinfilename = baseInputDir + "/" + inFilename
    outBaseName = baseOutputDir + "/" + os.path.splitext(inFilename)[0] + "Sentence"

    with codecs.open(pathedinfilename, 'r') as infile:
        outfile = None
        amWriting = False
        outFileCounter = 0
        for line in infile:
            line = line.strip()

            #print line
            if "</dependencies>" == line[:15]:
                #print "CLOSING"
                outfile.write(line+"\n")
                outfile.close()
                amWriting = False
                outfile = None
            elif '<?xml version="1.0"  encoding="ISO-8859-1"?>' == line[0:45]:
                #print "OPENING"
                outfile = open(outBaseName + str(outFileCounter) + ".xml", "w")
                outFileCounter += 1
                amWriting = True
                outfile.write(line+"\n")
            elif amWriting:
                #print "WRITING"
                outfile.write(line+"\n")
        if outfile:
            outfile.close()


def analyseDirectory( inpath, outpath ):
    # make the out directory if need be:
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for element in os.listdir(inpath):
        full_element = inpath + "/" + element
        if os.path.isfile(full_element):
            processFile(inpath, outpath, element)
        else:
            # it's a directory:
            analyseDirectory(full_element, outpath + "/" + element)


analyseDirectory(inpath, outpath)
