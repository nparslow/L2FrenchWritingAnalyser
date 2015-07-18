# coding=utf-8
import os
import codecs
import re
import unicodedata
import json
import sys

from gensim.models.word2vec import Vocab # Vocab object used in word2vec

__author__ = 'nparslow'

# to avoid screwed up ascii in the terminal/console
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


# splits by space and removes an odd character
# returns a list of words or an empty list
def basicTokenise(line):
    words = []
    # remove lines with jpg/gif files in them as the filename is often split
    # same for urls
    if not re.search(ur'((jpg|gif)\\\||http : )', line, flags=re.UNICODE | re.IGNORECASE ):
        # there are lots of encodings {alternative form of word} e.g. {specialisé \( e \) } spécialisées
        line = re.sub(ur'\{.+\}', ur'', line) # note this can lead to two subsequent spaces, so need to avoid empty string
        # remove { { citation\| parts:
        line = re.sub(ur'\{ \{ citation\\\|', ur'', line)
        # split on space or \|, make the brackets non-capturing with ?:
        words = re.split(ur'\s*(?:\s|(?:\\\|))+\s*', line.strip(), flags=re.UNICODE)
        # there are some empty lines and these lead to the empty string in the vocab, or lines with everything but
        # a space removed
        # found word with 'left to right mark' !?!?!?
        #print "tokenising:", line

    '''
    if len([x for x in words if len(x.strip())==0]) > 0:
        print "Problem line:"
        print line
        print words
        returning = [re.sub(ur'[\u200e\u202C]', '', word, flags=re.UNICODE)
            for word in words if len(word.strip())>0 and not re.match(ur'\s+$', word.strip(), flags=re.UNICODE)]
        print "returning:", returning
        if len([x for x in returning if len(x.strip())==0]) > 0 :
            print "Major problem!"
    '''
    return [re.sub(ur'[\u200e\u202C]', '', word.strip(), flags=re.UNICODE)
            for word in words if len(word.strip())>0 and not re.match(ur'\s+$', word.strip(), flags=re.UNICODE)]

# try to split any tokens which do not appear frequently enough:
def secondaryTokenise(word, word2count, token2subtokens, mincount):

    # check if we haven't already divided it:
    if word not in token2subtokens:
        newword = word
        # strip any punctuation before (if not before a number) or after: require at least 2 characters
        newword = trimPunctuation(word)

        if newword in word2count and word2count[newword].count > mincount:
            token2subtokens[word] = [newword]
        else:
            # todo : we should keep the split tokens!!!!
            # todo this really needs some work, probably shouldn't split with '.' to not stuff up websites etc.

            # try segmenting the word further using -, ~ and ., if we get words already seen then keep them
            # require at least one non-punc, non-numeral though:
            if re.search(ur'[^\W_\d]', newword, flags=re.UNICODE) is not None:
                newtokens = [x for x in re.split(ur'[\-~_/→，]', word, flags=re.UNICODE) if len(x) > 0]
                if len(newtokens) > 1 and len([x for x in newtokens if x not in word2count]) == 0:
                    if len([x for x in newtokens if word2count[x].count < mincount]) == 0:
                       token2subtokens[word] = newtokens
                if word not in token2subtokens: # if no success yet
                    newtokensdot = [x for x in re.split(ur'[\.\-\~_/→，]', word, flags=re.UNICODE) if len(x)>0]
                    if len(newtokensdot) > 1 and len([x for x in newtokensdot if x not in word2count]) == 0:
                        if len([x for x in newtokensdot if word2count[x].count < mincount]) == 0:
                            token2subtokens[word] = newtokensdot
                # else we do not add it

        #if word in token2subtokens:
        #    print word, token2subtokens[word]


def trimPunctuation(word):
    newword = word
    if (not word[0] in u'†') and len(word) > 1:
        # todo : we should keep the split tokens!!!!
        newword = re.sub(ur'^[\W_]+(?=[^\W\d_])', '', newword, flags=re.UNICODE)
        newword = re.sub(ur'^[^\w\-][\W-]*(?=[^\W_])', '', newword, flags=re.UNICODE)
        newword = re.sub(ur'(?<=[^\W_])\W+$', '', newword, flags=re.UNICODE)
    return newword

