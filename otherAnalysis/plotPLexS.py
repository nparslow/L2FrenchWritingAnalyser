import glob

__author__ = 'nparslow'

import calcPLex
#import readDdag
import numpy as np
from scipy.optimize import curve_fit
from scipy.misc import factorial
import matplotlib.pyplot as plt
import re
import compareCorrectedCorpus


def alternativeSfunction(x, a, b):

    return a*np.power(x, b)  # note using math.log will crash, np.log is the natural log by default




def poissonMass( k, lamb):
    return (lamb**k/factorial(k)) * np.exp(-lamb)

def poissonCount( N ):
    return lambda k, lamb: N * poissonMass(k, lamb)


def plotProbDistribution(title, dist, func, params):
    #fig = plt.subplot(111)
    #width = 0.8
    #fig.set_yscale('log')
    #plt.yscale('log')

    plt.figure(figsize=(8,7))
    plt.title(title, fontsize=32)
    plt.xlabel("mots difficiles par 10 tokens", fontsize=24)
    #plt.ylabel("frequency (log scale)", fontsize=24)
    plt.tick_params(axis='both', which = 'major', labelsize=18) # major axis markings
    plt.tick_params(axis='both', which = 'minor', labelsize=12)  # minor axis markings
    plt.xlim((-0.5,10.5))
    print "dist", dist
    xhist = np.linspace(-0.5,10.5,num=11) # i.e. 11 samples
    plt.bar(xhist, dist)
    #plt.semilogy()
    #plt.yscale('log', nonposy='clip') # needed as log -> 0 causes problems for filling
    width = 1.0
    #fig.set_xticks(np.arange(len(keys)) + width/2)
    #fig.set_xticklabels(range(len(keys)), rotation=45)
    #plt.ylim((0,1000))


    #frame = plt.gca()
    #frame.axes.get_xaxis().set_visible(False)
    title = re.sub(ur'\s', '_', title, flags=re.UNICODE)
    title = re.sub(ur'[\(\),\$\\>=\.]', '', title, flags=re.UNICODE)
    print title

    # add a line showing the expected distribution
    x = np.arange(0.0, 10.0, 0.1)
    plt.plot(x, func(x, params), 'r--', linewidth=4.0)

    #l = P.plot(bins, y, 'k--', linewidth=1.5)

    plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/makePLexSplots/plexdist_" + title + ".png")
    plt.show()
    #exit(10)


def plotPLex( wordforms, wordform2freqrank, difficultRank = 500):

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
            if rank > difficultRank:
                counter += 1
        # common words and words not in the lexique are ignored

    xhist = np.linspace(0,10,num=11) # i.e. 11 samples
    yhist = np.array(distribution, dtype=float)

    #nHard = sum([i*distribution[i]] for i in range(len(distribution))])
    #npoisson = lambda x,y : poissonW(wordlength, x, y)
    #print "distribution:"
    #print distribution
    print yhist
    #npoisson = lambda x,y : poissonMass(x, y)
    npoisson = poissonCount(sum(yhist))
    popt, pcov = curve_fit(npoisson, xhist, yhist, p0=[1.5]) # start with lambda = 1.5


    plotProbDistribution("P_Lex fit " + "$\lambda=" + str(round(popt[0],2)) + "$", dist=yhist, func = npoisson, params = popt)

    #print popt, pcov
    return popt, pcov


#filename = "/home/nparslow/Documents/AutoCorrige/Corpora/makePLexSplots/Calle_sxpipe_tokenised.txt"
#tokens = readDdag.readDdag(filename, keepSentences=False)

all_lemmcats = []

#globstring = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_CEFLE/Calle/0/0/0/Calle.E*.dep.xml"
globstring = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_CEFLE/Emanuel/0/0/0/Emanuel.E*.dep.xml"
globstring = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_CEFLE/Elias/0/0/0/Elias.E*.dep.xml"
globstring = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_ECRIT_VALETOPOULOS/chyFLE_2011_TI_UCY_4_Autoobservation_Susanna_Georgiou/0/0/0/chyFLE_2011_TI_UCY_4_Autoobservation_Susanna_Georgiou.E*.dep.xml"
globstring = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_CEFLE/Andrea/0/0/0/Andrea.E*.dep.xml"
globstring = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_CEFLE/Annette/0/0/0/Annette.E*.dep.xml"

for xmlfilename in glob.glob(globstring):

    finaltokens, origlemmacats, origverb2info, origtrees, origweight, wordsbeforemainverb =\
                compareCorrectedCorpus.getFinalTokenFormsAndTreesAndWeight(xmlfilename)

    for tokennum in origlemmacats:
        all_lemmcats.extend( x[0] + "_" + x[1] for x in origlemmacats[tokennum])
print all_lemmcats

lemmacat2freq = calcPLex.loadLemmaCat2freqrank()

#plex, plexerr = plotPLex(all_lemmcats, lemmacat2freq)

# x can be an array
def Sfunction(x, s):
    # need to convert x to a float?
    #print x
    if s > 0:
        #print s
        #print x
        return np.log(x)/np.log(s) * 100.0 # note using math.log will crash, np.log is the natural log by default
    else:
        return 0.0*x


