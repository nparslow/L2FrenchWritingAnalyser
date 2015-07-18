# coding=utf-8
import os
import re
import classifyVerbs
import getMEltInfo

import readDepXMLFile
__author__ = 'nparslow'

def makeRegexFromTokens( tokens, debug=False ):
    #print tokens
    # œ changes to oe (it's a ligature, not a character), but æ is not changed ... so allow for it in the regex
    # we have to account for changes in punctuation e.g. ` -> ' and ... from a single character
    # we if the first token has punctuation we allow that it may have been 'eaten' by the previous sentence
    if debug: print "making regex from tokens", tokens
    nPuncTokensAtStart = -1
    for i in range(len(tokens)):
        if re.match(ur'(?:_|[^\w\s])+', tokens[i], flags=re.UNICODE):
            nPuncTokensAtStart = i
        else:
            break

    # We can have a sentence with just punctuation tokens, a punctuation point somehow, in this case just return an empty regex:
    if re.match(ur'[^\w_]+$', "".join(tokens), flags=re.UNICODE):
        if debug: print "warning, sentence with just punct tokens", " ".join(tokens)
        return ur''

    # a space can be removed before a - e.g. 'verbe en -er' goes to 'verbe', 'en-', 'er', I hope there's a good reason for that
    # so we allow space or - between tokens by swapping - for ' - ' and then making the spaces added optional
    # -ci is changed to _-ci
    # Chaque` un ->  Chaque'un (i.e. space removed and reduced to one token)
    # 1h:00 is changed to '1h', ':', '0' yup 1 zero is removed  <- not yet treated
    # 6:00-8:00 becomes: 6 : 0 - 8 : 0 <- this problem seems to have disappeared somehow ...
    # so allow sequences of numbers to vary in length and composition
    # allow a . or ; or any kind of non-word non-space at the start due to bad tokenisation
    # allow for tokens with spaces that are optional c'est à dire ->  c' est-à-dire
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
    if debug: print "returning regex", matchregex
    return matchregex


class Token:
    def __init__(self, lemma, frmgform, observedform, parseposition):
        self.observedform = observedform    # will be a list as some structures are mutltitokens
                                            # note also some parts may appear multiple times  (for 2nd part of amalgams)
        self.frmgform = frmgform
        self.lemma = lemma
        self.parseposition = parseposition  # will be a list as there are sometimes 2 or 3 positions
        self.nSyllables = None