# need to wait till all secondaryTokenise is done as some counts may move above the min count
# assumed that adjustword2count has been called!
def tertiaryTokenise(line, word2count, token2splitToken, mincount):
    basicwords = basicTokenise(line)
    improvedwords = []
    for basicword in basicwords:
        #if word2count[basicword] < mincount:
        #if basicword not in word2count: # assumes we've adjusted
        #secondaryTokenise(basicword, word2count, token2splitToken, mincount)
        if basicword in word2count:
            #if word2count[basicword] > mincount:
            improvedwords.append(basicword)
            #    break
        elif basicword in token2splitToken:
            improvedwords.extend(token2splitToken[basicword])
        else: #i.e. word2count[basicword] < mincount or if its not in the original corpus:
            # we'll come here when treating a new word not in the original corpus
            secondaryTokenise(basicword, word2count, token2splitToken, mincount)
            if basicword in token2splitToken:
                improvedwords.extend(token2splitToken[basicword])
            else:
                replacementword = categoriseWord(basicword)
                improvedwords.append(replacementword)
                adjustWord2CountReplacement(word2count, basicword, replacementword) # already done elsewhere

    return improvedwords


# takes an open file object
# and builds a word2count dictionary using basic tokenisation:
def constructVocabularyStage1(corpusfile ):
    word2count = {}
    lineNumber = 0
    for line in corpusfile:
        lineNumber += 1
        words = basicTokenise(line)
        for word in words:
            try:
                word2count[word].count += 1
            except KeyError:
                word2count[word] = Vocab(count=1)
        #if lineNumber > 1000000: break
        if lineNumber % 100000 == 0: print lineNumber, "lines read" # about 22 million I think
    return word2count


def constructVocabularyStage2(corpusfile, word2count, mincount):
    token2splitToken = {}
    for line in corpusfile:
        basicwords = basicTokenise(line)
        #improvedwords = []
        for basicword in basicwords:
            if word2count[basicword].count < mincount:
                secondaryTokenise(basicword, word2count, token2splitToken, mincount)
                #if word in token2splitToken:
                #    improvedwords.extend(token2splitToken[word])
                #else:
                #    improvedwords.append(word)
    return token2splitToken


def adjustWord2Count(word2count, token2splitToken):
    for token in token2splitToken:
        for splittoken in token2splitToken[token]:
            word2count[splittoken].count += word2count[token].count
        del word2count[token]

