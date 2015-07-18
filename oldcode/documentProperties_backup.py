# -*- coding: utf-8 -*-
from queryLexique380 import loadLexiqueToDict

__author__ = 'nparslow'

import codecs
import os
import xml.etree.cElementTree as ET
import re
import numpy as np
import itertools
import subprocess
import calcPLex
import compareCorrectedCorpus
import calcHDD
import getCorpusInfo
import classifyVerbs

print "loading freq info"
lemmacat2freqrank = calcPLex.loadLemmaCat2freqrank()

# from http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
def run_command(command1, args1, command2, args2):
    #run_command("echo", charmatch.group(), "/home/nparslow/exportbuild/bin/yadecode", '-u -l=fr')
    p1 = subprocess.Popen([command1, args1], stdout=subprocess.PIPE)
    p2 = subprocess.Popen([command2, args2], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = p2.communicate()[0]
    #print output.decode('latin1')#, type(output.decode('latin1'))
    #print output.strip(), type(output)
    #print output.strip().decode('latin1') #.decode('utf8')
    #return output.strip().decode('utf8')
    #return output.strip().decode('latin1') #.decode('utf8')
    return output.strip().decode('utf8')

    '''
    # returns a tuple (0, 'output we want')
    # only works on *nix
    # returns wrong format
    output = commands.getstatusoutput(command)
    return output[1]
    '''
    '''
    print command
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    return iter(p.stdout.readline, b'')
    '''

def fixMixedEncodings(token):
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

    # todo some empty tokens arrive here:
    return token
    if len(token) > 0:
        pass


# from the corpus directory, base filename (w/o extension) [can include directory structure] and sentence number
# create the strings for the processed sentence file and the processed token file
# note baseFileName is used twice, once for the directory, once for the file
def getProcessedSentenceFilePaths(corpus, baseFileName, sentenceNum):
    baseFileName = os.path.basename(baseFileName)

    path1 = sentenceNum/1000000
    path2 = (sentenceNum%1000000)/10000
    path3 = (sentenceNum%10000)/100
    #path4 = (sentenceNum%100)
    #print sentenceNum, path1, path2, path3 #, path4

    processedPath = os.path.join(corpus, baseFileName, str(path1), str(path2), str(path3) )
    baseProcessedSentenceFile = os.path.join(processedPath, baseFileName + ".E" + str(sentenceNum))
    processedDepXMLFile = baseProcessedSentenceFile + ".dep.xml"
    processedTokenFile = baseProcessedSentenceFile + ".tokens"
    processedLogFile = baseProcessedSentenceFile + ".log"
    return processedDepXMLFile, processedTokenFile, processedLogFile

#allpossibleresults = {'ok', 'robust', 'corrected'}
def getLogFileInfo(logFilename):
    sentenceinfos = []
    with codecs.open(logFilename, mode='r', encoding='latin-1') as infile:
        for line in infile:
            # each line of interest has 'analysis sentencenumber sentence'
            # we take the first 2
            #sentenceinfo = re.match(ur'(ok|robust|corrected)\s(\d+)', line, flags=re.UNICODE)
            sentenceinfo = re.match(ur'(\w+)\s(\d+)\s', line, flags=re.UNICODE)
            if sentenceinfo:
                #allpossibleresults.add(sentenceinfo.groups()[0])
                sentenceinfos.append(sentenceinfo.groups())
    return sentenceinfos

def getTokensFromFile( processedTokenFile ):
    tokens = []
    if os.path.isfile(processedTokenFile):
        #print "*** using tokens ***", processedTokenFile
        # .tokens files are in utf-8 if run individually, latin-1 if run over corpus
        with codecs.open(processedTokenFile, mode="r", encoding='utf8') as tokenFile:
            for tokenline in tokenFile:
                # check for a tab as the last line is empty
                if '\t' in tokenline:
                    #print tokenline
                    tokenNum_token = tokenline.strip().split('\t')
                    # can have empty tokens, ignore them:
                    if len(tokenNum_token) > 1:
                        tokenNum, token = tokenline.strip().split('\t')
                        # take all tokens at this point, including punctuation
                        #if re.search(ur'[^\W_]', token, flags=re.UNICODE):

                        # hack to fix the euro problem:
                        token = fixMixedEncodings(token)
                        #token = re.sub(ur'\&\#226;\&\#130;\&\#172;', u'€', token, flags=re.UNICODE)
                        tokens.append(token)
    return tokens

def makeRegexFromTokens( tokens ):
    #print tokens
    # œ changes to oe, but æ is not changed ... so allow for it in the regex
    # we have to account for changes in punctuation e.g. ` -> ' and ... from a single character
    # we if the first token has punctuation we allow that it may have been 'eaten' by the previous sentence
    #matchregex = ur'\s*' + ur'\s*'.join([re.sub(ur'oe', ur'[œ|oe]', re.sub(ur'[^\w\s]+', ur'[^\w\s]+', tokens[i], flags=re.UNICODE), flags=re.UNICODE)
    #                            if i > 0 else re.sub(ur'oe', ur'[œ|oe]', re.sub(ur'[^\w\s]+', ur'[^\w\s]*', tokens[i], flags=re.UNICODE), flags=re.UNICODE)
    #                                     for i in range(len(tokens))])
    nPuncTokensAtStart = -1
    for i in range(len(tokens)):
        if re.match(ur'(?:_|[^\w\s])+', tokens[i], flags=re.UNICODE):
            nPuncTokensAtStart = i
        else:
            break

    # a space can be removed before a - e.g. 'verbe en -er' goes to 'verbe', 'en-', 'er', I hope there's a good reason for that
    # so we allow space or - between tokens by swapping - for ' - ' and then making the spaces added optional
    # -ci is changed to _-ci
    # Chaque` un ->  Chaque'un (i.e. space removed and reduced to one token)
    # 1h:00 is changed to '1h', ':', '0' yup 1 zero is removed  <- not yet treated
    # 6:00-8:00 becomes: 6 : 0 - 8 : 0 <- this problem seems to have disappeared somehow ...
    # so allow sequences of numbers to vary in length and composition
    # allow a . or ; or any kind of non-word non-space at the start due to bad tokenisation
    # allow for tokens with spaces that are optional c'est à dire ->  c' est-à-dire
    '''
    matchregex = ur'\s*\.?' + ur'\s*'.join([re.sub(ur'oe', ur'(œ|oe)',
                                                re.sub(ur'\d+', ur'\d+',
                                                    re.sub(ur'(?<!\\s\\)\-', ur'\s?\-\s?',
                                                           re.sub(ur'_', ur'_?',
                                                               re.sub(ur'[^\w\s\-]+', ur'\s?[^\w\s\-]+\s?',
                                                                      tokens[i],
                                                                      flags=re.UNICODE),
                                                               flags=re.UNICODE),
                                                           flags=re.UNICODE),
                                                    flags=re.UNICODE),
                                                flags=re.UNICODE)
                                if i > nPuncTokensAtStart or len(tokens) == 1 else
                                         re.sub(ur'oe', ur'(œ|oe)',
                                                re.sub(ur'\d+', ur'\d+',
                                                    re.sub(ur'(?<!\\s)\\-', ur'\s?\-\s?',
                                                           re.sub(ur'_', ur'_?',
                                                               re.sub(ur'[^\w\s\-]+', ur'\s?[^\w\s\-]*\s?',
                                                                      tokens[i],
                                                                      flags=re.UNICODE),
                                                               flags=re.UNICODE),
                                                        flags=re.UNICODE),
                                                    flags=re.UNICODE),
                                                flags=re.UNICODE)
                                         for i in range(len(tokens))])
    '''
    matchregex = ur'\s*[^\w\s\-]?\s*' + ur'\s*'.join([re.sub(ur'oe', ur'(œ|oe)',
                                                   re.sub(ur' ', ur' ?',
                                                        re.sub(ur'(?<!\\s\\)\-', ur'\s?\-\s?',
                                                               re.sub(ur'_', ur'_?',
                                                                   re.sub(ur'[^\w\s\-]+', ur'\s?[^\w\s\-]+\s?',
                                                                          tokens[i],
                                                                          flags=re.UNICODE),
                                                                   flags=re.UNICODE),
                                                               flags=re.UNICODE),
                                                       flags=re.UNICODE),
                                                flags=re.UNICODE)
                                if i > nPuncTokensAtStart or len(tokens) == 1 else
                                         re.sub(ur'oe', ur'(œ|oe)',
                                                re.sub(ur' ', ur' ?',
                                                    re.sub(ur'(?<!\\s)\\-', ur'\s?\-\s?',
                                                           re.sub(ur'_', ur'_?',
                                                               re.sub(ur'[^\w\s\-]+', ur'\s?[^\w\s\-]*\s?',
                                                                      tokens[i],
                                                                      flags=re.UNICODE),
                                                               flags=re.UNICODE),
                                                        flags=re.UNICODE),
                                                    flags=re.UNICODE),
                                                flags=re.UNICODE)
                                         for i in range(len(tokens)) ])
    return matchregex

# same as in compareCorrectedCorpus version
def joinTokens(tokens):
    if len(tokens) == 0: return ""
    # remove any ,."?! at the end or beginning
    outtoken = re.sub(ur'(^\s*[\.,"\?!]+\s*|\s*[\.,"\?!]+\s*$)', u"", tokens[0], flags=re.UNICODE)
    #outtoken = tokens[0]
    for i in range(1, len(tokens)):
        t = tokens[i]
        if t == tokens[i-1]:
            continue
        t = re.sub(ur'(^\s*[\.,"\?!]+\s*|\s*[\.,"\?!]+\s*$)', u"", tokens[i], flags=re.UNICODE)
        # don't add repeated tokens (as they are overlapping ones
        if not re.match(ur'[\W_]+$', t, flags=re.UNICODE):
            if len(outtoken) > 2 and outtoken[-2:] == u"-_":
                outtoken = outtoken[:-2] + u"-"
            if len(outtoken) > 0 and len(t) > 0:
                if outtoken[-1] not in u"'-" and t[0] not in u"'-":
                    outtoken += u" "
            outtoken += t
    return outtoken

class Text:
    def __init__(self, paragraph_list):
        # student level (None if unknown)
        self.level = None
        self.paragraphs = paragraph_list
        # Lexical Sophisitication Measures:
        self.PLex = None
        self.S = None
        self.vocd = None
        self.mtld = None
        self.hdd = None
        self.vocab1k = None
        self.vocab2k = None
        self.vocab3k = None
        self.vocab4k = None
        self.vocab8k = None
        self.vocabOther = None
        self.vocabUnk = None
        #self.maas = None
        # parsing results:
        self.parsedok = None
        self.parsedcorr = None
        self.parsedrob = None
        # general properties
        self.nWords = None
        self.nSentences = None
        self.spellcorrpersent = None
        self.meanweightperword = None # from parser
        # verb information:
        self.vsingle = None
        self.vaux = None
        self.vcompound = None
        self.vindicative = None
        self.vconditional = None
        self.vsubjunctive = None
        self.vimperfect = None
        self.vfuture = None
        self.vpresent = None
        self.vnotense = None
        # clause info:
        self.crel = None
        self.cnom = None
        self.cacc = None
        self.cloc = None

    def nParagraphs(self):
        return len(self.paragraphs)

    def getNSentences(self):
        if not self.nSentences:
            self.nSentences = sum([x.nSentences() for x in self.paragraphs])
        return self.nSentences

    def meanSentencesPerParagraph(self):
        return self.getNSentences()*1.0/len(self.paragraphs)

    # Standard Deviation:
    def sdSentencesPerParagraph(self):
        return np.std([x.nSentences() for x in self.paragraphs])

    def getNWords(self):
        if not self.nWords:
            self.nWords = sum([x.nWords() for x in self.paragraphs])
        return self.nWords

    def meanWordsPerSentence(self):
        #print list(itertools.chain(*[x.listWordsPerSentence() for x in self.paragraphs]))
        return np.mean(list(itertools.chain(*[x.listWordsPerSentence() for x in self.paragraphs])))

    def sdWordsPerSentence(self):
        return np.std(list(itertools.chain(*[x.listWordsPerSentence() for x in self.paragraphs])))

    # ignores words with no letters, ignores numbers -, _ etc.
    def meanLettersPerWord(self):
        return np.mean(list(itertools.chain(*[x.listLettersPerWord() for x in self.paragraphs])))

    def sdLettersPerWord(self):
        return np.std(list(itertools.chain(*[x.listLettersPerWord() for x in self.paragraphs])))

    # ignores words with no letters, ignores numbers -, _ etc.
    def meanSyllablesPerWord(self):
        return np.mean(list(itertools.chain(*[x.listSyllablesPerWord() for x in self.paragraphs])))

    def sdSyllablesPerWord(self):
        return np.std(list(itertools.chain(*[x.listSyllablesPerWord() for x in self.paragraphs])))

    def addLexiqueInfo(self, lexiqueDict):
        for paragraph in self.paragraphs:
            for sentence in paragraph.sentences:
                for word in sentence.tokens:
                    #print "obsform:", word.observedform
                    for obsform in word.observedform:
                        obsform = obsform.lower()
                        obsformsyllables = 0
                        if obsform in lexiqueDict:
                            obsformsyllables =  lexiqueDict[obsform][0][1]
                            if len(lexiqueDict[obsform]) > 1:
                                lemmaFound = False
                                i = 1
                                while not lemmaFound and i < len(lexiqueDict[obsform]):
                                    if lexiqueDict[obsform][i][0] == word.lemma:
                                        obsformsyllables = lexiqueDict[obsform][i][1]
                                        lemmaFound = True
                                    i += 1
                        else:

                            # mostly can't find from spelling errors
                            # if we can't find, count the no. of separate vowel sections except for e at the end
                            # remove qu?e at the end:
                            # miscounts things like negativEment
                            obsform = re.sub(ur'(?:qu)?e$', u"", obsform, flags=re.UNICODE)

                            obsformsyllables = len(re.findall(
                                ur'[aeiouùûüÿàâæçéèêëïîôœ]+', obsform.lower(), flags=re.UNICODE))
                            print "cant find", obsform, "in", word.observedform, "adding", obsformsyllables, "syllables"
                        if word.nSyllables is None: word.nSyllables = 0
                        word.nSyllables += obsformsyllables

    def setVocabularyMeasures(self):
        lemmacats = list(itertools.chain(*[x.listLemmaCats() for x in self.paragraphs]))
        try:
            # as the fit can crash
            popt, pcov = calcPLex.calcPLex( lemmacats, lemmacat2freqrank)
            self.PLex = popt[0]
        except:
            self.PLex = 0.0
        #print lemmacats
        popt, pcov = calcPLex.calcS( lemmacats, lemmacat2freqrank)
        self.S = popt[0]
        if len(lemmacats) >= 50:
            self.vocd = calcPLex.getVOCD(lemmacats)
        else:
            self.vocd = 0.0
        self.mtld = calcPLex.getMTLD(lemmacats)
        if len(lemmacats) >= 42:
            self.hdd = calcHDD.calcHDD(lemmacats)
        else:
            self.hdd = 0.0
        #self.maas = calcHDD.calcMaas(lemmacats) # don't think this works right atm
        vocabs, self.vocabOther, self.vocabUnk =\
            calcPLex.calcLFP( lemmacats, lemmacat2freqrank, difficultybins = (1000,2000,3000,4000,8000))
        self.vocab1k, self.vocab2k, self.vocab3k, self.vocab4k, self.vocab8k = vocabs

    def getSpellCorrPerSent(self):
        if not self.spellcorrpersent:
            self.spellcorrpersent = 1.0* sum([x.getNSpellCorr() for x in self.paragraphs])/self.getNSentences() # divide here not at paragraph level
        return self.spellcorrpersent

    def getMeanWeightPerWord(self):
        if not self.meanweightperword:
            self.meanweightperword = 1.0* sum([x.getMeanWeightPerWord() for x in self.paragraphs])/self.getNSentences()
        return self.meanweightperword

    def setVerbClauseInfo(self):
        for para in self.paragraphs:
            para.setVerbClauseInfo()
        # verb info:
        self.vsingle = 1.0*sum([x.vsingle for x in self.paragraphs])/self.getNSentences()
        self.vaux = 1.0*sum([x.vaux for x in self.paragraphs])/self.getNSentences()
        self.vcompound = 1.0*sum([x.vcompound for x in self.paragraphs])/self.getNSentences()
        self.vindicative = 1.0*sum([x.vindicative for x in self.paragraphs])/self.getNSentences()
        self.vconditional = 1.0*sum([x.vconditional for x in self.paragraphs])/self.getNSentences()
        self.vsubjunctive = 1.0*sum([x.vsubjunctive for x in self.paragraphs])/self.getNSentences()
        self.vimperfect = 1.0*sum([x.vimperfect for x in self.paragraphs])/self.getNSentences()
        self.vfuture = 1.0*sum([x.vfuture for x in self.paragraphs])/self.getNSentences()
        self.vpresent = 1.0*sum([x.vpresent for x in self.paragraphs])/self.getNSentences()
        self.vnotense = 1.0*sum([x.vnotense for x in self.paragraphs])/self.getNSentences()
        # clause info:
        self.crel = 1.0*sum([x.crel for x in self.paragraphs])/self.getNSentences()
        self.cnom = 1.0*sum([x.cnom for x in self.paragraphs])/self.getNSentences()
        self.cacc = 1.0*sum([x.cacc for x in self.paragraphs])/self.getNSentences()
        self.cloc = 1.0*sum([x.cloc for x in self.paragraphs])/self.getNSentences()

class Paragraph:
    def __init__(self, sentence_list):
        self.sentences = sentence_list
        self.spellcorr = None
        self.meanweightperword = None
        # verb info:
        self.vsingle = None
        self.vaux = None
        self.vcompound = None
        self.vindicative = None
        self.vconditional = None
        self.vsubjunctive = None
        self.vimperfect = None
        self.vfuture = None
        self.vpresent = None
        self.vnotense = None
        # clause info:
        self.crel = None
        self.cnom = None
        self.cacc = None
        self.cloc = None

    def nSentences(self):
        return len(self.sentences)

    def nWords(self):
        return sum(self.listWordsPerSentence())

    def listWordsPerSentence(self):
        return [x.nWords() for x in self.sentences]

    def listLettersPerWord(self):
        return list(itertools.chain(*[x.listLettersPerWord() for x in self.sentences]))

    def listSyllablesPerWord(self):
        return list(itertools.chain(*[x.listSyllablesPerWord() for x in self.sentences]))

    def listLemmaCats(self):
        return list(itertools.chain(*[x.lemmaCats for x in self.sentences]))

    def getNSpellCorr(self):
        #print self.sentences
        if not self.spellcorr:
            self.spellcorr = sum([x.spellingcorrections for x in self.sentences])
        return self.spellcorr

    def getMeanWeightPerWord(self): # todo currently just approximate as we don't take sentence weights into account
        if not self.meanweightperword:
            self.meanweightperword = sum([x.weightperword for x in self.sentences]) # don't divide yet, will do at text level
        return self.meanweightperword

    def setVerbClauseInfo(self):
        # verb info:
        self.vsingle = sum([x.vsingle for x in self.sentences])
        self.vaux = sum([x.vaux for x in self.sentences])
        self.vcompound = sum([x.vcompound for x in self.sentences])
        self.vindicative = sum([x.vindicative for x in self.sentences])
        self.vconditional = sum([x.vconditional for x in self.sentences])
        self.vsubjunctive = sum([x.vsubjunctive for x in self.sentences])
        self.vimperfect = sum([x.vimperfect for x in self.sentences])
        self.vfuture = sum([x.vfuture for x in self.sentences])
        self.vpresent = sum([x.vpresent for x in self.sentences])
        self.vnotense = sum([x.vnotense for x in self.sentences])
        # clause info:
        self.crel = sum([x.crel for x in self.sentences])
        self.cnom = sum([x.cnom for x in self.sentences])
        self.cacc = sum([x.cacc for x in self.sentences])
        self.cloc = sum([x.cloc for x in self.sentences])


class Sentence:
    def __init__(self):
        self.tokens = None
        self.matchregex = None
        self.uniquetokens = None
        self.lemmaCats = None
        self.spellingcorrections = None
        self.weightperword = None
        self.minweight = None
        # verb info:
        self.vsingle = None
        self.vaux = None
        self.vcompound = None
        self.vindicative = None
        self.vconditional = None
        self.vsubjunctive = None
        self.vimperfect = None
        self.vfuture = None
        self.vpresent = None
        self.vnotense = None
        # clause info:
        self.crel = None
        self.cnom = None
        self.cacc = None
        self.cloc = None

    def setAndGetUniqueTokens(self):
        if self.uniquetokens is None:
            self.uniquetokens = []
            obstokenpositions = set([])
            for token in self.tokens:
                for obstoken, obstokenposition in zip(token.observedform, token.parseposition):
                    if obstokenposition not in obstokenpositions:
                        self.uniquetokens.append(obstoken)
                        obstokenpositions.add(obstokenposition)
        return self.uniquetokens

    # take a dictionary of form token no. -> list of (Lemma, Cat) tuples and converts to a list of lemma_cat strings
    def setLemmaCats(self, token2LemmaCats):
        self.lemmaCats = []
        for lemmacats in [y for x,y in sorted(token2LemmaCats.items(), key=lambda x:x[0])]:
            self.lemmaCats.extend([x[0] + u"_" + x[1] for x in lemmacats])

    def nWords(self):
        self.setAndGetUniqueTokens()
        return len(self.uniquetokens)

    def listLettersPerWord(self):
        return [len(re.findall(ur'[^\W\d_]', x, flags=re.UNICODE))
                for x in self.uniquetokens if re.search(ur'[^\W\d_]', x, flags=re.UNICODE)]

    # will return empty list if syllables not yet assigned
    def listSyllablesPerWord(self):
        return [x.nSyllables for x in self.tokens if x is not None]


class Token:
    def __init__(self, lemma, frmgform, observedform, parseposition):
        self.observedform = observedform    # will be a list as some structures are mutltitokens
                                            # note also some parts may appear multiple times  (for 2nd part of amalgams)
        self.frmgform = frmgform
        self.lemma = lemma
        self.parseposition = parseposition  # will be a list as there are sometimes 2 or 3 positions
        self.nSyllables = None


def getNextSentence( corpus, baseFileName, sentenceNum, debug=False ):
    if debug: print "Getting Next Sentence, number:", sentenceNum
    processedDepXMLFile, processedTokenFile, processedLogFile = \
        getProcessedSentenceFilePaths(corpus, baseFileName, sentenceNum)
    return getNextSentenceFromFiles(processedDepXMLFile, processedTokenFile, processedLogFile, debug )


def getNextSentenceFromFiles( processedDepXMLFile, processedTokenFile, processedLogFile, debug=False ):

    #print processedSentenceFile
    sentence = None
    if os.path.isfile(processedDepXMLFile):
        sentence = Sentence()

        tree = ET.parse(processedDepXMLFile)
        # 'W' nodes are 'words' which can include multiple tokens, e.g. 'bien que' is one word
        # .iter for recursive, .findall for depth of 1
        # id the cluster then get the lex element from the cluster (we'll process it later)
        wordsforms = [(x.attrib['lemma'], x.attrib['form'], x.attrib['cluster'],
                       fixMixedEncodings(tree.findall("cluster[@id='" + x.attrib['cluster']+"']")[0].attrib["lex"]))
                      for x in tree.iter('node') if len(x.get('lemma'))>0 and x.get('lemma') != "_EPSILON"]
        print "wordsforms"
        print wordsforms
        # correct the encodings and remove epsilons

        tokens = getTokensFromFile(processedTokenFile)
        if len(wordsforms) > 0:
            # sentence was at least partially parsed
            #print "sorted word forms:"
            #print sorted(wordsforms, key=lambda x: x[2].split('_')[1])
            # sort by the start point of the token
            #re.sub(ur'E\d+F\d+\|', u'', x[3], flags=re.UNICODE)
            sentence.tokens = [Token(x[0], x[1], re.findall(ur'(?<=[F\d]\d\|)[^ ]+', x[3], flags=re.UNICODE),
                                     [int(x) for x in re.findall(ur'(?<=F)\d+(?=\|)', x[3], flags=re.UNICODE) ])
                               for x in sorted(wordsforms, key=lambda x: int(x[2].split('_')[1]))]
            #sentence.forms = [x[1] for x in sorted(wordsforms, key=lambda x: x[2].split('_')[1])]
        else:
            # sentence wasn't parsed, so use the tokens file:
            #tokens = getTokensFromFile(processedTokenFile)
            print "using tokens***"
            sentence.tokens = [Token(None, None, tokens[i], i) for i in range(len(tokens))]

        #print sentence.tokens
        #print "obs forms:", [x.observedform for x in sentence.tokens]

        tok2finalforms, tok2lemmacats, verb2info, trees, (weight, minweight) = \
            compareCorrectedCorpus.getFinalTokenFormsAndTreesAndWeight(processedDepXMLFile)
        sentence.setLemmaCats(tok2lemmacats)
        sentence.weightperword = weight
        sentence.minweight = minweight

        verbAnalysis = classifyVerbs.classifyVerbs(verb2info)
        sentence.vsingle = 0
        if "single" in verbAnalysis: sentence.vsingle += verbAnalysis["single"]
        sentence.vaux = 0
        if "aux" in verbAnalysis: sentence.vaux += verbAnalysis["aux"]
        sentence.vcompound = 0
        if "compound" in verbAnalysis: sentence.vcompound += verbAnalysis["compound"]
        sentence.vindicative = 0
        if "indicative" in verbAnalysis: sentence.vindicative += verbAnalysis["indicative"]
        sentence.vconditional = 0
        if "conditional" in verbAnalysis: sentence.vconditional += verbAnalysis["conditional"]
        sentence.vsubjunctive = 0
        if "subjonctive" in verbAnalysis: sentence.vsubjunctive += verbAnalysis["subjonctive"]
        sentence.vimperfect = 0
        if "imperfect" in verbAnalysis: sentence.vimperfect += verbAnalysis["imperfect"]
        sentence.vfuture = 0
        if "future" in verbAnalysis: sentence.vfuture += verbAnalysis["future"]
        sentence.vpresent = 0
        if "present" in verbAnalysis: sentence.vpresent += verbAnalysis["present"]
        sentence.vnotense = 0
        if "notense" in verbAnalysis: sentence.vnotense += verbAnalysis["notense"]
        # clause info:
        sentence.crel = 0
        if "rel" in verbAnalysis: sentence.crel += verbAnalysis["rel"]
        sentence.cnom = 0
        if "nom" in verbAnalysis: sentence.cnom += verbAnalysis["nom"]
        sentence.cacc = 0
        if "acc" in verbAnalysis: sentence.cacc += verbAnalysis["acc"]
        sentence.cloc = 0
        if "loc" in verbAnalysis: sentence.cloc += verbAnalysis["loc"]

        sxpipeSpellingChanges = 0
        for i in range(len(tokens)):
            # skip multitoken elements, too hard
            if len(tok2finalforms[i+1]) > 1 or len(tok2finalforms[i+1][0].split(' ')) > 1: continue
            if tok2finalforms[i+1][0][0] == "_": continue
            t = tokens[i].lower()
            f = tok2finalforms[i+1][0].lower()

            if t != f:
                print "spelling?", t, f, tok2finalforms[i+1]
                sxpipeSpellingChanges += 1
        sentence.spellingcorrections=sxpipeSpellingChanges
        '''
            t = joinTokens([tokens[i].lower()])
            f = joinTokens(tok2finalforms[i+1]).lower()

            print t, f
            if i > 0:
                # tok2finalforms first token is no. 1
                if tok2finalforms[i+1] == tok2finalforms[i]: continue # don't look if two same wordforms in a row
            if t != f:
                # check its not a multiwoprint "spelling?", t, f, tok2finalforms[i+1]
                    sxpipeSpellingChanges += 1rd thing
                tmpi = i+1
                isDouble = False
                while f.startswith(t) and tmpi < len(tokens) and len(t) < len(f):
                    t = joinTokens([t, tokens[tmpi]])
                    if t == f:
                        isDouble = True
                        break
                    tmpi += 1

                if not isDouble:
                    print "spelling?", t, f, tok2finalforms[i+1]
                    sxpipeSpellingChanges += 1
        '''


        '''
        for s_token, observedtoken in zip([sentence.tokens[0]] + [sentence.tokens[i] for i in range(1,len(sentence.tokens))
                                                                  if sentence.tokens[i-1].parseposition != \
                                                                     sentence.tokens[i].parseposition],
                                          getTokensFromFile(processedTokenFile)):
            # the tokens file overrules the depxml, e.g. in depxml you have \?
            if s_token.observedform != observedtoken:
                print "combining:", s_token.frmgform, s_token.observedform, observedtoken
                s_token.observedform = observedtoken
        '''
        #print words
        #print forms

        # we remove double entries from amalgams
        if debug: print "pre make regex:"
        '''
        print [(sentence.tokens[i].parseposition[0],
                sentence.tokens[i-1].parseposition[-1],
                sentence.tokens[i].observedform) for i in range(1, len(sentence.tokens))]
        print [sentence.tokens[0].observedform] +[sentence.tokens[i].observedform
                                   for i in range(1,len(sentence.tokens))
                                   if sentence.tokens[i].parseposition[0] > sentence.tokens[i-1].parseposition[-1]]
        '''
        '''
        obstokens = []
        obstokenpositions = []
        for token in sentence.tokens:
            for obstoken, obstokenposition in zip(token.observedform, token.parseposition):
                if obstokenposition not in obstokenpositions:
                    obstokens.append(obstoken)
                    obstokenpositions.append(obstokenposition)
        '''
        obstokens = sentence.setAndGetUniqueTokens()
        #print "obstokens", obstokens
        sentence.matchregex = makeRegexFromTokens(obstokens)
        if debug: print "obstokens:", obstokens
        '''
        sentence.matchregex = makeRegexFromTokens(
            [sentence.tokens[0].observedform] +[sentence.tokens[i].observedform
                                   for i in range(1,len(sentence.tokens))
                                   if sentence.tokens[i].parseposition[0] > sentence.tokens[i-1].parseposition[-1]])
        '''
    return sentence

# assumes an open file and no .tokens file
def getSentenceFromFileObject( processedSentenceFile, outfileobject ):
    sentence = Sentence()

    try:
        tree = ET.parse(processedSentenceFile)
        # 'W' nodes are 'words' which can include multiple tokens, e.g. 'bien que' is one word
        # .iter for recursive, .findall for depth of 1
        # id the cluster then get the lex element from the cluster (we'll process it later)
        wordsforms = [(x.attrib['lemma'], x.attrib['form'], x.attrib['cluster'],
                       fixMixedEncodings(tree.findall("cluster[@id='" + x.attrib['cluster']+"']")[0].attrib["lex"]))
                      for x in tree.iter('node') if len(x.get('lemma'))>0 and x.get('lemma') != "_EPSILON"]
        # correct the encodings and remove epsilons

        if len(wordsforms) > 0:
            # sentence was at least partially parsed
            #print "sorted word forms:"
            #print sorted(wordsforms, key=lambda x: x[2].split('_')[1])
            # sort by the start point of the token
            #re.sub(ur'E\d+F\d+\|', u'', x[3], flags=re.UNICODE)
            sentence.tokens = [Token(x[0], x[1], re.findall(ur'(?<=[F\d]\d\|)[^ ]+', x[3], flags=re.UNICODE),
                                     [int(x) for x in re.findall(ur'(?<=F)\d+(?=\|)', x[3], flags=re.UNICODE) ])
                               for x in sorted(wordsforms, key=lambda x: int(x[2].split('_')[1]))]

            # remove any unparseable (empty) sentences (no tokens files)
            if len(sentence) > 0:
                orderedsentence = [sentence[x] for x in sorted(sentence.keys())]
                outfileobject.write("\t".join(orderedsentence))
                outfileobject.write("\n")

    except ET.ParseError as e:
        # if the xml is unparseable (including if the file is empty) will come here
        print "Parse error on file", processedSentenceFile.name
    return sentence


# get the properties of a document
def getDocumentProperties(corpus, filename, debug=False):

    text = Text([])
    sentenceNum = 1
    currentParagraph = Paragraph([])
    wordSyllableLengths = []
    wordCharacterLengths = []

    baseFileName, extension = os.path.splitext(filename)
    processedLogFile = os.path.basename(baseFileName) + ".log"

    currentSentence = None

    # get the learner level if it's known:
    text.level = getCorpusInfo.getCorpusInfo(baseFileName)

    #print corpus, processedLogFile
    print
    print "file:", filename
    parsinginfos = getLogFileInfo(os.path.join(corpus, processedLogFile))
    if debug: print "Num sentences:", len(parsinginfos)

    with codecs.open(filename, mode='r', encoding='utf8') as infile:
        #lastParagraphSentenceBreak = 0

        lineNumber = 0
        for line in infile:
            if debug:
                print "line:", line
            lineNumber += 1

            #print processedSentenceFile, os.path.isfile(processedSentenceFile)
            if currentSentence is None:
                currentSentence = getNextSentence(corpus, baseFileName, sentenceNum, debug=debug)
            currentSentenceUntested = True
            while currentSentenceUntested and currentSentence is not None:

                if debug:
                    print "sentence:", sentenceNum
                    print currentSentence.tokens
                    print "regex", currentSentence.matchregex

                if re.match(currentSentence.matchregex, line, flags=re.UNICODE):
                    # remove it from the line:
                    line = re.sub(ur'^' + currentSentence.matchregex, u'', line, flags=re.UNICODE)
                    if debug: print "newline:", line
                    sentenceNum += 1
                    # stock the current info and replace it with the next info
                    currentParagraph.sentences.append(currentSentence)
                    currentSentence = getNextSentence(corpus, baseFileName, sentenceNum)
                else:
                    currentSentenceUntested = False
                    if len(currentParagraph.sentences) > 0:
                    #if sentenceNum -1 > lastParagraphSentenceBreak :
                        text.paragraphs.append(currentParagraph)
                        currentParagraph = Paragraph([])
                        #paragraphLengths.append(sentenceNum-1-lastParagraphSentenceBreak)

                        #lastParagraphSentenceBreak = sentenceNum -1
                        #print "new paragraph:", paragraphLengths, lastParagraphSentenceBreak

                print "current para", len(currentParagraph.sentences), len(text.paragraphs)



    # wrap up the last paragraph (here minus 1 as the sentence num is one higher than observed
    # even though we want the break after the last sentence unlike previously
    #if lastParagraphSentenceBreak < sentenceNum-1:
    if len(currentParagraph.sentences) > 0:
        text.paragraphs.append(currentParagraph)
        #paragraphLengths.append(sentenceNum-1-lastParagraphSentenceBreak)
        #print "final paragraph:", paragraphLengths
    paragraphLengths = [len(x.sentences) for x in text.paragraphs]
    print "all paragraphs:        ", paragraphLengths
    print "sum of para lengths:   ", sum(paragraphLengths)
    print "last real sentence:    ", sentenceNum -1
    print "expected no. sentences:", len(parsinginfos)
    if len(parsinginfos) != sum(paragraphLengths):
        print "PROBLEM!!!!!"
    text.parsedok = 1.0*parsinginfos.count("ok")/len(parsinginfos)
    text.parsedrob = 1.0*parsinginfos.count("robust")/len(parsinginfos)
    text.parsedcorr = 1.0*parsinginfos.count("corrected")/len(parsinginfos)


    #else:
    #    print "Sentene numbers match :)"

    lexiqueDict = {}
    loadLexiqueToDict(u"/home/nparslow/Documents/AutoCorrige/tools/Lexique380/Bases+Scripts/Lexique380.txt",
                      lexiqueDict)
    #print type(lexiqueDict)
    text.addLexiqueInfo( lexiqueDict)

    text.setVocabularyMeasures()
    text.setVerbClauseInfo() # must be run after all the sentences to pass the info up

    return text

# outfilepath : directory where outfile will go
# corpusname : will be used as a title and for the filename so choose wisely!
# header info : information to put in the header (can be split into lines separated by \n)
# should not include any %, @ signs
# varnametypes = list of 2-tuples (variable_name, type)
# [type can be NUMERIC, string, date or class (class not implemented atm) ]
# rows = list of lists each sublist = a row of info in the same order as the varnames
def savetoArff( outfilepath, corpusname, headerInfo, varnametypes, rows):
    with codecs.open(os.path.join(outfilepath, corpusname + ".arff"), mode="w", encoding="utf8")as arfffile:
        for headerline in headerInfo.split("\n"):
            arfffile.write("% " + headerline + '\n')
        arfffile.write("@RELATION " + corpusname + '\n')
        arfffile.write('\n')

        for attribute, attributetype in varnametypes:
            arfffile.write("@ATTRIBUTE " + attribute + "\t" + attributetype + '\n')
        arfffile.write('\n')
        arfffile.write("@DATA" + '\n')
        for row in rows:
            arfffile.write(",".join([unicode(x) if type(x) != unicode else x for x in row])+'\n')


def main():
    #baseDir = "/home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS/CORPUS_CHY-FLE/"
    baseDir = "/home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS/CORPUS_HELLAS-FLE/"
    #baseDir = "/home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS/CORPUS_CENTRE-FLE/"

    '''
    filename = "chyFLE_2011_TI_UCY_4_Autoobservation_Aphrodite_Papaioannou.txt" # 109 sentences
    filename = "chyFLE_2011_TI_UCY_4_Autoobservation_Savvia_Leonidou.txt" # 111 sentences

    filenames = ["chyFLE_2011_TI_UCY_4_Autoobservation_Neofytos_Antoniou.txt"]
    filenames = ["chyFLE_2010_TL_UCY_1A_Autoobservation_Agathe_Chrysse.txt"]
    filenames = ['chyFLE_2010_TL_UCY_1A_Strategies_Yiannis_Panayides.txt']
    filenames = ["chyFLE_2010_TL_UCY_1A_Strategies_Rafaella_Georgiou.txt"]
    filenames = ["chyFLE_2011_TI_UCY_4_Autoobservation_Susanna_Georgiou.txt"]
    filenames = ["chyFLE_2011_TI_UCY_4_Autoobservation_Margarita_Epiphaniou.txt"]
    fname = baseDir + filename

    corpus = "/home/nparslow/Documents/AutoCorrige/Corpora/crappy"
    '''
    filenames = ['hellasFLE_2010_TL_KPG_B2_Activite2_candidat18.txt'] # frmg bug site electronique -> site

    #filenames = ['centreFLE_2005_TL_CFLETP_5_Activite2_CRYAN_Barra.txt'] # frmg bug le Match 1-0. -> the 0 is lost
    #filenames = [ 'centreFLE_2004_TL_CFLETP_7_Activite2_ECKER_Susanne_2.txt'] # euro -> &#226;&#130;&#172;

    filenames = ["hellasFLE_2010_TL_KPG_C1_Activite1_candidat16.txt"]

    corpus = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_ECRIT_VALETOPOULOS"

    #corpus = "/home/nparslow/Documents/AutoCorrige/Corpora/crappy"
    #baseDir = "/home/nparslow/Documents/AutoCorrige/Corpora/"
    #filenames = ["test.txt"]

    corpus = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_CEFLE"
    baseDir = "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_CEFLE/C"
    filenames = ["Cecilia4.txt"]

    #nparagraphs = getDocumentProperties(corpus, fname)
    #print "nparas:", nparagraphs

    #for filename in os.listdir(baseDir):
    outputRows =[]
    variables = [ ("filename", "string"),
                  ("level", "NUMERIC"),
                  ("nParagraphs", "NUMERIC"),
                  ("nSentences", "NUMERIC"),
                  ("nWords", "NUMERIC"),
                  ("sentsPerPara", "NUMERIC"),
                  ("sdSentsPerPara", "NUMERIC"),
                  ("wordsPerSent", "NUMERIC"),
                  ("sdWordsPerSent", "NUMERIC"),
                  ("lettersPerWord", "NUMERIC"),
                  ("sdLettersPerWord", "NUMERIC"),
                  ("syllablesPerWord", "NUMERIC"),
                  ("sdSyllablesPerWord", "NUMERIC"),
                  ("PLex", "NUMERIC"),
                  ("S", "NUMERIC"),
                  ("vocd", "NUMERIC"),
                  ("mtld", "NUMERIC"),
                  ("hdd", "NUMERIC"),
                  ("vocab1k", "NUMERIC"),
                  ("vocab2k", "NUMERIC"),
                  ("vocab3k", "NUMERIC"),
                  ("vocab4k", "NUMERIC"),
                  ("vocab8k", "NUMERIC"),
                  ("vocabHigh", "NUMERIC"),
                  ("vocabOth", "NUMERIC"),
                  ("spellcorr", "NUMERIC"),
                  ("parsedok", "NUMERIC"),
                  ("parsedcorr", "NUMERIC"),
                  ("parsedrob", "NUMERIC"),
                  ("weightperword", "NUMERIC"),
                  ("vsingle", "NUMERIC"),
                  ("vaux", "NUMERIC"),
                  ("vcompound", "NUMERIC"),
                  ("vindicative", "NUMERIC"),
                  ("vconditional", "NUMERIC"),
                  ("vsubjunctive", "NUMERIC"),
                  ("vimperfect", "NUMERIC"),
                  ("vfuture", "NUMERIC"),
                  ("vpresent", "NUMERIC"),
                  ("vnotense", "NUMERIC"),
                  ("crel", "NUMERIC"),
                  ("cnom", "NUMERIC"),
                  ("cacc", "NUMERIC"),
                  ("cloc", "NUMERIC"),
                  ]

    for filename in filenames:
        print
        print filename
        fname = baseDir + filename
        text = getDocumentProperties(corpus, fname, debug=False)
        print "nparas:", text.nParagraphs()
        print "nsents:", text.getNSentences()
        print "nwords:", text.getNWords()
        print "mean sents/para", text.meanSentencesPerParagraph()
        print "sd   sents/para", text.sdSentencesPerParagraph()
        print "mean words/sent", text.meanWordsPerSentence()
        print "sd   words/sent", text.sdWordsPerSentence()
        print "mean letts/word", text.meanLettersPerWord()
        print "sd   letts/word", text.sdLettersPerWord()
        print "mean sylls/word", text.meanSyllablesPerWord()
        print "sd   sylls/word", text.sdSyllablesPerWord()
        print ""
        outputRows.append( (filename,
                            text.level,
                            text.nParagraphs(),
                            text.getNSentences(),
                            text.getNWords(),
                            text.meanSentencesPerParagraph(),
                            text.sdSentencesPerParagraph(),
                            text.meanWordsPerSentence(),
                            text.sdWordsPerSentence(),
                            text.meanLettersPerWord(),
                            text.sdLettersPerWord(),
                            text.meanSyllablesPerWord(),
                            text.sdSyllablesPerWord(),
                            text.PLex,
                            text.S,
                            text.vocd,
                            text.mtld,
                            text.hdd,
                            text.vocab1k,
                            text.vocab2k,
                            text.vocab3k,
                            text.vocab4k,
                            text.vocab8k,
                            text.vocabOther,
                            text.vocabUnk,
                            text.getSpellCorrPerSent(),
                            text.parsedok,
                            text.parsedcorr,
                            text.parsedrob,
                            text.meanweightperword,
                            text.vsingle,
                            text.vaux,
                            text.vcompound,
                            text.vindicative,
                            text.vconditional,
                            text.vsubjunctive,
                            text.vimperfect,
                            text.vfuture,
                            text.vpresent,
                            text.vnotense,
                            text.crel,
                            text.cnom,
                            text.cacc,
                            text.cloc,
                            ) )

    outarffdir = u"/home/nparslow/Documents/AutoCorrige/Corpora/figures"
    corpusName = "test"
    headerInfo = "a test corpus\n of stuff"
    savetoArff(outarffdir, corpusName, headerInfo, variables, outputRows )


    #print "possible results", allpossibleresults





if __name__ == "__main__":
    main()


