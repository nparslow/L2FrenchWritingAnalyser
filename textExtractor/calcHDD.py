import math
import re
from itertools import groupby
__author__ = 'nparslow'

# HD-D = summed proba of finding a word in a 42 word sample
# sum over all words (1 - hypergeom (0, 42, n, N) where n = seen occurances, N = all word occurances

def nCr(n,r):
    #print "nCr", n, r
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def hypergeom(k, n, K, N):
    #print k,n,K,N
    #print K,k, ",", N-K, n-k, ",", N, n
    return  1.0*nCr(K, k) * nCr(N - K, n - k) / nCr(N, n)

def freqDist( tokens ):
    return [tokens.count(x) for x in set(tokens)]

# this should be the same measure as D (VOCD) but more stable/accurate
# input is a list of tokens (or lemmas or whatever you want)
# also called SOP-42 in the orig paper
def calcHDD( tokens ):
    assert len(tokens) >= 42 # otherwise current form of calc doesn't work
    # get the frequency distribution
    fdist = freqDist(tokens)
    #print "calcHDD"
    #print tokens
    #print fdist
    HDD = 0.0
    for freq in fdist:
        HDD += (1-hypergeom(0,42,freq,len(tokens)))
    return HDD

def calcHDDfromFreq( fdist ):
    HDD = 0.0
    for freq in fdist:
        HDD += (1-hypergeom(0,42,freq,sum(fdist)))
    return HDD

def calcYuleK( tokens ):
    # get the frequency distribution
    fdist = freqDist(tokens)
    M2 = sum([len(list(g))*(freq**2) for freq,g in groupby(sorted(fdist))])
    M1 = len(fdist)
    #print "yo"
    return 10000*(M2-M1)/math.pow(M1,2)

def calcYuleKfromFreq( fdist ):
    M2 = sum([len(list(g))*(freq**2) for freq,g in groupby(sorted(fdist))])
    M1 = len(fdist)
    #print "yo"
    return 10000*(M2-M1)/math.pow(M1,2)

# this seems to be wrong???
def calcMaas( tokens ):
    # get the frequency distribution
    fdist = freqDist(tokens)
    V = len(fdist)
    N = len(tokens)
    return (math.log(N)-math.log(V))/math.pow(math.log(N),2)

def calcTextLengthAdjustedTTR( tokens ):
    ntypes = len(set(tokens))
    ntokens = len(tokens)
    return ntypes / math.sqrt(2.0*ntokens)

def calcUniqueBigramRatio( tokens ): # this will be used with lemmas most frequently
    bigrams = [(tokens[i],tokens[i+1]) for i in range(len(tokens)-1)]
    uniqueBigrams = set(bigrams)
    return len(uniqueBigrams) / math.sqrt(2.0*len(bigrams))

def calcHDDtest():
    # re. 2007 paper
    testtext = u"The girl was stolen a bread, but Chaplin take a fault. So, they are going to put a Chaplin in jail." \
               u" But a woman saw that the girl stolen the bread, so they take Chaplin and the girl." \
               u" When they was going to jail the girl and Chaplin ran away." \
               u" They go to sit and talk about where they live." \
               u" The girl say that she live no where." \
               u" So they dreaming a home where they can take orange in the tree and eat a breakfast in a kitchen." \
               u" The Chaplin say that do the work then we got a house."

    lemmatisedtesttext = re.sub(ur"[^\w\s]", "", testtext.lower())

    for x in sorted(set(lemmatisedtesttext.split()), key=lambda x: lemmatisedtesttext.split().count(x)):
        print x, lemmatisedtesttext.split().count(x), 1-hypergeom(0,42,lemmatisedtesttext.split().count(x), 100)

    fdist = freqDist(lemmatisedtesttext.split())
    print sorted(fdist)
    print sum(fdist), len(fdist)

    print calcHDD(lemmatisedtesttext.split())
    print calcYuleK(lemmatisedtesttext.split())
    print calcMaas(lemmatisedtesttext.split())

    testtext = u"a big a big house"
    print "text length adjusted TTR:", calcTextLengthAdjustedTTR( testtext.split()) # expect 0.95
    print "unique bigram ratio", calcUniqueBigramRatio( testtext.split() ) # expect 1.06

    print "testing hypergeom"
    n = 10
    k = 5
    N = 20
    K = 4
    print hypergeom(k, n, K, N)


#calcHDDtest()


if __name__ == "__main__":
    calcHDDtest()