# try to categorise the (rare) word:
# under current setup only returns one category:
def categoriseWord(word):

    newword = trimPunctuation(word)

    # NB: (?:[^\W_\d]|\'|\-)  means any letter or ' or -
    # [^W_\d](?:[^\W_\d]|\'|\-)* is any such sequence starting with a letter

    # group numbers together (we ignore the no. of digits, if it's decimal etc.), optional - in front
    # todo refine this so can't have 0 at front except just before a .
    if re.match(ur'([Nn]°)?\-?\d+(\.\d+)?$', newword, flags=re.UNICODE):
        newword = "_NUM_"
        '''
        # todo we could group numbers by pos/neg, no. of digits, dec or not, more than 2 after point etc.
        print "number:", word, len(word)
        lennum = re.findall(ur'\d', newword, flags=re.UNICODE)
        if len(word) not in digitdict: digitdict[len(word)] = 0
        digitdict[len(word)] += 1
        '''
    # look for dates with dots (needs to be before the dotnumber) :
    elif re.match(ur'[0123]?\d\.[0123]?\d\.([12]?\d)?\d\d$', newword, flags=re.UNICODE): # year last
        newword = "_DATE_"
        #print "date", word # todo nothing here!
    #elif re.match(ur'\d{2,4}\.\d{1,2}\.\d{1,2}$', newword, flags=re.UNICODE):
    elif re.match(ur'([12]?\d)?\d\d\.[0123]?\d\.[0123]?\d$', newword, flags=re.UNICODE): # year first
        newword = "_DATE_"
        #print "date", word # todo nothing here!

    # numbers of form 0000.00000.0000 etc.
    elif re.match(ur'(\d+\.)+\d*$', newword, flags=re.UNICODE):
        newword = "_DOTNUMBER_"

    # filenames: (before foreign as can include foreign characters)
    elif re.match(ur'[\w\-]+\.(?:pdf|svg|je?pg|doc|png|html?|aspx?)$', newword.lower(), flags=re.UNICODE):
        newword = "_FILENAME_"
        #print "filename:", word # doesn't seem to pick up many atm ...

    # look for foreign words (with non-french characters) # latin1 has too many non-french chars
    # Ll = latin 1, Zs = Separator Space, Cc = other control characters
    # Nd = number etc. Po & Ps = Punctuation
    #elif len([x for x in categories if x not in  ['Ll', 'Po', 'Nd']
    #          and x not in [ '-', '(', ')', u'«', u'»', '[', ']', u'€', u'’', u'“', u'”']]) > 0:
    #    newword = "_FOREIGN_"
    # note this will include alpha, beta etc.
    # note this will include 'modifier characters' (e.g. a diacritic but without a letter) as \w detects it
    # also includes ² which matches \w but doesn't match \d  wtf?!?!?!
    # todo exclude full width chars: e.g. u"＋ＮＡＴＵＲＡＬ"
    elif len([x for x in newword.lower() if x not in
            u'abcdefghijklmnopqrstuvwxyz0123456789ùûüÿàâæçéèêëïîôœ_' and re.match(ur'\w', x, re.UNICODE)]) > 0:
        #print "foreign?                                 ", newword, [x for x in newword.lower() if x not in
        #    u'abcdefghijklmnopqrstuvwxyz0123456789ùûüÿàâæçéèêëïîôœ_' and re.match(ur'\w', x, re.UNICODE)]
        newword = "_FOREIGN_"
        #print "foreign:", word
        # could subclassify as one character v multiple characters

    # look for acronyms:
    # this includes a lot of words in caps, and other stuff, todo check if lower version is known?
    # some roman numerals in here
    elif re.match(ur'(?:[^\W_\d]\.?)+$', newword, flags=re.UNICODE) and newword.isupper():
        newword = "_INITIALS_"
        #print "initials:", word

    # look for if word is only letters and all lower case:
    # this is where the interesting stuff is:, some foreign words in here
    elif re.match(ur'[^\W_\d](?:[^\W_\d]|\'|\-)*$', newword, flags=re.UNICODE) and newword.islower():
        newword = "_ALLLOWER_"
        #print "all lower:", word

    # look for first letter in upper case, the rest in lower case: (we need the min trick as python doesn't check in the right order)
    # includes some 2 & 3 letter abbreviations Etc, It , some hyphenated place names
    # elements Hg
    elif len(word) > 1 and newword[0].isupper() and re.match(ur'(?:[^\W_\d]|\'|\-)+$', newword[min(1,len(word)-1):], flags=re.UNICODE):
        newword = "_FIRSTUPPER_"
        #print "first upper:", word

    # look for mixed upper and lower:
    # a lot of d' or de or l'or -l' etc.l+ caps, some foreign e.g. el-Name al-Name todo separate l/d
    elif len(word) > 1 and re.match(ur'[^\W_\d](?:[^\W_\d]|\'|\-)*$', newword, flags=re.UNICODE) and not newword.islower() and \
        not newword.isupper():
        newword = "_MIXEDUPPERLOWER_"
        #print "mixed upperlower", word

    # look for pure punctuation:
    elif re.match(ur'[^\w_]+$', newword, flags=re.UNICODE):
        newword = "_PUNCT_"
        #print "punct", word

    # look for a mix of upper case letters and numbers (dashes and underscores and dots allowed):
    elif re.match(ur'[\w\-\.]+$', newword, flags=re.UNICODE) and newword.isupper():
        newword = "_NUMUPPERMIX_"
        #print "mix nums and uppers", word



    # look for 39e / 15ème / 5è: etc.
    elif re.match(ur'\d+(?:e|i?èmes?|è|i?ères?|emes?|nd|rd|th|st)$', newword, flags=re.UNICODE):
        newword = "_ORDINAL_"
        #print "ordinal", word

    # look for area: e.g. 300x200
    elif re.match(ur'\d+(?:\.\d+)?x\d+(?:\.\d+)?$', newword, flags=re.UNICODE):
        newword = "_AREA_"
        #print "area", word

    # look for a web addresse, the www is optional:
    elif re.match(ur'(?:www\.)?(?:[\w\-]+\.)+(?:edu|org|comfgov|com|gov|tv|net|info|mil|ac|biz|art|ep|bz|gouv|'
                  ur'sk|cz|ie|ua|cu|by|in|eu|pt|nl|es|lu|lib|nu|bf|rm|go|id|co|ch|de|ru|fm|fr|be|it|ee|'
                  ur'ws|yu|pa|bg|tk|pf|uk|jp|ro|pl|se|au|dk|lv|hr|fi|ae|za|bg|ge|lu|us|at|ba|cl|pt|ca|'
                  ur'gl|si|om|gr|mg|nc|hu|ma)+', newword, flags=re.UNICODE):
        newword = "_WEBSITE_"
        #print "website", word

    # some www don't have an ending:
    elif re.match(ur'www\.\w+', newword, flags=re.UNICODE):
        newword = "_WEBSITE_"

    # look for a time
    elif re.match(ur'[0-2]?[0-9]h(?:[0-5][0-9])?', newword, flags=re.UNICODE):
        newword = "_TIME_"
        #print "time type1", word

    # note can be anything after it atm... may cause problems
    elif re.match(ur'(?:\d?\d[Hh])?\d+min(?:utes)?(?:\d\d)?', newword, flags=re.UNICODE):
        newword = "_TIME_"
        #print "time type2", word

    # partially segmented ISBN:
    elif re.match(ur'[0-3]\-\d{2,6}', newword, flags=re.UNICODE):
        newword = "_PARTIALISBN_"
        #print "isbn part", word

    # num dash num e.g. 2-3
    elif re.match(ur'\d\-\d$', newword, flags=re.UNICODE):
        newword = "_NUMDASHNUM_"
        #print "num dash num", word

    # check if there's a . at the end, maybe with a ' before it:
    #elif (word.endswith('.') and newword[:-1] in word2count) or \
    #    (word.endswith("'.") and newword[:-2] in word2count):
    #    newword = newword[:-1]
    #    print "punc before/after", word # todo none here!!

    elif re.match(ur'†', newword, flags=re.UNICODE):
        newword = "_CHURCH_"
        #print "church", word

    # a@b (with no dots after @) seems to be missed:
    # todo should check if replacing @ with a makes a word
    # e.g. Les@anarchistes, Cryptogra@phie, System@tic but also 'Nothing@All' 'd@ns'
    elif re.match(ur'([\w\-]\.)*[\w\-]+@[\w\-]+(?:\.[^\W\d]{2,4}){0,2}$', newword, flags=re.UNICODE):
        newword = "_AATB_"
        #print "a at b", word

    elif re.match(ur'\d+bis$', newword, flags=re.UNICODE):
        newword = "_BIS_"
        #print "bis", word

    # alphanumeric hat alphanumeric seems to come up a lot
    elif re.match(ur'\w\^\w$', newword, flags=re.UNICODE):
        newword = "_HAT_"
        #print "hat", word # todo none here

    # date range is missed:
    elif re.match(ur'(janv?|févr?|mars?|avri?|mai|juin|juil|août|sept?|octo?|nove?|déc)\.?\-'
                  ur'(janv?|févr?|mars?|avri?|mai|juin|juil|août|sept?|octo?|nove?|déc)\.?$', newword.lower(), flags=re.UNICODE):
        newword = "_DATERANGE_"
        print "date range", word # todo none here

    # if after all the others it has only letters call it a word:
    elif re.match(ur'[^\W_\d](?:[^\W_\d]|\'|\-)*$', newword, flags=re.UNICODE):
        newword = "_OTHERWORD_"
        # never seems to come in here ...
        #print "                                          ", newword, newword
        #print "other word", word # todo this is covered by the alllower and similar above!

    # numbers followed by one or two letters: (this includes some years like 1983a etc.)
    # todo this doesn't seem to be a particularly coherent group! some years
    # todo e.g. 1987b 2005a etc.
    elif re.match(ur'(?:\-?\d+\.)?\d+[^\W\d_]{1,2}$', newword, flags=re.UNICODE):
        newword = "_MEASURE_"
        #print "measure", word

    # letters followed by numbers, can have _ and -:
    # most common x l a b : could sub categorise for these
    elif re.match(ur'[^\W\d][\d\-_]+$', newword, flags=re.UNICODE):
        newword = "_MODEL_"
        #print "model", word

    # known abbreviations: (prob should be earlier)
    # last punctuation is removed as it is stripped earlier
    elif re.match(ur'(km2|i\.e\.?|e\.g\.?|a\.k\.a\.?)', newword, flags=re.UNICODE):
        newword = "_ABBREV"
        #print "abbrev", word
    # no. ? n°
    #elif re.match(ur'n°')

    # todo these should be cut in 2 and see if the word-like part is a word
    elif re.match(ur'[^\W\d]+\d+$', newword, flags=re.UNICODE):
        newword ="_LETTSNUMS_"

    # numbers followed by letters
    elif re.match(ur'\d+[^\W\d]+$', newword, flags=re.UNICODE):
        newword = "_NUMSLETTS_"

    elif re.match(ur'(([^\W\d]|\')\-)+([^\W\d]|\')$', newword, flags=re.UNICODE):
        newword = "_HYPHENATED_"

    # these are with letters rather than pure numbers:
    elif re.match(ur'[nN]°\w+$', newword, flags=re.UNICODE):
        newword = "_NUMERONAME_"

    # if a word
    else:
        #print word, "\t", newword #, len(word) > 1, re.match(ur'[^\W_\d]([^\W_\d]|\'|\-)*$', word, flags=re.UNICODE), not word.islower(), not word.isupper()
        newword = "_OTHER_"
        #print "other", word

    #if len(newword) > 0:
    if newword[0] == "_":
        #if newword not in replacedwords: replacedwords[newword] = []
        #replacedwords[newword].append(word)
        pass
    else:
        print "Error: unclassified!"
    return newword

