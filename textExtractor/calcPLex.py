import codecs
import json
import random
import re
import subprocess
import math
import numpy as np
from scipy.optimize import curve_fit
from scipy.misc import factorial
import matplotlib.pyplot as plt

__author__ = 'nparslow'


#def poissonW(total, k, lamb):
#    return total*(lamb**k/factorial(k)) * np.exp(-lamb)

def alternativeSfunction(x, a, b):
    return a*np.power(x, b)  # note using math.log will crash, np.log is the natural log by default

def poissonMass( k, lamb):
    return (lamb**k/factorial(k)) * np.exp(-lamb)

def poissonCount( N ):
    return lambda k, lamb: N * poissonMass(k, lamb)

def Sfunction(x, s):
    # need to convert x to a float?
    #print x
    if s > 0 :
        #print s
        #print x
        return np.log(x)/np.log(s) * 100.0 # note using math.log will crash, np.log is the natural log by default
    else:
        return 0.0*x

# this will crash if N==0, but N will usually be an array, so not sure how to test ...
def TTRfunction(N, D):
    if D > 0:
        return (D/N)*(np.power(1+2*(N/D), 0.5)-1)
    else:
        return 0.0*N

# the inverse of the TTR function, i.e. calculate D from TTR and N
def DfromTTRN(TTR, N):
    return (-1.0*N/2)*np.power(TTR,2)/(TTR-1.0)

# need a list of wordforms or lemmas, and a dictionary which converts them to frequency ranks from a corpus
def calcPLex( wordforms, wordform2freqrank, difficultRank = 500):
    #print "freq dict", len(wordform2freqrank.keys())
    # values from 0 to 10 inclusive, will include the no. of hard words in each group of 10 words:
    distribution = [0]*11
    counter = 0
    for i in range(len(wordforms)):
        if i > 0 and i%10 == 0:
            distribution[counter] += 1
            counter = 0
        wordform = wordforms[i]
        if wordform in wordform2freqrank:
            freq, rank = wordform2freqrank[wordform]
            #print freq, rank, wordform, difficultRank
            if rank > difficultRank:
                counter += 1
        # common words and words not in the lexique are ignored

    x = np.linspace(0,10,num=11) # i.e. 11 samples
    y = np.array(distribution, dtype=float)

    #nHard = sum([i*distribution[i]] for i in range(len(distribution))])
    #npoisson = lambda x,y : poissonW(wordlength, x, y)
    #print "distribution:"
    #print distribution
    #print y
    #npoisson = lambda x,y : poissonMass(x, y)
    npoisson = poissonCount(sum(distribution))
    popt, pcov = curve_fit(npoisson, x, y, p0=[1.5]) # start with lambda = 1.5

    #print popt, pcov
    return popt, pcov


# 0 presumed as start of first difficulty bin range
# to maintain an even bin length, after the last bin is ignored
def calcS( wordforms, wordform2freqAndrank, difficultybins = (500,1000,1500,2000,2500,3000), samplesize=50):
    assert(len(difficultybins) > 0)
    #print wordforms

    allcumcoverages = []
    for subi in range(len(wordforms)):  #range(len(wordforms) / samplesize): # int division
        first = subi #*samplesize
        last = first + samplesize

        subsample = []
        if last <= len(wordforms):
            subsample = wordforms[first:last]
        else:
            # add words from the beginning
            # this is not the original S, but it means all words count evenly
            subsample = wordforms[first:] + wordforms[:last-len(wordforms)]

        coverages = []
        for i in range(len(difficultybins)):
            coverages.append( 0.0 )
        #coverages = [0.0]*(len(difficultybins))
        for wordform in subsample:
            if wordform in wordform2freqAndrank:
                freq, rank = wordform2freqAndrank[wordform]
                bin = 0
                if rank > difficultybins[-1]: continue # ignore words beyond the last difficulty limit
                for binlimi in range(len(difficultybins)):
                    binlim = difficultybins[binlimi]
                    bin = binlimi # binlimi corresponds to the first difficulty bar
                    if rank < binlim: break

                #print wordform, freq, rank, bin
                coverages[bin] += 1
        # add the previous cumcoverage with the next coverage
        cumulativecoverages = [coverages[0]]
        for cov in coverages[1:]:
            cumulativecoverages.append( cumulativecoverages[-1] + cov)
        for i in range(len(cumulativecoverages)):
            cumulativecoverages[i] = cumulativecoverages[i]*100.0/samplesize
        #print cumulativecoverages
        allcumcoverages.append(cumulativecoverages)

    # so we have a list of lists, need to fit
    func = Sfunction
    # take average (this is cheating)
    cumufreqs = [0.0]*len(difficultybins)
    for cumufreq in allcumcoverages:
        for i in range(len(cumufreq)):
            cumufreqs[i] += cumufreq[i]
    for i in range(len(cumufreqs)):
        cumufreqs[i] /= len(wordforms)
    #cumufreqs = [sum(x[y])/(1.0*len(allcumcoverages)) for x in allcumcoverages for y in range(len(difficultybins)+1)]
    #print cumufreqs
    popt, pcov = curve_fit(func, difficultybins, cumufreqs, p0=[5000]) # start with s = 5000
    return popt, pcov

