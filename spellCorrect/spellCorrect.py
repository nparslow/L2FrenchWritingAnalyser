# coding=utf-8
__author__ = 'nparslow'

# from http://norvig.com/spell-correct.html

import re, collections, codecs
import xml.etree.cElementTree as ET
import json
import os.path

alphabet = u'abcdefghijklmnopqrstuvwxyzùûüÿàâæçéèêëïîôœ' + \
    u'ABCDEFGHIJKLMNOPQRSTUVWXYZ\xd9\xdb\xdc\u0178\xc0\xc2\xc6\xc7\xc9\xc8\xca\xcb\xcf\xce\xd4\u0152' + \
    u'\'`-' # lower case, upper case and punct

# split a text into words
def words(text):
    all =  re.findall(ur'((?:\'|\`|\-|[^\W\d])+)', text.lower(), flags=re.UNICODE)
    #print all
    #all = re.findall(ur'\b[abcdefghijklmnopqrstuvwxyzùûüÿàâæçéèêëïîôœ\'\`\-]+\b', text, flags=re.UNICODE)
    #all = re.findall(ur'\b[\'\`\-' + alphabet + ur']+\b', text, flags=re.UNICODE)
    all = re.findall(ur'(?<=[\b\s])[' + alphabet + ur']+(?=[\b\s])', text, flags=re.UNICODE)
    #print all
    # use (?: ) to not capture individual letters individually

    return all

def wordsFromXML( xmlfile ):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    count = 0
    #for textElement in root.iter("text"):
    #    print textElement.tag, textElement.text

    #    count += 1
    #    if count > 10: break

    #print root.tag
    #for child in root:
    #    print child.tag

    #    count += 1
    #    if count > 10: break
    outputText = ""
    for textElement in root.iter("{http://www.mediawiki.org/xml/export-0.10/}text"):
        #print pageElement.tag
        #for revision in pageElement.findall("revision"):
        #    print revision.tag
        #    for textElement in revision.findall('text'):
        #        print textElement.tag
        #print textElement.tag#, textElement.text
        # wiki meta chars
        #print textElement.text

        # we have to remove triple chars before doubles as otherwise a four character will be removed as 2 doubles
        afterHTMLescape = re.sub(ur'&\w{1,6};', ur' ', textElement.text) # 6 seems to be the max length
        #afterHTMLescape = textElement.text
        afterTags = re.sub(ur'\<[^\/]+\/\>|\<\/?(ref|math|gallery|center|!--.+--|BR|br)( \w+=.+)?\>', ur' ', afterHTMLescape)
        afterThrees = re.sub( ur'\'\'\'|\.\.\.', ur' ', afterTags)
        afterTwos = re.sub(ur'\{\{|\}\}|\[\[|\]\]|==|\*\*|\'\'', ur' ', afterThrees)
        reHTTP = ur'http[^ ]+'
        reWikiMeta = ur'\||\[|\]\'\'|=|#|\*'
        # punctuation:
        rePunc = ur'\{|\}|\(|\)|\[|\]|\?|\.|\!|\:|,|;|«|»|\]|…'
        afterPunc = re.sub( reHTTP + ur'|' + reWikiMeta + ur'|' + rePunc, ur' ', afterTwos)
        # todo replace e.g. {{e}} with ième etc.
        # todo if first word in sentence and only first letter is a capital, ignore the word (prob just ignore first
        # word in sentences, or after a full stop <- this looks good

        #print words(afterPunc)
        outputText += " " + afterPunc

        count += 1
        if count % 100 == 0 : print "articles:", count
        #if count > 300: break
    return outputText


def train(features):
    model = collections.defaultdict(lambda : 1) # default is 1 for smoothing, so minimum for a seen word is 2
    for f in features:
        model[f] += 1
    return model

NWORDS = {}
#lines =   20000
#lines =  100000
#lines = 1000000
lines = 10000000 # 10 million
wikifile =   str(lines) + "_lines.xml"
dictfile = str(lines) + "_dict.json"
basedir = '/home/nparslow/Documents/AutoCorrige/SpellChecker/'

NWORDS = {}
if (os.path.isfile(basedir+dictfile)):
    print "loading dict file", wikifile
    with codecs.open(basedir + dictfile, 'r', encoding='utf-8') as infile:
        NWORDS = collections.defaultdict(lambda : 1, json.load(infile))
else:

    NWORDS = train(words(wordsFromXML(basedir + wikifile)))

    with codecs.open(basedir + dictfile, 'w', encoding='utf-8') as outfile:
        json.dump(NWORDS, outfile)



#alphabetset = set([])
#for word in NWORDS:
#    for character in word:
#        if character not in alphabetset:
#            alphabetset.add(character)
#print alphabet
#print "".join(sorted(alphabetset))


# all edit distance of 1 from the word
def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word)+1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a+b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

# all edit distance of 2 (this is going to be very large)
def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

# this is very slow, prob need to improve the algo running time
def correct(word):
    # hierarchy, all known edits of distance 1 more likely than all known edits of distance 2
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    # include the word itself in the list
    return max(candidates, key=NWORDS.get)


#wordsFromXML('/home/nparslow/Documents/AutoCorrige/SpellChecker/frwiki-latest-pages-articles.xml')
#wordsFromXML('/home/nparslow/Documents/AutoCorrige/SpellChecker/20000_lines.xml')
#print NWORDS


#print correct("ecole") # need to weight lower case to capital heavier than lower case to lower case
#print correct("Ecole")
#print correct("fontt")

def testWords():
    # using the standard test word set:
    nWellDone = 0
    nAll = 0
    with codecs.open(basedir + "testWords.txt", encoding='utf-8') as f:
        nlines = 0
        for line in f:
            nlines += 1
            if nlines > 1: # to avoid header line
                incorrectWord, correctWord = line.strip().split('\t')
                corrected = correct(incorrectWord)
                correctWords = [correctWord]
                if "/" in correctWord:
                    correctWords = correctWord.split('/') # as there are 2 possible correct answers
                print incorrectWord, correctWord, corrected, corrected in correctWords
                nAll += 1
                if corrected in correctWords: nWellDone += 1

    print nWellDone, nAll, 1.0*nWellDone/nAll

testWords()

# using only unigram frequencies (and including the word itself)
# 10 articles : 0.11  accuracy
# 66 articles (20k lines of wiki) : 0.23 (37/163)
# 300 articles  (< 100k lines of wiki) : (56/163) : 0.34
# 4307 articles ( 1mil lines of wiki) : ( 76 / 163 ) : 0.46 (took about 5-10mins i guess)