def adjustWord2CountReplacement(word2count, oldword, newword):
    if oldword in word2count:
        if newword not in word2count: word2count[newword] = Vocab(count=0)
        word2count[newword].count += word2count[oldword].count
        del(word2count[oldword])
    else:
        #print "not in word2count", oldword
        pass


class Tokeniser():
    # last 2 can be filenames of json files or dictionaries
    def __init__(self, fullfilename, mincount, word2count=None, token2subtokens=None):
        self.filename = fullfilename
        self.MINCOUNT = mincount
        if word2count is None:
            self.word2count = {}
            self.token2subtokens = {}
            self.getVocab()
        elif type(word2count) == str and type(token2subtokens) == str:
            self.word2count, self.token2subtokens = loadFiles(word2count, token2subtokens)
        else:
            self.word2count = word2count
            self.token2subtokens = token2subtokens

    def getVocab(self):
        with codecs.open(self.filename, encoding='utf-8') as corpusfile:
            self.word2count = constructVocabularyStage1(corpusfile)
        print "vocab size stage 1: ", len(self.word2count)

        # we do a loop first to divide up tokens which are rare but divisible:
        for word in self.word2count.keys():
            if self.word2count[word].count < self.MINCOUNT:
                secondaryTokenise(word, self.word2count, self.token2subtokens, self.MINCOUNT)

        # adjust the counts:
        print "words to replace  : ", len(self.token2subtokens)
        adjustWord2Count(self.word2count, self.token2subtokens)
        print "vocab size stage 2: ", len(self.word2count)

        # now replace any remaining tokens with insufficient counts by some category term:
        for word in self.word2count.keys():

            if self.word2count[word].count < self.MINCOUNT:
                replacementword = categoriseWord(word)
                self.token2subtokens[word] = [replacementword]
                adjustWord2CountReplacement(self.word2count, word, replacementword)


    def __iter__(self):
        #outsentences = []
        with codecs.open(self.filename, encoding='utf-8') as corpusfile:
            lineNumber = 0
            for line in corpusfile:
                tokens = tertiaryTokenise(line, self.word2count, self.token2subtokens, self.MINCOUNT)
                #print tokens
                #outsentences.append(tokens)
                lineNumber += 1
                #if lineNumber > 20: break
                yield tokens

        print "vocab size stage 3: ", len(self.word2count)
        #return outsentences

    def tokeniseLine(self, line):
        return tertiaryTokenise(line, self.word2count, self.token2subtokens, self.MINCOUNT)

    def saveFiles(self, vocabFileName, replaceFileName):
        with codecs.open(vocabFileName, mode='w', encoding='utf8') as vfile:
            # gensim Vocab object is not serialisable
            outdict = dict([(x,y.count) for (x,y) in self.word2count.iteritems()] )
            json.dump(outdict, vfile)
        with codecs.open(replaceFileName, mode='w', encoding='utf8') as rfile:
            json.dump(self.token2subtokens, rfile)


