__author__ = 'nparslow'

import tarfile

import re
import os
import sys
import xml.etree.cElementTree as ET

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
            tree = ET.parse(tar.extractfile(filename))

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


filename = "/home/nparslow/Documents/AutoCorrige/frwiki/frwikipedia_001.tar.gz"

tar = tarfile.open(filename)
sentences = {}
for filename in tar.getnames():

    analyseFileWiki(filename, sentences )
    #print filename

print sentences
print len(sentences)