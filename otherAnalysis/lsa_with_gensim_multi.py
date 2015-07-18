#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'nparslow'

import json
import re
import os
import sys
import tarfile
import xml.etree.cElementTree as ET
from gensim import corpora, models, similarities, matutils
import logging
import multiprocessing



#class FileAnalyser(object):
#    def __init__(self):
#        manager = multiprocessing.Manager()
#        self.sentences = manager.list()
#        self.jobs = []
#        #self.sentences = sentences

def analyseTarFile( filename, sentences):
    with tarfile.open(filename, mode='r') as tar:
        #for filename in tar.getnames()[0:10]:
        counter = 0
        for tarinfo in tar:
            if counter > 100: break
            counter += 1

            filename = tarinfo.name
            basefilename = os.path.split(filename)[-1]
            #print basefilename
            if re.match(r"^frwikipedia_\w+\.E\w+\.dis\.dep\.xml$", basefilename):
                # i.e. ignore the '.passage.xml' files
                fileobject = tar.extractfile(filename)
                #with tar.extractfile(filename) as fileobject: # with here provokes an attribute error in multiprocessor
                analyseFileWiki(fileobject, sentences)
                fileobject.close()

def analyseDirectory( inbasepath, jobs, sentences):
    # it's a directory:

    for element in os.listdir(inbasepath ):
        in_full_element = inbasepath + os.sep + element # note don't use 'pathsep' as it's a colon

        if os.path.isfile(in_full_element) and tarfile.is_tarfile(in_full_element):
            p = multiprocessing.Process(target=analyseTarFile, args=(in_full_element, sentences, ))
            jobs.append(p)
            p.start()
            #self.analyseTarFile(in_full_element )
        elif os.path.isdir(in_full_element):
            # analyse the directory
            analyseDirectory(in_full_element, jobs, sentences )

def analyseAll( inbasepath):
    manager = multiprocessing.Manager()
    sentences = manager.list()
    jobs = []
    analyseDirectory(inbasepath, jobs, sentences)

    for proc in jobs:
        proc.join()
    return sentences


def analyseFileWiki( fileobject, sentences ):

    #sentences.append([])

    #print "parsing:", fileobject.name
    try:
        tree = ET.parse(fileobject)
        sentence = []

        for node in tree.findall('node'):
            lemma = node.get("lemma")
            cat = node.get("cat")
            #print "lemmma", lemma

            if lemma not in ignorelemmas and lemma[0] != "_"\
                    and lemma not in stopwords and not re.match(r'\W+', lemma, re.UNICODE)\
                    and cat in acceptedCategories:
                # TODO are there others apart from these? Uw is some sort of pronoun
                #sentences[-1].append(lemma + "_" + cat)
                sentence.append(lemma + "_" + cat)

        # remove any unparseable sentences
        #if len(sentences[sentenceNumber]) == 0: del sentences[sentenceNumber]
        print(sentence)
        #if len(sentences[-1]) < minLemmaQuantity:
        #    del sentences[-1] # require at least 3 lemmas in the sentence
        if len(sentence) >= minLemmaQuantity:
            sentences.append(tuple(sentence))
            #return tuple(sentence)

    except ET.ParseError as e:
        # if the xml is unparseable (including if the file is empty) will come here
        print "Parse error on file", fileobject.name
    #return None
    #print "sents:", sentences



class MyCorpus(object):
    def __init__(self, sentences):
        self.sentences = sentences
    def __iter__(self):
        for line in self.sentences:
            # assume there's one document per line, tokens separated by whitespace

            yield dictionary.doc2bow(line, allow_update=True) # causes problems
            #print dictionary.doc2bow(line)


if __name__=='__main__':

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # note can have a lemma in a best="no" (i.e. no parse found case), e.g. lemma='ne'

    stopwords = {} #{'et', 'le', 'de', 'un', u'à', u'être', u'avoir', 'que', 'ce', 'ou', 'qui', } # a set
    #ignorechars = ''',:'!.?'''
    #ignorechars = {'\'', ':', '!', '?', '-', '.', ',', '(', ')'}
    ignorelemmas = {"", "cln", "Uw", "cll", "ilimp", "cld", "clr", "cla"}

    acceptedCategories = {"nc", "v", "adj", "adv"}
    # ignore pro, det, prep, coo, Infl, N2, np, strace, S, VMod, aux, unknown, comp, incise etc.

    minLemmaQuantity = 3 # min no. of lemmas to have in a sentence to keep the sentence

    dictionary = corpora.Dictionary(None, None) # initialise dictionary with no phrases and no max size


    if len(sys.argv) != 1: # first argument is always the name of the script
        print len(sys.argv)
        print("Usage: ./lsa_with_cefle") # script to call takes a student_name as input param
        exit(1)

    inbasepath = "/home/nparslow/Documents/AutoCorrige/frwiki/"



    #fileanalyser = FileAnalyser()
    #fileanalyser.analyseAll(inbasepath)

    #sentences = fileanalyser.getSentences()
    sentences = analyseAll(inbasepath)

    print sentences
    #outfilename = "/home/nparslow/Documents/fouille_de_textes/projet/lund/allSentences.json"
    outfilename = "/home/nparslow/Documents/AutoCorrige/frwiki/testrun2.json"
    with open(outfilename, 'w') as outfile:
        json.dump(tuple(sentences), outfile)



    corpus_memory_friendly = MyCorpus(sentences)

    # collect statistics about all tokens
    #dictionary = corpora.Dictionary(corpus_memory_friendly, prune_at=None)
    dictionary = corpora.Dictionary(sentences) # dictionary stores conversion integer <-> word

    # remove words that appear only once
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
    dictionary.filter_tokens(once_ids) # remove stop words and words that appear only once
    dictionary.compactify() # remove gaps in id sequence after words that were removed
    print(dictionary)
    dictionary.save('wikitest.dict')

    # to save the corpus in Market Matrix format, also SVMlight, Blei, Low possible
    corpora.MmCorpus.serialize('wikicorpus.mm', corpus_memory_friendly)

    #print(corpus_memory_friendly)

    # convert from/to sparse (also numpy conversion possible)
    #corpus = matutils.Sparse2Corpus(scipy_sparse_matrix)
    #scipy_csc_matrix = matutils.corpus2csc(corpus_memory_friendly)
    #print scipy_csc_matrix