def calcAB( wordforms, wordform2freqAndrank, maxrank=3000, samplesize=50 ):

    allcumcoverages = []
    for subi in range(len(wordforms)):  #range(len(wordforms) / samplesize): # int division
        first = subi #*samplesize
        last = first + samplesize

        subsample = []
        if last <= len(wordforms):
            subsample = wordforms[first:last]
        else:
            # add words from the beginning
            # this is not the original S, but it means all words count evenly
            subsample = wordforms[first:] + wordforms[:last-len(wordforms)]

        coverages = [0.0]*(maxrank)
        #coverages = [0.0]*(len(difficultybins))
        for wordform in subsample:
            if wordform in wordform2freqAndrank:
                freq, rank = wordform2freqAndrank[wordform]
                if rank <= maxrank:
                    coverages[rank-1] += 1

        # add the previous cumcoverage with the next coverage
        cumulativecoverages = [coverages[0]]
        for cov in coverages[1:]:
            cumulativecoverages.append( cumulativecoverages[-1] + cov)
        for i in range(len(cumulativecoverages)):
            cumulativecoverages[i] = cumulativecoverages[i]*100.0/samplesize
        #print cumulativecoverages
        allcumcoverages.append(cumulativecoverages)

    # so we have a list of lists, need to fit
    func = alternativeSfunction
    # take average (this is cheating)
    cumufreqs = [0.0]*maxrank

    for cumufreq in allcumcoverages:
        for i in range(len(cumufreq)):
            cumufreqs[i] += cumufreq[i]
    for i in range(len(cumufreqs)):
        cumufreqs[i] /= len(wordforms)
    #print "cumufreqs", cumufreqs
    #cumufreqs = [sum(x[y])/(1.0*len(allcumcoverages)) for x in allcumcoverages for y in range(len(difficultybins)+1)]
    #print cumufreqs
    #popt, pcov = curve_fit(func, range(1,maxrank+1), cumufreqs, p0=[5000]) # start with s = 5000
    popt, pcov = curve_fit(func, range(1,maxrank+1), cumufreqs, p0=[25, 0.2]) # start with s = 5000

    return popt, pcov


def loadLemmaCat2freqrank(
        freq_ranks_filename="/home/nparslow/Documents/fouille_de_textes/projet/lund/frmg_normfreq_ranks.json"):
    # read the corpus frequency ranks:
    with open(freq_ranks_filename, 'r') as infile:
        lemmacat2freqrank = json.load(infile)
    return lemmacat2freqrank

    '''
    # calculate the normalised corpus ranks list (we should stock this really, it's inefficient recalculating it)
    # NB be careful as corpusranks is an array so starts from 0
    maxrank = len(lemmacat2freqrank)
    corpusranks = np.zeros(maxrank)
    ranks = np.linspace(1,maxrank, num=maxrank)

    for lemma_cat in lemmacat2freqrank:
        freq, rank = lemmacat2freqrank[lemma_cat]
        if rank <= maxrank:
            corpusranks[rank-1] += freq
    '''