class Sentence:
    def __init__(self, processedDepXMLFile, processedTokenFile, processedLogFile, processedMEltFile, debug=False):

        if debug:
            print "new Sentence"
            print processedDepXMLFile
            print processedTokenFile
            print processedLogFile
            print processedMEltFile

        self.debug = debug

        self.tokens = None
        self.rawtokens = None
        self.matchregex = None
        self.uniquetokens = None
        self.lemmaCats = None
        self.spellingcorrections = None
        self.weightperword = None
        self.minweight = None
        self.meltconfidences = None
        self.meltdiffs = None
        self.wordsbeforemainverb = None
        self.hasnomainverb = None
        # parse info
        self.parsed = None
        # verb info:
        self.vgroups = None # should be sum of verb entries for a particular axis projection, != no. of verbs as compounds count as one verb group
        self.vanalysis = None # will be a dictionary with property -> count
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
        # tree info
        self.trees = None

        self.wordforms = []
        self.verbAnalysis = None
        self.totalverbgroups = None

        if os.path.isfile(processedTokenFile):
            self.rawtokens = readDepXMLFile.getTokensFromFile(processedTokenFile)

        # melttoks is a list of (tok, tag, prob)
        meltToks = getMEltInfo.loadAndAlign(processedMEltFile, self.rawtokens )

        if os.path.isfile(processedDepXMLFile):
            xmlinfo = readDepXMLFile.readDepXMLFile(processedDepXMLFile, self.debug)
            self.wordforms = xmlinfo["wordforms"]

            if debug:
                print "xmlinfo, tok to final forms:"
                print xmlinfo["tok2finalforms"]
                print "xmlinfo, tok to lemmacats:"
                print xmlinfo["tok2lemmacats"]
            self.setLemmaCats(xmlinfo["tok2lemmacats"])
            if debug:
                print "xmlinfo, lemmacats:"
                print self.lemmaCats
            self.weightperword = xmlinfo["weightperword"]
            self.minweight = xmlinfo["minweight"]
            self.wordsbeforemainverb = xmlinfo["wordsbeforemainverb"]
            self.hasnomainverb = 1 if xmlinfo["wordsbeforemainverb"] == -1 else 0
            self.trees = dict( (x,len(xmlinfo["trees"][x])) for x in xmlinfo["trees"])
            self.parsed = xmlinfo["parsemode"]
            #print "sent parsed", self.parsed

            self.tok2finalforms = xmlinfo["tok2finalforms"]

            #print "sent", xmlinfo["verb2info"]
            self.verbAnalysis, self.totalverbgroups = classifyVerbs.classifyVerbs(xmlinfo["verb2info"])
            #print "sent", self.verbAnalysis

            self.calcSpellingCorrections()

            self.meltdiffs = getMEltInfo.getMEltDiffs(xmlinfo["tok2lemmacats"], meltToks, debug)

        if len(self.wordforms) > 0:
            # sentence was at least partially parsed
            #print "sorted word forms:"
            #print sorted(wordsforms, key=lambda x: x[2].split('_')[1])
            # sort by the start point of the token
            #re.sub(ur'E\d+F\d+\|', u'', x[3], flags=re.UNICODE)
            self.tokens = [Token(x[0], x[1], re.findall(ur'(?<=[F\d]\d\|)[^ ]+', x[3], flags=re.UNICODE),
                                     [int(x) for x in re.findall(ur'(?<=F)\d+(?=\|)', x[3], flags=re.UNICODE) ])
                               for x in sorted(self.wordforms, key=lambda x: int(x[2].split('_')[1]))]
            #sentence.forms = [x[1] for x in sorted(wordsforms, key=lambda x: x[2].split('_')[1])]
        else:
            # sentence wasn't parsed, so use the tokens file:
            #tokens = getTokensFromFile(processedTokenFile)
            print "using tokens***"
            self.tokens = [Token(None, None, self.rawtokens[i], i) for i in range(len(self.rawtokens))]

        if debug: print "sent tokens:", self.tokens

        self.matchregex = makeRegexFromTokens(self.rawtokens, debug)
        if debug:
            print "obstokens:", self.rawtokens
            print "regex", self.matchregex



        self.meltconfidences = [float(x[2]) if (x[2] is not None and x[2] != 'None') else 1.0 for x in meltToks]
        if debug: print "sent melt confs:", self.meltconfidences


        # todo : continue putting textExtractor getnextsentencefromfile stuff here (then clean up and organise)
        # todo check calc


    # we use the raw tokens and compare with tok2final forms
    def calcSpellingCorrections(self):
        sxpipeSpellingChanges = 0
        #print self.rawtokens
        for i in range(len(self.rawtokens)):
            # skip multitoken elements, too hard
            if i+1 in self.tok2finalforms:
                #print tok2finalforms
                if len(self.tok2finalforms[i+1]) > 1 or len(self.tok2finalforms[i+1][0].split(' ')) > 1: continue
                if self.tok2finalforms[i+1][0][0] == "_": continue
                t = self.rawtokens[i].lower()
                f = self.tok2finalforms[i+1][0].lower()

                if t != f:
                    if self.debug: print "spelling?", t, f, self.tok2finalforms[i+1]
                    sxpipeSpellingChanges += 1
        self.spellingcorrections=sxpipeSpellingChanges


    def setAndGetUniqueTokens(self):
        if self.uniquetokens is None:
            self.uniquetokens = []
            obstokenpositions = set([])
            for token in self.tokens:
                for obstoken, obstokenposition in zip(token.observedform, token.parseposition):
                    #print "yo", obstoken, obstokenposition
                    if obstokenposition not in obstokenpositions:
                        self.uniquetokens.append(obstoken)
                        obstokenpositions.add(obstokenposition)
            '''
            # there may be a repeated token which has been ignored (e.g. 'il est est qqc')
            # this is an ugly patch, but not sure of a better way :/
            for i in range(1, len(obstokenpositions)+1):
                if i not in obstokenpositions:
                    print "missing token", i
                    for token in self.tokens:
                        #print "token parsepos", token.parseposition
                        if token.parseposition[0] == i +1:
                            print token.observedform
                            self.uniquetokens = self.uniquetokens[0:i] + token.observedform + self.uniquetokens[i:]
            print "obs tok pos", obstokenpositions
            '''
        return self.uniquetokens

    # take a dictionary of form token no. -> list of (Lemma, Cat) tuples and converts to a list of lemma_cat strings
    # punctuation is removed (i.e. any element which has no alphanumeric char in it
    def setLemmaCats(self, token2LemmaCats):
        self.lemmaCats = []
        for lemmacats in [y for x,y in sorted(token2LemmaCats.items(), key=lambda x:x[0])]:
            # amalgams have multiple elements and all need to be added, hence the extend/list use
            #if len(lemmacats) > 1: print "extending lemma cats with:", lemmacats #[x[0] + u"_" + x[1] for x in lemmacats]
            # the _ is used in the lemmacat2freq as stocking a tuple rather than a list is not possible in json
            # so we keep the format here
            toadd = [x[0] + u"_" + x[1] for x in lemmacats]
            # we need to avoid adding any composed words twice:
            if len(self.lemmaCats) >= len(toadd):
                if self.lemmaCats[-len(toadd):] == toadd:
                    continue
            self.lemmaCats.extend(toadd)
            #self.lemmaCats.extend( [(x[0], x[1]) for x in lemmacats])

    def nWords(self):
        self.setAndGetUniqueTokens()
        return len(self.uniquetokens)

    def listLettersPerWord(self):
        return [len(re.findall(ur'[^\W\d_]', x, flags=re.UNICODE))
                for x in self.uniquetokens if re.search(ur'[^\W\d_]', x, flags=re.UNICODE)]

    # will return empty list if syllables not yet assigned
    def listSyllablesPerWord(self):
        return [x.nSyllables for x in self.tokens if x is not None]

    def addLexiqueInfo(self, lexiqueDict):
        for word in self.tokens:
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