import codecs
import os
import math

__author__ = 'nparslow'


# todo somehow empty string and/or space is getting in here, need to remove that!
def loadNgrams( ngramfilename, n=2 ):
    nGramDict = {}
    with codecs.open(ngramfilename, mode='r', encoding='utf8') as nfile:
        for line in nfile:
            # one n-gram per line, n-gram is separated by spaces, count by a tab
            line = line.strip()
            try:
                ngram, count = line.split('\t')
                ngram = tuple(ngram.split(' '))
                if len(ngram) == n:
                    count = int(count)
                    nGramDict[ngram] = count
                else:
                    print "Ngram too short/long:", line
            except:
                print "Ngram line problem:", line
    return nGramDict

def getNminusOneGramDict( nGramDict ):
    nmoGramDict = {}
    for ngram in nGramDict:
        nmogram = tuple(ngram[:-1])
        if nmogram not in nmoGramDict: nmoGramDict[nmogram] = 0
        nmoGramDict[nmogram] += nGramDict[ngram]
    return nmoGramDict


# returns the total counts so we can do smoothing on the fly
# takes an ngram and a nMinusOne-gram dict
def probabiliseNgramDicts( nGramDict, nmoGramDict):
    totalcounts = 1.0*sum(nGramDict.values())
    for ngram in nGramDict:
        nGramDict[ngram] /= totalcounts
    for nmogram in nmoGramDict:
        nmoGramDict[nmogram] /= totalcounts # total count will be the same, indepedent of n
    return totalcounts

# when using output prob should divide by length of tokens {as log(a^b) = b*log(a)}
# you shouldn't add start tokens to the token list before calling this function as it will do it.
def analyseTokens( toks, nGramDict, nmoGramDict, totalcounts ):
    # get the length of the n-grams:
    n = len(nGramDict.keys()[0]) # todo this is probably inefficient
    smoothingp = 1.0/totalcounts

    newtoks = ["_START"]*(n-1) + toks + ["_START"]*(n-1)

    pSequence = []
    for i in range(n, len(newtoks)):
        nGram = tuple( toks[i-n:i] )
        nmoGram = tuple( toks[i-n:i-1])
        p = smoothingp
        if nGram in nGramDict:
            p = nGramDict[nGram] / nmoGramDict[nmoGram]
        elif nmoGram in nmoGramDict:
            p = smoothingp / nmoGramDict[nmoGram]
        pSequence.append(p)

    return pSequence
    # take logs and sum:
    #return sum([math.log(x) for x in pSequence])


def getNgramDicts( ngramfilename, n=2 ):
    nGramDict = loadNgrams(ngramfilename, n)
    nmoGramDict = getNminusOneGramDict(nGramDict)

    totalcounts = probabiliseNgramDicts(nGramDict, nmoGramDict)

    return nGramDict, nmoGramDict, totalcounts

def convertToRelativeProbs( nGramDict, nmoGramDict ):
    for ngram in nGramDict:
        nGramDict[ngram] /= nmoGramDict[tuple(ngram[:-1])]

def main():

    #ngramfile = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/ngram_wiki_count.txt"
    ngramfile = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/trigram_wiki_count.txt"

    nGramDict, nmoGramDict, totalcounts = getNgramDicts(ngramfile)

    convertToRelativeProbs(nGramDict, nmoGramDict)

    #ngramoutfile = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/norm_ngram_wiki_count.txt"
    ngramoutfile = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/norm_trigram_wiki_count.txt"
    with codecs.open(ngramoutfile, mode='w', encoding='utf8') as nfile:
        for nGram in nGramDict:
            # one n-gram per line, n-gram is separated by spaces, count by a tab
            nfile.write( " ".join(nGram) + "\t" + str(nGramDict[nGram]) + "\n")


if __name__ == "__main__":
    main()




