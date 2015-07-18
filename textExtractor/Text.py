# coding=utf-8
import codecs
import itertools
import re
import math
import numpy as np
import calcHDD
import calcPLex
import getCohesionVariables
import nGramModel
import readDdag
from utils import flatten2LevelList
from utils import product
from utils import combineCountDicts
import getCorpusInfo

__author__ = 'nparslow'

# return the differences between subsequence members in a sequence
# returns a list with one less member than the inlist
def getDifferences( inlist ):
    return [inlist[i]-inlist[i-1] for i in range(1, len(inlist))]

# returns a statistic based on the differences between elements in a list
def getDiffStatistic( inlist, statistic="mean" ):
    diffs = getDifferences(inlist)
    return getCountStatistic( diffs, statistic )

# returns a statistic based on an input of a sequence of values
# by default returns the mean if unknown statistic is input
def getCountStatistic( incounts, statistic = "mean"):
    if statistic == "sd":
        return np.std(incounts)
    return np.mean(incounts)

# an lfp_run is a list of 1 or 2-tuples, with a beginning (or 'unknown') and a possible end
def LFP_run_to_params( lfp_run):
    borders = [0]
    #positions = []
    #nextpos = 0
    for params in lfp_run:
        if params[0] == borders[-1] + 1:
            # then we don't need to add it to the borders
            pass
        elif params[0] == "unknown":
            pass
        else:
            print params
            borders.append(params[0]-1)
            #nextpos += 1
        if len(params) == 1:
            if params[0] == "unknown":
                #positions.append("unknown")
                pass
            else:
                #positions.append("high")
                pass
        if len(params) > 1:
            borders.append(params[1])
            #positions.append(nextpos)
            #nextpos += 1
    return borders #, positions