# this should be run once separately
def createLemmaCat2freqrank(
        freqs_filename_path = "/home/nparslow/Documents/AutoCorrige/vocabulary/frmg_frequencies/CPL.lemma"):
    # the goal here is to read the .lemma file and calculate/stock the normalised frequency and ranks
    # CPL = large mixed corpus, wiki, est-france etc.

    # todo this is all a bit hard-wired
    # note that the lemma can include spaces, e.g. 'V. L'Homme:_Uv_np'
    lexique = {}
    with codecs.open(freqs_filename_path, 'r', encoding="latin-1") as f:
        # assumes no header in file
        rank = 1
        for line in f:
            lemma_cat, freq = line.strip().split("\t")
            # don't actually need to split here: need something more complicated too,
            # punctuation is e.g. ':__' i.e. punct + two underscores or can be e.g. '._poncts'
            # and sometimes things like 'Bourgogne:_LOCATION_np'
            #lemma, cat = lemma_cat.rsplit("_",1)

            if lemma_cat in lexique:
                print "double entry", lemma_cat, line.rstrip()
                # can come in here due to a space before the lemma e.g. ' parce:_LOCATION_np'
                # we ignore these as they may change the rank for everything and so require reranking
            else:
                # stock both frequency and rank (we assume list is already ordered)
                lexique[lemma_cat] = (int(freq), rank)
            rank += 1

    totalwords = 1.0*sum([x[1] for x in lexique.values()]) # 1.0 to get float division later
    # output to json with normalised frequency
    for lemma_cat, (freq, rank) in lexique.items():
        lexique[lemma_cat] = (freq/totalwords, rank)

    outfilename = "/home/nparslow/Documents/fouille_de_textes/projet/lund/frmg_normfreq_ranks.json"
    with open(outfilename, 'w') as outfile:
        json.dump(lexique, outfile)


def calcLFP( wordforms, wordform2freqAndrank, difficultybins = (1000,2000,3000)):
    #print "calcLFP"
    rankhistogram = [0]*(len(difficultybins) + 2) # +1 for the 3000+ and + 1 for unknown
    for wordform in wordforms:
        binnum = -1 # default = unknown
        if wordform in wordform2freqAndrank:
            freq, rank = wordform2freqAndrank[wordform]
            if rank > difficultybins[-1]:
                binnum = -2
            else:
                for bini in range(len(difficultybins)):
                    binnum = bini
                    if rank < difficultybins[bini]:
                        break
        rankhistogram[binnum] += 1

        if wordform in wordform2freqAndrank:
            #print wordform, binnum, wordform2freqAndrank[wordform]
            pass
        else:
            #print wordform, binnum
            pass
    # normalise the scores to fractions of 1: (as this applies to the whole text)
    for i in range(len(rankhistogram)):
        rankhistogram[i] *= 1.0/len(wordforms)
    return rankhistogram[0:-2], rankhistogram[-2], rankhistogram[-1]


# todo WARNING: this will not work with accents and underscores needs review !!!!
def getVOCD( token_list ):
    assert False
    assert len(token_list) > 50
    # swap unusual chars in the token list:
    token_list = [re.sub(ur'[\'\s\-\"]', u"_", x, flags=re.UNICODE) for x in token_list]
    # it seems the underscore doesn't work as expected
    token_list = [re.sub(ur'(_|[^\w\s])', 'aa', x, flags=re.UNICODE) for x in token_list]

    result = subprocess.check_output(
            ["/home/nparslow/Documents/AutoCorrige/vocabulary/perl/getVOCD.pl", '"'+" ".join(token_list)+'"'])
    return float(result)

# todo WARNING: this will not work with accents and underscores needs review !!!!
def getMTLD( token_list ):
    assert False
    # swap unusual chars in the token list:
    token_list = [re.sub(ur'[\'\s\-\"]', u"_", x, flags=re.UNICODE) for x in token_list]
    token_list = [re.sub(ur'(_|[^\w\s])', 'aa', x, flags=re.UNICODE) for x in token_list]
    #print token_list
    result = subprocess.check_output(
            ["/home/nparslow/Documents/AutoCorrige/vocabulary/perl/getMTLD.pl", '"'+" ".join(token_list)+'"'])
    return float(result)

def calcTTR( token_list ):
    return 1.0*len(set(token_list))/len(token_list)

