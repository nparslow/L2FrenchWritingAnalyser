#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'nparslow'

import json
import re
import os
import sys
import tarfile

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
inbasepath = "/home/nparslow/Documents/AutoCorrige/frwiki/"


def analyseTarFile( filename, sentences):
    #filename = "/home/nparslow/Documents/AutoCorrige/frwiki/frwikipedia_001.tar.gz"
    tar = tarfile.open(filename)
    for filename in tar.getnames():

        basefilename = os.path.split(filename)[-1]
        #print basefilename
        found = re.search(r"frwikipedia_\w+\.E(\w+)(?=\.dis\.dep\.xml)", basefilename)
        if found: # i.e. ignore the '.passage.xml' files
            sentenceNumber = found.group(1)

            fileobject = tar.extractfile(filename)
            analyseFileWiki(fileobject, sentenceNumber, sentences)

def analyseDirectory( inbasepath, sentences):
    # it's a directory:
    for element in os.listdir(inbasepath ):
        in_full_element = inbasepath + os.sep + element # note don't use 'pathsep' as it's a colon

        if os.path.isfile(in_full_element) and tarfile.is_tarfile(in_full_element):
            analyseTarFile(in_full_element, sentences )
        elif os.path.isdir(in_full_element):
            # analyse the directory
            analyseDirectory(in_full_element, sentences )


def analyseFileWiki( fileobject, sentenceNumber, sentences ):

        #print sentenceNumber, basefilename
        if sentenceNumber not in sentences: sentences[sentenceNumber] = ""

        #print "parsing:", filename
        try:
            tree = ET.parse(fileobject)

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
            print "Parse error on file", fileobject.name



sentences = {}

analyseDirectory(inbasepath, sentences)


print sentences
#outfilename = "/home/nparslow/Documents/fouille_de_textes/projet/lund/allSentences.json"
outfilename = "/home/nparslow/Documents/AutoCorrige/frwiki/testrun2.json"
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