# variables = list of 2tuples (variable, listofparams), filenames = dict of type of file to filename
class Text:
    def __init__(self, variables, resource2filename, sentences, debug=False ):

        self.variables = variables
        self.resource2filename = resource2filename
        self.debug = debug

        self.sentences = sentences
        # student level (None if unknown)
        self.level = getCorpusInfo.getCorpusInfo(resource2filename["filename"])

        self.nWords = None
        self.paragraphStarts = [0] # the start position 0 is always there

        self.lemmacats = None

        self.vanalysis = None
        self.vgroups = None

        self.ddagSentences = None

        # prepare any of the required properties for particular variables:
        self.variabletypes = set([x[0] for x in variables])
        self.__prepareRequiredElements()

        # variable name to function
        #self.requiredFuncs = []
        #for variable in variables:
        #    self.requiredFuncs.append( ) # todo

        self.variablevalues = [None]*len(variables) # use position in list to define



    # do any internal preparations required for the variables:
    def __prepareRequiredElements(self):
        # we always get the number of words:
        self.getNWords()
        if "paragraphs" in self.variabletypes:
            self.alignParagraphs()
        for vocabVar in ["PLex", "S", "altS", "vocd", "mtld", "hdd", "LFP"]:
            if vocabVar in self.variabletypes:
                self.setLemmaCats()
                break # we only need to set it once
        if "verb" in self.variabletypes or "clause" in self.variabletypes:
            self.setVerbClauseInfo()
        # we set the trees for all (as it is used after)
        #if "treeTypesHDD" in self.variabletypes or "treeTypesYuleK" in self.variabletypes:
        self.setTrees()
        if "w2vct" in self.variabletypes:
            self.setDDagSentences()



    def calcVariables(self, resources):
        # some variables are best calculated together, in particular the LFP and altS:
        # grab the LFP variables and sort by the lowest boundary (note 'unknown' will be put last)
        # we use enumerate to retain the position in the list of variables
        #print [ (x,y) for y,x in enumerate(self.variables) if x[0] == "LFP"]
        lfp_vars = sorted([ (x,y) for y,x in enumerate(self.variables) if x[0] == "LFP"], key=lambda (x,y):x[1][0])
        lfp_runs = []
        run2vars = {}
        for (lfp_var, params), varpos in lfp_vars:
            foundrun = False
            for i in range(len(lfp_runs)):
                if len(lfp_runs[i][-1]) > 1:
                    # check the end of the last segment is less than the start of the (possible) next
                    if lfp_runs[i][-1][1] < params[0]:
                        lfp_runs[i].append(params)
                        foundrun = True
                        if i not in run2vars: run2vars[i] = []
                        run2vars[i].append(varpos)
                        break
                else:
                    # we can only add if it is unknown and the previous is unlimited
                    # or if the previous is unknown, in which case we already calculate it (so we skip)
                    if params[0] == "unknown":
                        if lfp_runs[i][-1][0] == "unknown":
                            pass
                        else:
                            lfp_runs[i].append(params)
                        foundrun = True
                        if i not in run2vars: run2vars[i] = []
                        run2vars[i].append(varpos)
                        break
            # this also covers the intial case (the loop above will have 0 turns):
            if not foundrun:
                lfp_runs.append( [params] )
                if len(lfp_runs)-1 not in run2vars: run2vars[len(lfp_runs)-1] = []
                run2vars[len(lfp_runs)-1].append(varpos)
        for i, run in enumerate(lfp_runs):
            borders = LFP_run_to_params(run)
            #print "getting LFP", borders
            # use all except for the first zero as it is not used in LFP calculation
            lfpvalues, lfphigh, lfpunknown = self.getVariable("LFP", params=borders[1:], resources=resources)
            for varnum in run2vars[i]:
                var, params = self.variables[varnum]
                if len(params) == 1:
                    if params[0] == "unknown":
                        self.variablevalues[varnum] = lfpunknown
                    else:
                        self.variablevalues[varnum] = lfphigh
                else:
                    for lowbord, value in zip(borders, lfpvalues):
                        if lowbord + 1 == params[0]:
                            self.variablevalues[varnum] = value
                            break

        if "syllablesPerWord" in self.variabletypes:
            self.addLexiqueInfo(resources["lexiqueDict"])

        altsvals = []
        w2vctvals = []
        for i, (var, params) in enumerate(self.variables):
            # don't recalculate anything calculated
            if self.variablevalues[i] is None:
                # altS we need to get both at once, so we stock them to avoid recalculation
                if var == "altS":
                    #print "altS", params
                    if len(altsvals) == 0:
                        altsvals = self.getVariable("altS", [], resources)
                    if params[0] == "a":
                        self.variablevalues[i] = altsvals[0]
                    else:
                        self.variablevalues[i] = altsvals[1]
                # ditto for word2vec cos theta values:
                elif var == "w2vct":
                    if len(w2vctvals) == 0:
                        w2vctvals = self.getVariable("w2vct", [], resources)
                    if params[0] == "Word":
                        if params[1] == "Word":
                            self.variablevalues[i] = w2vctvals[0]
                        else: # Sent
                            self.variablevalues[i] = w2vctvals[1]
                    else: # Sent
                        if params[1] == "Sent":
                            self.variablevalues[i] = w2vctvals[2]
                        else: # Text
                            self.variablevalues[i] = w2vctvals[3]
                # for the general variable
                else:
                    #print "calc", var, params
                    self.variablevalues[i] = self.getVariable(var, params, resources)






    def getVariable(self, variable, params, resources ):
        if variable == "paragraphs":
            return len(self.paragraphStarts)
        elif variable == "sentences":
            return len(self.sentences)
        elif variable == "words":
            return self.getNWords()
        elif variable == "sentsPerPara":
            #print "sents per para", params[0]
            return getDiffStatistic( self.paragraphStarts +[len(self.sentences)], params[0] )
        elif variable == "wordsPerSent":
            return getCountStatistic( [len(x.uniquetokens) for x in self.sentences], params[0] )
        elif variable == "lettersPerWord":
            #print [y for x in self.sentences for y in x.uniquetokens]
            # we need the if requirement to remove punctuation etc.
            return getCountStatistic( [len(re.findall(ur'[^\W\d_]', y, flags=re.UNICODE))
                                       for x in self.sentences for y in x.uniquetokens
                                       if len(re.findall(ur'[^\W\d_]', y, flags=re.UNICODE)) > 0], params[0] )
        elif variable == "syllablesPerWord":
            #print "syllables per word", [x.listSyllablesPerWord() for x in self.sentences]
            return getCountStatistic( flatten2LevelList([x.listSyllablesPerWord() for x in self.sentences]), params[0] )
        elif variable == "PLex":
            # as the fit can crash
            #print "plexing"
            try:
                popt, pcov = calcPLex.calcPLex( self.lemmacats, resources["lemmacat2freqrank"], difficultRank=params[0])
                #print "plex", popt, pcov
                return popt[0]
            except:
                print "P_Lex fit problem"
                return 0.0
        elif variable == "S":
            popt, pcov = calcPLex.calcS( self.lemmacats, resources["lemmacat2freqrank"])
            return popt[0]
        elif variable == "altS":
            #return self.getAltSValues( resources["lemmacat2freqrank"] )
            popt, pcov = calcPLex.calcAB( self.lemmacats, resources["lemmacat2freqrank"])
            return popt
        elif variable == "vocd":
            if len(self.lemmacats) >= 50:
                #print "vocd", self.lemmacats
                #print  calcPLex.getVOCD(self.lemmacats), calcPLex.calcVOCD(self.lemmacats)
                return calcPLex.calcVOCD(self.lemmacats)
            else:
                return -1.0
        elif variable == "mtld":
            return calcPLex.calcMTLD(self.lemmacats, params[0])
        elif variable == "hdd":
            if len(self.lemmacats) >= 42:
                return calcHDD.calcHDD(self.lemmacats)
            return 0.0
        elif variable == "LFP":
            #vocabs, vocabOther, vocabUnk =\
            #print "lfp:", params
            #print calcPLex.calcLFP( self.lemmacats, resources["lemmacat2freqrank"], difficultybins = params)
            return calcPLex.calcLFP( self.lemmacats, resources["lemmacat2freqrank"], difficultybins = params)
        elif variable == "spellcorr":
            return 1.0* sum([x.spellingcorrections for x in self.sentences])/self.getNWords()
        elif variable == "meltdiff":
            return 1.0* sum([x.meltdiffs for x in self.sentences])/self.getNWords()
        elif variable == "meanmelt": # gets the geometic mean:
            return math.pow( product(flatten2LevelList([x.meltconfidences for x in self.sentences])), 1.0/self.getNWords())
        elif variable == "parsed":
            # need a param either 'full', 'corrected' or 'robust'
            #print "parsed:", params[0], type(params[0])
            #print [x.parsed for x in self.sentences]
            #print [type(x.parsed) for x in self.sentences]
            return 1.0* len( [x.parsed for x in self.sentences if x.parsed == params[0]])/len(self.sentences)
        elif variable == "weightPerWord":
            return 1.0* sum([x.weightperword*len(x.uniquetokens) for x in self.sentences])/self.getNWords()
        elif variable == "verb":
            #print params[0]
            #print self.vanalysis.keys()
            if params[0] in self.vanalysis:
                return 1.0*self.vanalysis[params[0]]/self.vgroups
            else:
                return 0.0
        elif variable == "clause":
            #print "CLAUSE", params[0], self.vanalysis[params[0]]
            #print "CLAUSE", self.vanalysis.keys()
            if params[0] in self.vanalysis:
                return 1.0*self.vanalysis[params[0]]/len(self.sentences)
            else:
                return 0.0
        elif variable == "w2vct":
            return getCohesionVariables.getCohesionVariables(resources["word2vecModel"], self.ddagSentences)
        elif variable == "treeTypesPerSent":
            return getCountStatistic( [len(x.trees.keys()) for x in self.sentences], *params )
        elif variable == "TreeTypesHDD":
            #print "hdd", self.trees.values()
            return calcHDD.calcHDDfromFreq(self.trees.values())
        elif variable == "TreeTypesYuleK":
            #print "yulek", self.trees.values()
            return calcHDD.calcYuleKfromFreq(self.trees.values())
        elif variable == "noVerbSentences":
            return 1.0*len([x.hasnomainverb for x in self.sentences if x.hasnomainverb > 0])/len(self.sentences)
        elif variable == "toksBeforeMainVerb":
            return 1.0*sum([x.wordsbeforemainverb for x in self.sentences if x.wordsbeforemainverb >= 0])/ \
                   len([x.wordsbeforemainverb for x in self.sentences if x.wordsbeforemainverb >= 0])
        # currently no sentence boundaries:
        elif variable == "bigramLogProbs":
            return nGramModel.analyseTokens(flatten2LevelList(self.ddagSentences),
                                            resources["nGramDict"], resources["nmoGramDict"], resources["nGramCounts"])



    def getNWords(self):
        if not self.nWords:
            self.nWords = sum([x.nWords() for x in self.sentences])
        return self.nWords


    # todo this should be moved to sentence or token level ?
    def addLexiqueInfo(self, lexiqueDict):
        for sentence in self.sentences:
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
                        #if debug: print "cant find", obsform, "in", word.observedform, "adding", obsformsyllables, "syllables"
                    if word.nSyllables is None: word.nSyllables = 0
                    word.nSyllables += obsformsyllables

    def setLemmaCats(self):
        self.lemmacats = list(itertools.chain(*[x.lemmaCats for x in self.sentences]))

    def setVerbClauseInfo(self):
        self.vanalysis = combineCountDicts( [x.verbAnalysis for x in self.sentences] )
        self.vgroups = sum([x.totalverbgroups for x in self.sentences])

    def setTrees(self):
        self.trees = combineCountDicts([x.trees for x in self.sentences])

    # these are currently not aligned with parsed sentences, but in theory it shouldn't be too hard if needed ...
    def setDDagSentences(self):
        self.ddagSentences = readDdag.readDdag( self.resource2filename["ddagfile"] )

    def alignParagraphs(self):
        # here we get the number of paragraphs and align each sentence to a paragraph:
        with codecs.open(self.resource2filename["filename"], mode='r', encoding='utf8') as infile:

            lineNumber = 0
            currentSentenceNum = 0
            for line in infile:
                if self.debug:
                    print "line:", line
                lineNumber += 1

                #print processedSentenceFile, os.path.isfile(processedSentenceFile)
                #if currentSentence is None:
                #    currentSentence = getNextSentence(corpus, meltdir, baseFileName, sentenceNum, debug=debug)
                currentSentenceUntested = True
                while currentSentenceUntested and currentSentenceNum < len(self.sentences):

                    if self.debug:
                        print "sentence:", currentSentenceNum
                        print self.sentences[currentSentenceNum].tokens
                        print "regex", self.sentences[currentSentenceNum].matchregex
                        print "lineto match", line

                    if re.match(self.sentences[currentSentenceNum].matchregex, line, flags=re.UNICODE):
                        # remove it from the line:
                        line = re.sub(ur'^' + self.sentences[currentSentenceNum].matchregex, u'', line, flags=re.UNICODE)
                        if self.debug: print "newline:", line
                        currentSentenceNum += 1
                        # stock the current info and replace it with the next info
                        #currentParagraph.sentences.append(currentSentence)
                        #sentences.append(currentSentence)
                        #if self.debug: print "getting next sentence", baseFileName, sentenceNum
                        #currentSentence = getNextSentence(corpus, meltdir, baseFileName, sentenceNum, debug=debug)
                    else:
                        currentSentenceUntested = False
                        #if len(currentParagraph.sentences) > 0:
                        # the -1 as sentenceNum starts from 1, and in our code starts from zero
                        if currentSentenceNum - self.paragraphStarts[-1] > 0:
                        #if sentenceNum -1 > lastParagraphSentenceBreak :
                            #text.paragraphs.append(currentParagraph)
                            # note: sentenceNum is one more than the current sentence when counting from zero
                            self.paragraphStarts.append(currentSentenceNum)
                            #currentParagraph = Paragraph([])
                            #paragraphLengths.append(sentenceNum-1-lastParagraphSentenceBreak)

                            #lastParagraphSentenceBreak = sentenceNum -1
                            #print "new paragraph:", paragraphLengths, lastParagraphSentenceBreak
                if re.search(ur'\S', line, flags=re.UNICODE):
                    print "PROBLEM section of line unfound"
                    print len(self.sentences), currentSentenceNum
                    print "regex         :", self.sentences[currentSentenceNum].matchregex
                    print "remaining line:", line

                    #print "current para", len(currentParagraph.sentences), len(text.paragraphs)
        # note : we don't add the end of the final paragraph



    # todo
        #self.adjustedTTR = calcHDD.calcTextLengthAdjustedTTR(lemmacats)
        #self.uniqueBigram = calcHDD.calcUniqueBigramRatio(lemmacats)
        #self.maas = calcHDD.calcMaas(lemmacats) # don't think this works right atm


    '''
    def getAltSValues(self, lemmacat2freqrank, val = "a"):
        if self.altS_a == None or self.altS_b == None:
            popt, pcov = calcPLex.calcAB( self.lemmacats, lemmacat2freqrank)
            self.altS_a = popt[0], self.altS_b = popt[1]
        if val == "b":
            return self.altS_b
        return self.altS_a
    '''