def calcVOCD( token_list ):
    min_n = 35
    assert len(token_list) >= min_n
    max_n = min(len(token_list),50)
    xs = np.linspace(min_n, max_n , max_n-min_n + 1) # need to check
    #print xs
    samples = 100
    Ds = []
    print "TTR from first few words", calcTTR(token_list[:35]), calcTTR(token_list[:50])
    for i in range(3): # to the fit 3 times
        ys = []
        sds = []
        for npos in range(len(xs)): # for each N (no. of tokens)
            n = int(xs[npos])
            TTRs = []
            for j in range(samples): # average over 100 times
                # get a random sample of n tokens:
                sample = random.sample(token_list, n )
                #print "sample", sample
                # calculate TTR for this n:
                #print "sample check", len(sample), len(set(sample)), set(sample)
                TTRs.append(calcTTR(sample))
            #print "TTRs", TTRs
            mean = np.mean(TTRs,0)
            sd = np.std(TTRs,0)
            #print "mean TTR, ", n, mean, sd

            ys.append(mean)
            sds.append(sd)



        # fit for D :
        #print "ys", ys
        #  using standard error of mean as errors:
        sds = np.array(sds)/math.sqrt(samples)
        #popt, pcov = curve_fit(TTRfunction, xs, ys, sigma=sds, p0=[100]) # set initial value at 100
        popt, pcov = curve_fit(TTRfunction, xs, ys, p0=[50]) # set initial value at 100

        #plotVOCDFit("vocd", ys, TTRfunction, popt )
        Ds.append(popt[0])

        #print " unfitted Ds: "
        unfittedDs = DfromTTRN(np.array(ys), xs)
        #print np.mean(unfittedDs), unfittedDs
    # todo should we weight by (inverse of) fit error?
    #print "Ds", Ds
    return np.mean(Ds)

def calcMTLDwithDirection(tokens, cutpoint = 0.72):
    factorcount = 0
    factorlengths = []
    currenttoks = []
    ntoks = 0
    for tok in tokens:
        ntoks += 1 # needed as tokens may be an iterator
        currenttoks.append(tok)
        if calcTTR(currenttoks) < cutpoint:
            factorlengths.append(len(currenttoks))
            factorcount += 1
            currenttoks = []
    # get the residual (fraction of the way to the cutpoint):
    if len(currenttoks) > 0:
        residual_ttr = (1.0 - calcTTR(currenttoks))/(1.0-cutpoint)
        if residual_ttr > 0.0:
            factorcount += residual_ttr
        else:
            # the ttr didn't drop below 1.0 so we have no idea of the factor except that it's longer
            # than the no. of tokens remaining.
            # so we subtract the no. of tokens remaining from the ntok count
            ntoks -= len(currenttoks)

        #print "resi", residual_ttr
        #if residual_ttr > 0.0:
        #    factorlengths.append( len(currenttoks)/residual_ttr )
        #else:
        #    factorlengths.append( 0 )

    #print "average:", np.mean(factorlengths)
    return 1.0*ntoks/factorcount, factorcount

# gives the same scores as for the 'within_only' option of Lingua::MTLD
# the 'within_and_between' mode weights the forward and reverse by the no. of observations
# (so partially obs will count less?)
def calcMTLD(tokens, cutpoint=0.72, weight_by_count=False):
    forward, fcount = calcMTLDwithDirection(tokens, cutpoint)
    backward, bcount = calcMTLDwithDirection(reversed(tokens), cutpoint)
    if weight_by_count:
        return 1.0*(forward*fcount+backward*bcount)/(fcount+bcount)
    else:
        return  (forward+backward)/2.0


def plotVOCDFit(title, dist, func, params):

    plt.figure(figsize=(8,7))
    plt.title(title, fontsize=32)
    plt.xlabel("no. tokens", fontsize=24)
    plt.ylabel("TTR", fontsize=24)
    plt.tick_params(axis='both', which = 'major', labelsize=18) # major axis markings
    plt.tick_params(axis='both', which = 'minor', labelsize=12)  # minor axis markings
    plt.xlim((35.0,50.0))

    width = 1.0
    #plt.bar(xhist, dist, width=width)
    xhist = np.linspace(35,50,num=len(dist))
    plt.plot(xhist, dist, 'b+', ms=8.0, mew=1.0) # ms = marker size, mew = marker width
    #frame = plt.gca()
    #frame.axes.get_xaxis().set_visible(False)
    #title = re.sub(ur'\s', '_', title, flags=re.UNICODE)
    #title = re.sub(ur'[\(\),\$\\>=\.]', '', title, flags=re.UNICODE)
    #print title

    # add a line showing the expected distribution
    x = np.arange(35.0, 50.0, 0.1)
    plt.plot(x, func(x, *params), 'r--', linewidth=4.0)

    #fitsos = sum( np.power(func(xhist, *params)-dist,2) )
    #perlsos = sum( np.power(func(xhist, 68.10)-dist,2) )
    #print "fit sum of squares", fitsos, fitsos < perlsos
    #print "perl sum of squares", perlsos

    plt.plot(x, func(x, 68.10), 'r--', linewidth=4.0, color='green')

    #l = P.plot(bins, y, 'k--', linewidth=1.5)

    #plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/makePLexSplots/cumfreqdistS_" + title + ".png")
    #plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/makePLexSplots/cumfreqdistUnbinnedAndrea_" + title + ".png")
    plt.show()
    #exit(10)