def loadFiles(vocabFileName, replaceFileName):
    word2count, token2subtokens = {}, {}
    with codecs.open(vocabFileName, mode='r', encoding='utf8') as vfile:
        # gensim Vocab object is not serialisable
        word2count = json.load(vfile)
        for word in word2count.keys():
            word2count[word] = Vocab(count=word2count[word])
    with codecs.open(replaceFileName, mode='r', encoding='utf8') as rfile:
        token2subtokens = json.load(rfile)
    return word2count, token2subtokens



# run with bumblebee?
def main():

    corpusdirectory = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/"
    #corpusdirectory = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/divided/"

    #corpusfilename = "mi-frwiki1" # half wiki
    corpusfilename = "frwiki_net.tok" # full wiki
    #corpusfilename = "mini_frwiki_net_train.tok" # first 50k lines of dev part
    #corpusfilename = "frwiki_net_dev.tok" # 7,000,000 lines
    #corpusfilename = "editions.tok"

    fullfilename = os.path.join(corpusdirectory, corpusfilename)

    MINCOUNT = 50
    word2count = {}
    replacedwords = {}
    with codecs.open(fullfilename, encoding='utf-8') as corpusfile:
        word2count = constructVocabularyStage1(corpusfile)

    # we do a loop first to divide up tokens which are rare but divisible:
    token2subtokens = {}
    for word in word2count.keys():
        if word2count[word].count < MINCOUNT:
            secondaryTokenise(word, word2count, token2subtokens, MINCOUNT)

    # adjust the counts:
    #print token2subtokens
    adjustWord2Count(word2count, token2subtokens)

    # now replace any remaining tokens with insufficient counts by some category term:
    for word in word2count.keys():

        if word2count[word].count >= MINCOUNT:
            #print "adding 1"
            #totaltokens += word2count[word]
            pass
        else:
            # i.e. less than MINCOUNT
            #print x
            replacementword = categoriseWord(word)
            adjustWord2CountReplacement(word2count, word, replacementword)
            if replacementword not in replacedwords: replacedwords[replacementword] = []
            replacedwords[replacementword].append(word)
            #toolowtypes +=1
            #toolowtokens += word2count[word]

        #print runningtotal, totaltokens
        #if totaltokens > runningtotal + 10: break

    print "final vocab size:", sum([x.count for x in word2count.itervalues()])
    #print "tokens:", totaltokens, "types:", len(word2count)
    #print "too low tokens:", totaltokens, "too low types:", toolowtypes
    #print "fraction too low tokens", 1.0*toolowtokens/totaltokens
    #print "fraction too low types", 1.0*toolowtypes/len(word2count)

    if "" in word2count: print "empty string in vocab, something went wrong!"
    if " " in word2count: print "space in vocab, something went wrong!"

    # now save a vocab file with low freq words replaced by _UNK
    # one word per line
    vocabfilename = "wiki_vocab.json"
    replaceFileName = "wiki_replace.json"
    '''
    with codecs.open(corpusdirectory + vocabfilename, 'w', encoding='utf-8') as vocabfile:
        vocabfile.write("_UNK\n")
        for x in sorted(word2count.keys()):
            if word2count[x].count > MINCOUNT:
                vocabfile.write(x + "\n")
    '''

    with codecs.open(corpusdirectory + vocabfilename, mode='w', encoding='utf8') as vfile:
        # gensim Vocab object is not serialisable
        outdict = dict([(x,y.count) for (x,y) in word2count.iteritems()] )
        json.dump(outdict, vfile)
    with codecs.open(corpusdirectory + replaceFileName, mode='w', encoding='utf8') as rfile:
        json.dump(token2subtokens, rfile)

    # save lists of replaced to check if good groupings
    replacedFileName = "replaced.json"
    with codecs.open(corpusdirectory + replacedFileName, 'w', encoding='utf-8') as replfile:
        json.dump(replacedwords, replfile)

if __name__ == "__main__":
    main()