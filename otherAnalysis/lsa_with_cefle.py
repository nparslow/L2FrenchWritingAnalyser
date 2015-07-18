#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'nparslow'

import json
import re
import os
import sys

import xml.etree.cElementTree as ET

if len(sys.argv) != 1: # first argument is always the name of the script
    print len(sys.argv)
    print("Usage: ./lsa_with_cefle") # script to call takes a student_name as input param
    exit(1)
#inpath = sys.argv[1]
#outpath = sys.argv[2]
#script = " ".join(sys.argv[1:])
#script = sys.argv[1]

#inbasepath = "/home/nparslow/Documents/fouille_de_textes/projet/lund/frmgXml"
inbasepath = "/home/nparslow/Documents/AutoCorrige/frwiki/frwikipedia_001"

def analyseDirectory( inbasepath, sentences):
    # it's a directory:
    for element in os.listdir(inbasepath ):
        in_full_element = inbasepath + os.sep + element # note don't use 'pathsep' as it's a colon

        if os.path.isfile(in_full_element):
            #analyseFile(in_full_element, sentences )
            analyseFileWiki(in_full_element, sentences )
        else:
            # analyse the directory
            analyseDirectory(in_full_element, sentences )

# doesn't overwrite output
def analyseFile( filename, sentences ):
    basefilename = os.path.split(filename)[-1]
    #print basefilename
    student = re.search(r"(?<=FRMG)\w+(?=Sentence\d+\.xml)", basefilename).group(0)
    sentenceNumber = re.search(r"(?<=FRMG)\w+(?=Sentence(\d+)\.xml)", basefilename).group(1)

    key = student + "_" + sentenceNumber
    if key not in sentences: sentences[key] = ""

    tree = ET.parse(filename)

    #distribution_trees = {}

    for node in tree.findall('node'):
        #treeInfo = node.get("tree")
        lemma = node.get("lemma")
        #print treeInfo, lemma

        if lemma not in ["", "cln", "Uw", "cll", "ilimp", "cld", "clr", "cla"] and lemma[0] != "_": # TODO are there others apart from these? Uw is some sort of pronoun
            sentences[key] += " " + lemma

    # remove any unparseable sentences
    if len(sentences[key]) == 0: del sentences[key]

def analyseFileWiki( filename, sentences ):
    basefilename = os.path.split(filename)[-1]
    #print basefilename
    found = re.search(r"frwikipedia_\w+\.E(\w+)(?=\.dis\.dep\.xml)", basefilename)
    if found: # i.e. ignore the '.passage.xml' files

        sentenceNumber = found.group(1)
        #print sentenceNumber, basefilename
        if sentenceNumber not in sentences: sentences[sentenceNumber] = ""

        #print "parsing:", filename
        try:
            tree = ET.parse(filename)

            #distribution_trees = {}

            for node in tree.findall('node'):
                #treeInfo = node.get("tree")
                lemma = node.get("lemma")
                #print treeInfo, lemma

                if lemma not in ["", "cln", "Uw", "cll", "ilimp", "cld", "clr", "cla"] and lemma[0] != "_": # TODO are there others apart from these? Uw is some sort of pronoun
                    sentences[sentenceNumber] += " " + lemma

            # remove any unparseable sentences
            if len(sentences[sentenceNumber]) == 0: del sentences[sentenceNumber]
        except ET.ParseError as e:
            # if the xml is unparseable (including if the file is empty) will come here
            print "Parse error on file", filename



sentences = {}

analyseDirectory(inbasepath, sentences)

print sentences
#outfilename = "/home/nparslow/Documents/fouille_de_textes/projet/lund/allSentences.json"
outfilename = "/home/nparslow/Documents/AutoCorrige/frwiki/testrun.json"
with open(outfilename, 'w') as outfile:
    json.dump(sentences, outfile)


titles = sentences.values()
stopwords = ['et','le','de','un', u'à', u'être', u'avoir', 'que']
ignorechars = ''',:'!.?'''
#ignorechars = ''',:'!'''

import lsa
mylsa = lsa.LSA(stopwords, ignorechars)
for t in titles:
    mylsa.parse(t)
mylsa.build()
mylsa.printA()
mylsa.calc()
mylsa.printSVD()