def main():

    # only needs to be run once:
    #createLemmaCat2freqrank()

    # check the vocd calculation:
    # from McKee, Malvern & Richards 2000
    utterances = ["where are the toy",
                  "yeah",
                  "yeah",
                  "book",
                  "book",
                  "book",
                  "book",
                  "book",
                  "two",
                  "where the two booko@",
                  "I want two booko@",
                  "okay",
                  "baby",
                  "bug",
                  "duck",
                  "there",
                  "yeah",
                  "what",
                  "what",
                  "yeah",
                  "comb",
                  "comb",
                  "that",
                  "comb",
                  "brush",
                  "brush",
                  "soap",
                  "yeah",
                  "purple",
                  "that yellow",
                  "no purple",
                  "purple",
                  "milk there",
                  "no",
                  "yeah",
                  "me",
                  "yeah",
                  "yeah",
                  "there",
                  "purple",
                  "yeah",
                  "get more book",
                  "puppet show",
                  "puppet",
                  "puppet",
                  "mommy",
                  "no more cookie",
                  "no",
                  "hello",
                  "hello",
                  "yeah",
                  "hello",
                  "no",
                  "yeah",
                  "yeah",
                  "that box",
                  "yeah",
                  "mommy color",
                  "mommy color too",
                  "three color",
                  "here mommy",
                  "purple",
                  "that purple",
                  "yeah",
                  "here mommy",
                  "help me",
                  "help",
                  "help",
                  "help me",
                  "yeah",
                  "eye",
                  "the nose",
                  "all done",
                  "house",
                  "house",
                  "the house",
                  "me",
                  "down",
                  "go down",
                  "out",
                  "there",
                  "car",
                  "car",
                  "car",
                  "car",
                  "nope",
                  "want to put it away mommy",
                  "I want it away",
                  "yeah",
                  "no"
                  ]
    tokens = [token for utterance in utterances for token in utterance.split()]
    print "toks", len(tokens) #tokens # 129 tokens
    print "types", len(set(tokens))
    print "ttr", calcTTR(tokens)
    #print "vocd", calcVOCD(tokens)
    #print "perl vocd", getVOCD(tokens)

    print
    print "mtld"
    print "perl", getMTLD(tokens)
    print "pyth", calcMTLD(tokens, 0.72)
    #print "pyth w", calcMTLD(tokens, 0.72, weight_by_count=True)

    tokens = [u'_PERSON_np', u'\xeatre_v', u'le_det', u'fille_nc', u'de_prep', u'Patricia_np', u',__', u'ensemble_adv', u'cln_cln', u'avoir_aux', u'd\xe9cider_v', u'de_prep', u'partir_v', u'en_prep', u'Italie_np', u',__', u'mais_coo', u'pour_prep', u'un_det', u'raison_nc', u'divers_adj', u'.__', u'_PERSON_np', u'esp\xe9rer_v', u'cll_cll', u'trouver_v', u'le_det', u'homme_nc', u'de_prep', u'son_det', u'vie_nc', u'alors que_csu', u'alors que_csu', u'Patricia_np', u'esp\xe9rer_v', u'surtout_adv', u'clr_clr', u'reposer_v', u'sous_prep', u'le_det', u'soleil_nc', u'chaud_adj', u'de_prep', u'Italie_np', u'.__', u'son_det', u'petit_adj', u'voiture_nc', u'pouvoir_v', u'\xe0 peine_adv', u'\xe0 peine_adv', u'contenir_v', u'son_det', u'_NUMBER_nc', u'valise_nc', u'mais_coo', u'que_csu', u'importer_v', u',__', u'rien_pro', u'ne_clneg', u'pouvoir_v', u'g\xe2cher_v', u'son_det', u'plaisir_nc', u'.__', u'le_det', u'route_nc', u'\xeatre_v', u'long_adj', u'entre_prep', u'le_det', u'Su\xe8de_np', u'et_coo', u'le_det', u'Italie_np', u',__', u'et_coo', u'une fois_prep', u'une fois_prep', u'arriv\xe9_nc', u',__', u'son_det', u'_NUMBER_adj', u'touriste_nc', u'devoir_v', u'trouver_v', u'un_det', u'h\xf4tel_nc', u'au bord de_prep', u'au bord de_prep', u'au bord de_prep', u'le_det', u'mer_nc', u'.__', u'ensuite_adv', u'ce_cln', u'\xeatre_v', u'le_det', u'inn\xe9vitable_adj', u'sc\xe9ance_nc', u'de_prep', u'bronzage_nc', u'afin de_prep', u'afin de_prep', u'\xeatre_v', u'beau_adj', u'pour_prep', u'aller_v', u'manger_v', u'le_det', u'soir_nc', u'dans_prep', u'un_det', u'restaurant_nc', u'Uw_np', u'.__', u'ce_cln', u'\xeatre_aux', u'dans_prep', u'un_det', u'bar_nc', u',__', u'apr\xe8s_prep', u'le_det', u'repas_nc', u',__', u'que_prel', u'Marie_np', u'avoir_aux', u'rencontrer_v', u'Paolo_np', u'et_coo', u'Patricia_np', u'avoir_aux', u'faire_v', u'le_det', u'connaissance_nc', u'de_prep', u'Mario_np', u'.__', u'ainsi_adv', u'le_det', u'f\xeate_nc', u'pouvoir_v', u'continuer_v', u"jusqu'\xe0_prep", u'le_det', u'petit_adj', u'matin_nc', u'.__', u'ensemble_adv', u',__', u'cln_cln', u'avoir_aux', u'visiter_v', u'le_det', u'ville_nc', u'de_prep', u'Rome_np', u'.__', u'Paolo_np', u'et_coo', u'Mario_np', u'\xeatre_v', u'de_prep', u'vrai_adj', u'italien_nc', u',__', u'cln_cln', u'savoir_v', u'flatter_v', u'le_det', u'femme_nc', u'et_coo', u'\xeatre_v', u'un_det', u'beau_adj', u'parleur_nc', u',__', u'mais_coo', u'que_csu', u'importer_v', u',__', u'_PERSON_np', u'tomber_v', u'amoureux_nc', u'de_prep', u'Paolo_np', u'pendant_prep', u'un_det', u'sc\xe9ance_nc', u'de_prep', u'shopping_nc', u'.__', u'quand?_pri', u'tome_nc', u'\xe0_prep', u'Mario_np', u',__', u'plus_adv', u'romantique_adj', u',__', u'ce_cln', u'\xeatre_v', u'devant_prep', u'un_det', u'couch\xe9_adj', u'de_prep', u'soleil_nc', u'que_que', u'cln_cln', u'd\xe9voiler_v', u'son_det', u'flamme_nc', u'\xe0_prep', u'Patricia_np', u'qui_prel', u'aussit\xf4t_adv', u'tomber_v', u'sous_prep', u'le_det', u'charme_nc', u'.__', u'malheureusement_adv', u',__', u'voici_v', u'le_det', u'heure_nc', u'de_prep', u'le_det', u'adieu_nc', u'mais_coo', u'Paolo_np', u'et_coo', u'Mario_np', u'vouloir_v', u'suivre_v', u'son_det', u'_NUMBER_adj', u'compagne_nc', u'en_prep', u'su\xe8de_nc', u',__', u'et_coo', u'ainsi_adv', u',__', u'le_det', u'valise_nc', u'sur_prep', u'le_det', u'toit_nc', u'de_prep', u'le_det', u'petit_adj', u'voiture_nc', u',__', u'Patricia_np', u'et_coo', u'Marie_np', u'rentrer_v', u'en_prep', u'su\xe8de_nc', u'avec_prep', u'ce_ce', u'que_prel', u'lui_pro', u'\xeatre_aux', u'venir_v', u'chercher_v', u'.__']
    #tokens = [u'_PERSON_np', u'etre_v', u'le_det', u'fille_nc', u'de_prep', u'Patricia_np', u',__', u'ensemble_adv', u'cln_cln', u'avoir_aux', u'decider_v', u'de_prep', u'partir_v', u'en_prep', u'Italie_np', u',__', u'mais_coo', u'pour_prep', u'un_det', u'raison_nc', u'divers_adj', u'.__', u'_PERSON_np', u'esperer_v', u'cll_cll', u'trouver_v', u'le_det', u'homme_nc', u'de_prep', u'son_det', u'vie_nc', u'alors que_csu', u'alors que_csu', u'Patricia_np', u'esperer_v', u'surtout_adv', u'clr_clr', u'reposer_v', u'sous_prep', u'le_det', u'soleil_nc', u'chaud_adj', u'de_prep', u'Italie_np', u'.__', u'son_det', u'petit_adj', u'voiture_nc', u'pouvoir_v', u'a peine_adv', u'a peine_adv', u'contenir_v', u'son_det', u'_NUMBER_nc', u'valise_nc', u'mais_coo', u'que_csu', u'importer_v', u',__', u'rien_pro', u'ne_clneg', u'pouvoir_v', u'gacher_v', u'son_det', u'plaisir_nc', u'.__', u'le_det', u'route_nc', u'etre_v', u'long_adj', u'entre_prep', u'le_det', u'Suede_np', u'et_coo', u'le_det', u'Italie_np', u',__', u'et_coo', u'une fois_prep', u'une fois_prep', u'arrive_nc', u',__', u'son_det', u'_NUMBER_adj', u'touriste_nc', u'devoir_v', u'trouver_v', u'un_det', u'hotel_nc', u'au bord de_prep', u'au bord de_prep', u'au bord de_prep', u'le_det', u'mer_nc', u'.__', u'ensuite_adv', u'ce_cln', u'etre_v', u'le_det', u'innevitable_adj', u'sceance_nc', u'de_prep', u'bronzage_nc', u'afin de_prep', u'afin de_prep', u'etre_v', u'beau_adj', u'pour_prep', u'aller_v', u'manger_v', u'le_det', u'soir_nc', u'dans_prep', u'un_det', u'restaurant_nc', u'Uw_np']
    #tokens = [re.sub(ur'[_\W]', 'AA', x, flags=re.UNICODE).lower() for x in tokens if re.match(ur'\w', x, flags=re.UNICODE)] # checking shows prob is not punctuation, nor upper case letters.
    #tokens = [re.sub(ur'(_|[^\w\s])', 'aa', x, flags=re.UNICODE) for x in tokens]
    # to get agreement with perl, need the following four lines:
    # 1) remove any non-ascii, 2) remove any pure punctuation
    from unidecode import unidecode
    tokens = [unidecode(x) for x in tokens]
    #tokens = [re.sub(ur'_', 'AA', x, flags=re.UNICODE) for x in tokens]
    #tokens = [re.sub(ur'\s', 'BB', x, flags=re.UNICODE) for x in tokens]
    tokens = [x for x in tokens if not re.match(ur'[^\w]', x, flags=re.UNICODE)]
    #print unidecode(u"\u5317\u4EB0")
    #print unidecode(u'\xeatreaav')
    print "toks", len(tokens), tokens
    print "types", len(set(tokens))
    print "ttr", calcTTR(tokens)
    print "vocd", calcVOCD(tokens)
    print "perl vocd", getVOCD(tokens)
    print "mtld", calcMTLD(tokens)
    print "perl mtld", getMTLD(tokens)
    # difference of about 5 with sub, about 4 with sub + lower

    print ""
    text = u"The girl was stolen a bread, but Chaplin take a fault. So, they are going to put a Chaplin in jail. But a woman saw that the girl stolen the bread, so they take Chaplin and the girl. When they was going to jail the girl and Chaplin ran away. They go to sit and talk about where they live. The girl say that she live no where. So they dreaming a home where they can take orange in the tree and eat a breakfast in a kitchen. The Chaplin say that do the work then we got a house."
    # with the sub (and with lower too, though it's not neccessary), works very well vocd: 33.59 v 33.76
    #tokens = re.sub(ur'(_|[^\w\s])', '', text, flags=re.UNICODE).split()
    tokens = text.split()



    #tokens = text.split()
    print "toks", len(tokens) #
    print "types", len(set(tokens))
    print "ttr", calcTTR(tokens)
    #print "vocd", calcVOCD(tokens)
    #print "perl vocd", getVOCD(tokens)
    #print "mtld", calcMTLD(tokens) # these two agree
    #print "perl mtld", getMTLD(tokens)
    #for i in range(1,len(tokens)):
    #    print i, calcTTR(tokens[:i])




if __name__ == "__main__":
    main()