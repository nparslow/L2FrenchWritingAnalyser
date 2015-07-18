# coding=utf-8
import commands
import xml.etree.cElementTree as ET
import os
import json
import sys
import codecs
import re
import subprocess

import documentProperties

__author__ = 'nparslow'


'''
loops over the files created by frmg
compile a learner vocab for use in language modelling
saves to a .json file
'''





def analyse( path, vocabdict ):
    if os.path.isdir(path):
        for element in os.listdir(path):
            analyse(os.path.join(path, element), vocabdict)
    else:
        analyseFile(path, vocabdict)

# will overwrite output
# vocab is our discovered vocab (as a word to count dictionary)
def analyseFile( filename, vocab2count ):
    basefileName, fileExtension = os.path.splitext(filename)
    if fileExtension == ".xml":
        pass
        '''
        basefileName, fileExtension = os.path.splitext(basefileName)
        if fileExtension == ".dep":
            #print "filename", filename
            sentence = documentProperties.getNextSentenceFromFiles(filename, basefileName + ".tokens")

            # unique tokens come from the frmg analyser, tokens from the .tokens file
            tokens = tokens = sentence.tokens

            for token in tokens:
                #print token.frmgform, token.lemma

                # 3 options:
                # 1) token.frmgform and token.lemma are the sam
                # 2) lemma is _LABEL (take the lemma)
                # 3) lemma is e.g. Uw or cln or ilimp or sortir etc. (take the token)
                # 4) lemma is _EPSILON and fmrgform is _EPSILON (I'll remove these at an earlier stage)

                to_take = token.frmgform
                if token.lemma[0] == "_":
                    to_take = token.lemma

                if "&#" in token.frmgform or "&#" in token.lemma:
                     # in fact the two encodings can be mixed: e.g. <token> E1F1 é&#201;&#163;
                    print token.frmgform, token.lemma

                if to_take not in vocab2count: vocab2count[to_take] = 0
                vocab2count[to_take] += 1
        '''

        '''
        tree = ET.parse(filename)
        for node in tree.findall('node'):
            treeInfo = node.get("tree")echo "&#201;" | yadecode -u -l=fr

            lemma = node.get("lemma")
            #print treeInfo, lemma

            if treeInfo[0].isdigit():
                number_types = treeInfo.split()
                treeNum = number_types[0]
                #for x in number_types[1:]:
                #    print "type", x
                if treeNum not in results: results[treeNum] = 0
                results[treeNum] += 1
        '''
    elif fileExtension == ".tokens":
        pass
        '''
        # note upper case is retained at this point
        #print "analysing file", filename
        with codecs.open(filename, mode='r', encoding='utf8') as tfile:
            for line in tfile:
                line = line.strip()

                #if "&#" in line:
                #    # in fact the two encodings can be mixed: e.g. <token> E1F1 é&#201;&#163;
                #    command = "echo '" + line
                #    print line
                #    print filename



                if re.search('\t', line):
                    number, token = line.split('\t')
                    if re.match(ur'\d+', number, flags=re.UNICODE):

                        chars = re.finditer(ur'(?:&#\d\d\d\;)+', token, flags=re.UNICODE)
                        newtoken = u""
                        usedpos = 0
                        for charmatch in chars:
                            newtoken += token[usedpos:charmatch.start()]
                            usedpos = charmatch.end()
                            # translate the character:
                            command = 'echo "' + charmatch.group() + '" |' \
                                      ' /home/nparslow/exportbuild/bin/yadecode -u -l=fr'
                            #os.system(command)
                            #translation = "".join(run_command(command))
                            #c = run_command(command)
                            c = run_command("echo", charmatch.group(), "/home/nparslow/exportbuild/bin/yadecode", '-u -l=fr')
                            #print c, type(c)
                            #print c.decode('utf8'), type(c.decode('utf8'))
                            newtoken += c
                        newtoken += token[usedpos:]
                        if newtoken != token:
                            #print token, newtoken
                            token = newtoken
                            #for x in translation:
                            #    print x

                        # some empty tokens arrive here:
                        if len(token) > 0:
                            if token not in vocab2count: vocab2count[token] = 0
                            vocab2count[token] += 1
        '''
    elif fileExtension == ".log":
        pass

    elif fileExtension == ".ddag":
        with codecs.open(filename, mode='r', encoding='utf8') as tfile:
            for line in tfile:
                line = line.strip()
                if "##DAG END" not in line and "##DAG BEGIN" not in line:
                    tokennum, tokeninfo, nexttokennum = line.split('\t')
                    #print tokeninfo
                    # can have multiple tokens so start from the right:
                    token = re.search(ur'(?: )([^\}]+)$', tokeninfo, flags=re.UNICODE).groups()[0]

                    # can have left over whitespace somehow:
                    token = token.strip()

                    # in case some empty tokens arrive here:
                    if len(token) > 0:

                        if token not in vocab2count: vocab2count[token] = 0
                        vocab2count[token] += 1
                    #if u"«" in tokeninfo: print tokeninfo, token, len(token), token == u"«", u"«" in vocab2count #vocab2count[u'«']

        #print u"«" in vocab2count



def main():

    if len(sys.argv) > 2: # first argument is always the name of the script
        print "Usage: ./compileLearnerVocab output_filename" \
              " (default =  /home/nparslow/Documents/AutoCorrige/Corpora/outputs/learner_vocab.json) "
        print "e.g. python compileLearnerVocab.py  /home/nparslow/Documents/AutoCorrige/Corpora/outputs/learner_vocab.json"
        exit(1)

    outfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/outputs/learner_vocab_chyfle.json"
    outfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/outputs/learner_vocab_cefle.json"
    outfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/outputs/learner_vocab_combined.json"

    if len(sys.argv) > 1:
        outfilename = sys.argv[1]

    #individually
    corpora = ["/home/nparslow/Documents/AutoCorrige/Corpora/tokenised/CORPUS_ECRIT_VALETOPOULOS/",
               ]
    corpora = ["/home/nparslow/Documents/AutoCorrige/Corpora/tokenised/CORPUS_CEFLE/",
               ]
    # add CEFLE later
    corpora = ["/home/nparslow/Documents/AutoCorrige/Corpora/tokenised/CORPUS_ECRIT_VALETOPOULOS/",
               "/home/nparslow/Documents/AutoCorrige/Corpora/tokenised/CORPUS_CEFLE/",
               ]

    vocab2count = {}
    for corpusdir in corpora:
        analyse(corpusdir, vocab2count)
    #print u"«" in vocab2count
    for word in vocab2count:
        print word
    print "vocab with upper/lower difference:", len(vocab2count)
    print "vocab w/o  upper/lower difference:", len(set([x.lower() for x in vocab2count]))
    with codecs.open(outfilename, 'w', encoding="utf8") as outfile:
        json.dump(vocab2count, outfile)


    outlistfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/outputs/learner_vocab.list"
    with codecs.open(outlistfilename, mode="w", encoding="utf8") as outlistfile:
        for word in set([x.lower() for x in vocab2count]):
            outlistfile.write(word + "\n")

    #print results
    #print len(results)


if __name__ == "__main__":
    main()
