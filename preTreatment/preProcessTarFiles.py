#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'nparslow'

import sys
import tarfile
import os
import re
import xml.etree.cElementTree as ET
import codecs
import subprocess

def analyseTarFile( filename, outbasepath):
    #print "an Tar"
    with tarfile.open(filename, mode='r') as tar:
        outfilename = os.path.join(outbasepath, re.sub(r'\.tar\.gz', '.out', os.path.split(filename)[-1])) # remove the directory structure
        #print outfilename, filename

        with codecs.open(outfilename, encoding="utf-8", mode="w") as outfileobject:
            counter = 0
            for tarinfo in tar:
                #if counter > 100: break
                counter += 1

                xmlfilename = tarinfo.name
                basexmlfilename = os.path.split(xmlfilename)[-1]
                #print basexmlfilename
                if re.match(r"^frwikipedia_\w+\.E\w+\.dis\.dep\.xml$", basexmlfilename):
                    # i.e. ignore the '.passage.xml' files
                    fileobject = tar.extractfile(xmlfilename)
                    #with tar.extractfile(xmlfilename) as fileobject: # with here provokes an attribute error
                    #analyseFileWiki(fileobject, outfileobject)
                    analyseFileWikiDDAG(fileobject, outfileobject)
                    fileobject.close()

def analyseDirectory( inbasepath, outbasepath ):
    for element in os.listdir(inbasepath ):
        in_full_element = inbasepath + os.sep + element # note don't use 'pathsep' as it's a colon
        #print element, "an Dir", os.path.isfile(in_full_element), tarfile.is_tarfile(in_full_element)
        if os.path.isfile(in_full_element) and tarfile.is_tarfile(in_full_element):
            #print "an tar"
            analyseTarFile(in_full_element, outbasepath)

        elif os.path.isdir(in_full_element):
            # analyse the directory
            analyseDirectory(in_full_element, outbasepath)


def analyseFileWiki( infileobject, outfileobject ):
    #print "parsing:", fileobject.name
    try:
        tree = ET.parse(infileobject)
        sentence = {} # position to lemma_cat

        #print "new sentence"
        for node in tree.findall('node'):
            lemma = node.get("lemma")
            cat = node.get("cat")
            cluster = node.get("cluster")
            end_position = cluster.rsplit("_",1)[1] # e.g. cluster has form E13c_8_9
            print "lemmma", lemma, "cat", cat, "cluster", cluster, "end pos", end_position

            #if True: # at the preprocessing stage we keep everything:
            if len(lemma) > 0 and len(cat) > 0: # only non-empty lemmas and cats
                if cat != "_"  and not re.match(r'\W+', lemma, re.UNICODE): # require no _ at start of lemma and no punctuation
                #       and lemma[0] != "_" and cat in acceptedCategories:
                    # TODO are there others apart from these? Uw is some sort of pronoun
                    #sentence.append(lemma + "_" + cat)
                    sentence[end_position] = lemma + "_" + cat
        print sentence

        # remove any unparseable (empty) sentences
        if len(sentence) > 0:
            orderedsentence = [sentence[x] for x in sorted(sentence.keys())]
            outfileobject.write("\t".join(orderedsentence))
            outfileobject.write("\n")

    except ET.ParseError as e:
        # if the xml is unparseable (including if the file is empty) will come here
        print "Parse error on file", infileobject.name
    exit(0)


def getDDAG(line):
    os.environ['PATH'] += ":/home/nparslow/exportbuild/bin/"

    command1 = 'echo'
    args1 = line
    command2 = 'sxpipe'
    command3 = 'dag2ddag'
    command4 = 'dag2udag'
    p1 = subprocess.Popen([command1, args1], stdout=subprocess.PIPE)
    p2 = subprocess.Popen([command2, ], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    p3 = subprocess.Popen([command3, ], stdin=p2.stdout, stdout=subprocess.PIPE)
    p2.stdout.close()  # Allow p2 to receive a SIGPIPE if p3 exits.
    p4 = subprocess.Popen([command4, ], stdin=p3.stdout, stdout=subprocess.PIPE)
    p3.stdout.close()  # Allow p3 to receive a SIGPIPE if p4 exits.
    output = p4.communicate()[0]
    print output
    exit(0)
    return output


def analyseFileWikiDDAG( infileobject, outfileobject=None ):
    #print "parsing:", fileobject.name

    for line in infileobject:
        ddags = getDDAG(line)

        for ddagline in ddags:
            ddagline = ddagline.strip()
            if "##DAG END" not in ddagline and "##DAG BEGIN" not in ddagline:
                tokennum, tokeninfo, nexttokennum = ddagline.split('\t')
                #print tokeninfo
                # can have multiple tokens so start from the right:
                token = re.search(ur'(?: )([^\}]+)$', tokeninfo, flags=re.UNICODE).groups()[0]

                # in case some empty tokens arrive here:
                # ouput = 1 token per line, empty line = new sentence
                if len(token) > 0:
                    outfileobject.write(token)
                    outfileobject.write("\n")
            elif "##DAG END" in ddagline:
                outfileobject.write("\n")


    exit(0)


if __name__=='__main__':
    if len(sys.argv) != 1: # first argument is always the name of the script
        print len(sys.argv)
        print("Usage: ./preProcessTarFiles.py")
        exit(1)

    #print "hello"
    inbasepath = "/home/nparslow/Documents/AutoCorrige/frwiki/"
    outbasepath = "/home/nparslow/Documents/AutoCorrige/Corpora/tokenised/CORPUS_FRWIKI"

    analyseDirectory(inbasepath, outbasepath)
    #print "bye"