def plotCumFreqDist(title, dist, func, params):
    #fig = plt.subplot(111)
    #width = 0.8
    #fig.set_yscale('log')
    #plt.yscale('log')

    plt.figure(figsize=(8,7))
    plt.title(title, fontsize=32)
    plt.xlabel("frequency rank", fontsize=24)
    plt.ylabel("cumulative text coverage", fontsize=24)
    plt.tick_params(axis='both', which = 'major', labelsize=18) # major axis markings
    plt.tick_params(axis='both', which = 'minor', labelsize=12)  # minor axis markings
    plt.xlim((0.01,3250))
    print "cum freq dist", dist


    width = 500.0
    xhist = np.linspace(00,2500,num=6) # i.e. 6 bins in cum freq dist
    #plt.bar(xhist, dist, width=width)
    xhist = np.linspace(500,3000,num=6)
    plt.plot(xhist, dist, 'b+', ms=10.0, mew=3.0) # ms = marker size, mew = marker width
    #print "hist", xhist
    #plt.semilogy()
    #plt.yscale('log', nonposy='clip') # needed as log -> 0 causes problems for filling

    #fig.set_xticks(np.arange(len(keys)) + width/2)
    #fig.set_xticklabels(range(len(keys)), rotation=45)
    #plt.ylim((0,1000))


    #frame = plt.gca()
    #frame.axes.get_xaxis().set_visible(False)
    title = re.sub(ur'\s', '_', title, flags=re.UNICODE)
    title = re.sub(ur'[\(\),\$\\>=\.]', '', title, flags=re.UNICODE)
    print title

    # add a line showing the expected distribution
    x = np.arange(0.0, 3250.0, 1)
    plt.plot(x, func(x, params), 'r--', linewidth=4.0)

    #l = P.plot(bins, y, 'k--', linewidth=1.5)

    #plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/makePLexSplots/cumfreqdistS_" + title + ".png")
    #plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/makePLexSplots/cumfreqdistbadSforAndrea_" + title + ".png")
    plt.show()
    #exit(10)


def plotCumFreqDistUnbinned(title, dist, func, params):
    #fig = plt.subplot(111)
    #width = 0.8
    #fig.set_yscale('log')
    #plt.yscale('log')

    plt.figure(figsize=(8,7))
    plt.title(title, fontsize=32)
    plt.xlabel("frequency rank", fontsize=24)
    plt.ylabel("cumulative text coverage", fontsize=24)
    plt.tick_params(axis='both', which = 'major', labelsize=18) # major axis markings
    plt.tick_params(axis='both', which = 'minor', labelsize=12)  # minor axis markings
    plt.xlim((0.00,3000))
    print "cum freq dist", dist


    width = 500.0
    xhist = np.linspace(1,len(dist)+1,num=len(dist)) # i.e. 6 bins in cum freq dist
    #plt.bar(xhist, dist, width=width)
    xhist = np.linspace(1,len(dist)+1,num=len(dist))
    plt.plot(xhist, dist, 'b+', ms=8.0, mew=1.0) # ms = marker size, mew = marker width
    #print "hist", xhist
    #plt.semilogy()
    #plt.yscale('log', nonposy='clip') # needed as log -> 0 causes problems for filling

    #fig.set_xticks(np.arange(len(keys)) + width/2)
    #fig.set_xticklabels(range(len(keys)), rotation=45)
    #plt.ylim((0,1000))


    #frame = plt.gca()
    #frame.axes.get_xaxis().set_visible(False)
    title = re.sub(ur'\s', '_', title, flags=re.UNICODE)
    title = re.sub(ur'[\(\),\$\\>=\.]', '', title, flags=re.UNICODE)
    print title

    # add a line showing the expected distribution
    x = np.arange(0.0, 3250.0, 1)
    plt.plot(x, func(x, *params), 'r--', linewidth=4.0)

    #l = P.plot(bins, y, 'k--', linewidth=1.5)

    #plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/makePLexSplots/cumfreqdistS_" + title + ".png")
    #plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/makePLexSplots/cumfreqdistUnbinnedAndrea_" + title + ".png")
    plt.show()
    #exit(10)

def plotS( wordforms, wordform2freqAndrank, difficultybins = (500,1000,1500,2000,2500,3000), samplesize=50):
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
    print "cumufreqs", cumufreqs
    #cumufreqs = [sum(x[y])/(1.0*len(allcumcoverages)) for x in allcumcoverages for y in range(len(difficultybins)+1)]
    #print cumufreqs
    popt, pcov = curve_fit(func, difficultybins, cumufreqs, p0=[5000]) # start with s = 5000

    plotCumFreqDist("a="+str(round(popt[0],0))+" b="+str(round(popt[1],2)), cumufreqs, func, popt)

    return popt, pcov


def plotSunbinned( wordforms, wordform2freqAndrank, maxrank=3000, samplesize=50):
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

        coverages = [0.0]*(maxrank)
        #coverages = [0.0]*(len(difficultybins))
        for wordform in subsample:
        #for wordform in set(subsample):
        #  repetition is not really the problem, as its with sample size 50
        # rather seems to be a need for better rankings.
            if wordform in wordform2freqAndrank:
                freq, rank = wordform2freqAndrank[wordform]

                print wordform, freq, rank
                if rank <= maxrank:
                    coverages[rank-1] += 1
            else:
                print "not in dict", wordform

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
    print "cumufreqs", cumufreqs
    #cumufreqs = [sum(x[y])/(1.0*len(allcumcoverages)) for x in allcumcoverages for y in range(len(difficultybins)+1)]
    #print cumufreqs
    #popt, pcov = curve_fit(func, range(1,maxrank+1), cumufreqs, p0=[5000]) # start with s = 5000
    popt, pcov = curve_fit(func, range(1,maxrank+1), cumufreqs, p0=[25, 0.2]) # start with s = 5000

    plotCumFreqDistUnbinned("S="+str(round(popt[0],0)), cumufreqs, func, popt)

    return popt, pcov














#s, serr = plotS(all_lemmcats, lemmacat2freq )
s, serr = plotSunbinned(all_lemmcats, lemmacat2freq )
print "fit params", s, "fit cov", serr