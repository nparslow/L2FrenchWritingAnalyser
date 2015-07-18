import codecs
import json
import os

import createKnownDict

__author__ = 'nparslow'

MINCOUNT = 50

# we'll start with bigrams:
def fileToNgrams( infilename, word2count, token2splitToken, n=2, mincount=MINCOUNT ):

    nGramCount = {}
    with codecs.open(infilename, encoding="utf-8") as infile:
        for lineNumber, line in enumerate(infile):
            if lineNumber % 10000 == 0: print "ngraming line number", lineNumber
            toks = createKnownDict.tertiaryTokenise(line, word2count, token2splitToken, mincount)
            countNgrams(nGramCount, toks, n )
    return nGramCount


# NB we currently don't divide into sentences :/
# todo: currently only does n, should do all up to and including n, i.e. 3 would do 3, 2 and 1
def countNgrams(nGramDict, toks, n):
    assert n > 0 # 1 should never be needed, but should still work ...
    toks = ["_START"]*(n-1) + toks + ["_START"]*(n-1)
    for i in range(n, len(toks)):
        nGram = tuple( toks[i-n:i] )
        if nGram not in nGramDict: nGramDict[nGram] = 0
        nGramDict[nGram] += 1
    return



# run with bumblebee?
def main():

    n = 3

    corpusdirectory = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/"
    #corpusdirectory = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/divided/"

    #corpusfilename = "mi-frwiki1" # half wiki
    corpusfilename = "frwiki_net.tok" # full wiki
    #corpusfilename = "mini_frwiki_net_train.tok" # first 50k lines of dev part
    #corpusfilename = "frwiki_net_dev.tok" # 7,000,000 lines
    #corpusfilename = "editions.tok"

    fullfilename = os.path.join(corpusdirectory, corpusfilename)


    word2count = {}
    replacedwords = {}

    # we have to read twice, once to create the dictionary of known v unknown words:
    with codecs.open(fullfilename, encoding='utf-8') as corpusfile:
        word2count = createKnownDict.constructVocabularyStage1(corpusfile)

    # we do a loop first to divide up tokens which are rare but divisible:
    token2subtokens = {}
    for word in word2count.keys():
        if word2count[word].count < MINCOUNT:
            createKnownDict.secondaryTokenise(word, word2count, token2subtokens, MINCOUNT)

    # adjust the counts:
    #print token2subtokens
    createKnownDict.adjustWord2Count(word2count, token2subtokens)

    # now replace any remaining tokens with insufficient counts by some category term:
    for word in word2count.keys():

        if word2count[word].count >= MINCOUNT:
            #print "adding 1"
            #totaltokens += word2count[word]
            pass
        else:
            # i.e. less than MINCOUNT
            #print x
            replacementword = createKnownDict.categoriseWord(word)
            createKnownDict.adjustWord2CountReplacement(word2count, word, replacementword)
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

    # now we can loop a second time and get the n-grams (now we know which words to treat or to subtokenise)
    nGramsDict = fileToNgrams(fullfilename, word2count, token2subtokens, mincount=MINCOUNT, n=n)

    # now save a vocab file with low freq words replaced by _UNK
    # one word per line
    vocabfilename = "ngram_wiki_vocab.json"
    replaceFileName = "ngram_wiki_replace.json"
    nGramFileName = "ngram_wiki_count.txt"
    if n == 2:
        vocabfilename = "bigram_wiki_vocab.json"
        replaceFileName = "bigram_wiki_replace.json"
        nGramFileName = "bigram_wiki_count.txt"
    elif n == 3:
        vocabfilename = "trigram_wiki_vocab.json"
        replaceFileName = "trigram_wiki_replace.json"
        nGramFileName = "trigram_wiki_count.txt"

    with codecs.open(corpusdirectory + vocabfilename, mode='w', encoding='utf8') as vfile:
        # gensim Vocab object is not serialisable
        outdict = dict([(x,y.count) for (x,y) in word2count.iteritems()] )
        json.dump(outdict, vfile)
    with codecs.open(corpusdirectory + replaceFileName, mode='w', encoding='utf8') as rfile:
        json.dump(token2subtokens, rfile)
    with codecs.open(os.path.join(corpusdirectory, nGramFileName), mode='w', encoding='utf8') as nfile:
        for nGram in nGramsDict:
            # one n-gram per line, n-gram is separated by spaces, count by a tab
            nfile.write( " ".join(nGram) + "\t" + str(nGramsDict[nGram]) + "\n")

    # save lists of replaced to check if good groupings
    replacedFileName = "ngram_replaced.json"
    with codecs.open(corpusdirectory + replacedFileName, 'w', encoding='utf-8') as replfile:
        json.dump(replacedwords, replfile)

if __name__ == "__main__":
    main()