#!/usr/bin/python
__author__ = 'nparslow'

import xml.etree.cElementTree as ET
import os
import json
import sys

'''
loops over the files created by remove crud and converts the output to a json
retains the directory hierarchy as dictionary hierachy in json
'''
if len(sys.argv) != 3: # first argument is always the name of the script
    print "Usage: ./AnalyseFRMGxml base_directory output_filename"
    print "e.g. python AnalyseFRMGxml.py  /home/nparslow/Documents/fouille_de_textes/projet/lund/frmgXml" \
          " /home/nparslow/Documents/fouille_de_textes/projet/lund/frmgStats.json"
    exit(1)
path = sys.argv[1]
outfilename = sys.argv[2]



# TODO work out how to combine into a sentence-level measure ?

def processFile( pathFileName, results):
    #tree = ET.parse("/home/nparslow/Software/test_again3.xml")
    #tree = ET.parse("/home/nparslow/Documents/fouille_de_textes/projet/lund/frmgXml/A/FRMGAugustSentence9.xml")
    tree = ET.parse(pathFileName)

    #distribution_trees = {}

    for node in tree.findall('node'):
        treeInfo = node.get("tree")
        lemma = node.get("lemma")
        #print treeInfo, lemma

        if treeInfo[0].isdigit():
            number_types = treeInfo.split()
            treeNum = number_types[0]
            #for x in number_types[1:]:
            #    print "type", x
            if treeNum not in results: results[treeNum] = 0
            results[treeNum] += 1

def analyseDirectory( inpath, results ):
    for element in os.listdir(inpath):
        full_element = inpath + "/" + element
        # create the sub-dictionary to match the directory structure
        results[element] = {}
        if os.path.isfile(full_element):
            processFile(full_element, results[element])
        else:
            # it's a directory:
            analyseDirectory(full_element, results[element])


results = {}
analyseDirectory(path, results)

# make the out directory if need be:
#if not os.path.exists(outpath):
#    os.makedirs(outpath)

with open(outfilename, 'w') as outfile:
    json.dump(results, outfile)
#print results
#print len(results)
