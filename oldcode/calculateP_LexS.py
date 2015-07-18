__author__ = 'nparslow'

import json
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
import xml.etree.cElementTree as ET
from scipy.misc import factorial

# read the corpus frequency ranks:
lemmacat2freqrank = {}
with open("/home/nparslow/Documents/fouille_de_textes/projet/lund/frmg_freq_ranks.json", 'r') as infile:
    lemmacat2freqrank = json.load(infile)

# calculate the normalised corpus ranks list (we should stock this really, it's inefficient recalculating it)
# NB be careful as corpusranks is an array so starts from 0
maxrank = len(lemmacat2freqrank)
corpusranks = np.zeros(maxrank)
ranks = np.linspace(1,maxrank, num=maxrank)


for lemma_cat in lemmacat2freqrank:
    freq, rank = lemmacat2freqrank[lemma_cat]
    if rank <= maxrank:
        corpusranks[rank-1] += freq

cranks = corpusranks/np.sum(corpusranks)
'''
# this section is to look at the frequency distribution from the corpus if you want to
plt.figure()
plt.loglog()
plt.plot(ranks, cranks, 'kx', label="corpus")
plt.legend()
plt.show()
'''

# this function is for S and P_Lex calculations where we have to group multiple files in the directory
# before analysis
def analyseStudentGroupedFiles( student2filegroup, lemma_cat2frequencyANDrank, results, analysis_function ):

    for student in student2filegroup:
        #print student
        result = analysis_function(student2filegroup[student], lemma_cat2frequencyANDrank)
        if result is not None:
            results[student] = result
        #print student, results[student]
        #break

def getStudentFileLists( inpath, student2filelist):
    for element in os.listdir(inpath):
        full_element = inpath + "/" + element
        if os.path.isfile(full_element):
            student = re.search(r"(?<=FRMG)\w+(?=Sentence\d+\.xml)", element).group(0)
            if student not in student2filelist: student2filelist[student] = []
            student2filelist[student].append(full_element)
        else:
            # it's a directory:
            getStudentFileLists(full_element, student2filelist)

def Sfunction(x, s):
    # need to convert x to a float?
    #print x
    if s > 0 :
        #print s
        #print x
        return np.log(x)/np.log(s) * 100.0 # note using math.log will crash, np.log is the natural log by default
    else:
        return 0.0*x

def SfunctionAlt(x, s, b):
    # need to convert x to a float?
    #print x
    if s > 0 :
        #print s
        #print x
        return 100*(1.0-s*np.power(x,b))# note using math.log will crash, np.log is the natural log by default
    else:
        return 0.0*x

def SfunctionAltLogist(x, b, x0, k):
    # need to convert x to a float?
    #print x
    #if s > 0 :
        #print s
        #print x
    return 100*(1.0-np.power(x, b)*(1/(1+np.exp(-k*(x-x0)))))
    # note using math.log will crash, np.log is the natural log by default
    #else:
    #    return 0.0*x

def SfunctionAltLogist2(x, b, x0, k):
    # need to convert x to a float?
    #print x
    #if s > 0 :
        #print s
        #print x
    return 100*(1.0-np.log(1+np.power(x, b))*(1/(1+np.exp(-k*(x-x0)))))
    # note using math.log will crash, np.log is the natural log by default
    #else:
    #    return 0.0*x

def logistic(x, x0, k):
    return 1.0/(1.0+np.exp(-k*(x-x0)))


def getS( filenames, lemma_cat2frequencyANDrank ):
    # filenames = list of filenames to be processed as one text
    # lemma_cat2frequencyANDrank is a dictionary with keys = 'lemma'+ '_' + 'cat', with values = 2-tuple : freq, rank

    # loop over files and get frequency distribution of words in text
    # i.e. a dictionary : lemma_cat to percentage_of_text, rank of lemma in general corpus
    lemma_cat2intextfreqSfunctionAltLogistuency = {}
    for filename in filenames:
        tree = ET.parse(filename)

        for node in tree.findall('node'):
            #treeInfo = node.get("tree")
            lemma = node.get("lemma")
            cat = node.get("cat")
            lemma_cat = lemma + "_" + cat

            #corpfreq, corprank = (0, -1)
            #if lemma_cat in lemma_cat2frequencyANDrank:
            #    corpfreq, corprank = lemma_cat2frequencyANDrank[lemma_cat]

            if lemma_cat not in lemma_cat2intextfrequency:
                lemma_cat2intextfrequency[lemma_cat] = 0
            lemma_cat2intextfrequency[lemma_cat] += 1

    # loop over the frequency distribution in rank order to construct the cumulative percentage
    ranks = [] # note we should really have points for ranks with no change too * todo ??
    cumufreqs = []
    maxrank = 100000000
    for lemma_cat, intextfreq in sorted(lemma_cat2intextfrequency.iteritems(),
            key=lambda x: lemma_cat2frequencyANDrank[x[0]][1] if x[0] in lemma_cat2frequencyANDrank else maxrank ):
        rank = maxrank
        # only add a point if a rank is defined:
        if lemma_cat in lemma_cat2frequencyANDrank:
            rank = lemma_cat2frequencyANDrank[lemma_cat][1]

            # cumulative frequency = this freq plus the last cumulative frequency if it exists:
            cumufreq = intextfreq
            if len(cumufreqs) > 0: cumufreq += cumufreqs[-1]
            ranks.append(rank)
            cumufreqs.append(cumufreq)


    # normalise to a fraction of the recognised words: (last entry = total no. of recognised words)
    cumufreqs = [100.0*x/cumufreqs[-1] for x in cumufreqs] # 100 so it's as a percentage (to match paper)

    # fit the distribution (numpy?)

    # only take up to 90%
    cumufreqs = [x for x in cumufreqs if x < 98]
    ranks = ranks[:len(cumufreqs)]

    # introduce all the zero change points (otherwise fit is biased by low values):

    newranks = range(1, ranks[-1]+1)
    newcumufreqs = [0]*ranks[-1]
    current_rank_pos = 0
    current_cumu_freq = 0
    for i in newranks:
        if i == ranks[current_rank_pos+1]:
            current_rank_pos += 1
            current_cumu_freq = cumufreqs[current_rank_pos]
        newcumufreqs[i-1] = current_cumu_freq

    cumufreqs = newcumufreqs
    ranks = newranks


    #python numpy fit data
    ranks = np.array(ranks, dtype=float) # have to convert to np array of floats or will bug
    cumufreqs = np.array(cumufreqs, dtype=float)
    #popt, pcov = curve_fit(Sfunction, ranks, cumufreqs, p0=[5000]) # start with s = 5000

    #func = SfunctionAlt
    #popt, pcov = curve_fit(func, ranks, cumufreqs, p0=[1.5, -0.25]) # start with s = 5000
    func = SfunctionAltLogist
    popt, pcov = curve_fit(func, ranks, cumufreqs, p0=[-0.25, 5000, 0.00001]) # start with s = 5000

    #print popt
    plt.figure()
    plt.plot(ranks, cumufreqs, 'ko', label="data")
    plt.plot(ranks, func(ranks, *popt), 'r-', label="Fitted Curve")
    plt.legend(loc='lower right')
    plt.show()
    print popt
    return popt[0]

def poisson(k, lamb):
    return (lamb**k/factorial(k)) * np.exp(-lamb)

def poissonW(total, k, lamb):
    return total*(lamb**k/factorial(k)) * np.exp(-lamb)

def getP_Lex( filenames, lemma_cat2frequencyANDrank ):
    # filenames = list of filenames to be processed as one text
    # lemma_cat2frequencyANDrank is a dictionary with keys = 'lemma'+ '_' + 'cat', with values = 2-tuple : freq, rank

    # loop over files and get frequency distribution of words in text
    # i.e. a dictionary : lemma_cat to percentage_of_text, rank of lemma in general corpus
    wordcount = 0 # will go from 0 to 9 then reset to 0
    currentcount = 0
    hardwords = [] # one entry for every 10 words, each being an integer - the no. of 'hard' words in each group of 10
    hardrank = 1000 # above this rank, all words are considered 'hard'
    # note technically the sentences should be in same order as text, but it shouldn't make a difference
    # trailing words in the text in a group less than 10 are ignored

    for filename in filenames:
        tree = ET.parse(filename)

        for node in tree.findall('node'):
            #treeInfo = node.get("tree")
            lemma = node.get("lemma")
            cat = node.get("cat")
            lemma_cat = lemma + "_" + cat
            #print lemma_cat

            # only consider words we recognise:  # add lexical only requirement
            if lemma_cat in lemma_cat2frequencyANDrank and cat in ['nc', 'adv', 'adj', 'v']:
                corpfreq, corprank = lemma_cat2frequencyANDrank[lemma_cat]
                if corprank > hardrank:
                    currentcount += 1

                wordcount += 1
                # once we get to 10 words, add the info and reset
                if wordcount == 10:
                    hardwords.append(currentcount)
                    currentcount = 0
                    wordcount = 0


    #python numpy fit data
    counts = [0]*11 # 11 as we can have from 0 to 10 inclusive
    for count in hardwords:
        counts[count] +=1
    wordlength = sum(counts)
    print "wl:", wordlength # 1 to 25 , min is 15 normally, i.e. 150 words

    if wordlength < 15: return None

    x = np.linspace(0,10,num=11) # i.e. 11 samples
    #print x
    y = np.array(counts, dtype=float)

    npoisson = lambda x,y : poissonW(wordlength, x, y)
    popt, pcov = curve_fit(npoisson, x, y, p0=[1.5]) # start with lambda = 1.5

    # to show the fit (mostly terrible, perhaps stats too low)

    plt.figure()
    plt.plot(x, y, 'ko', label="data")
    plt.plot(x, npoisson(x, *popt), 'r-', label="Fitted Curve")
    plt.legend()
    plt.show()
    print popt

    return popt[0]


def getSalt( filenames, lemma_cat2frequencyANDrank ):
    # the problem is that seen / not seen is a function of text length

    # filenames = list of filenames to be processed as one text
    # lemma_cat2frequencyANDrank is a dictionary with keys = 'lemma'+ '_' + 'cat', with values = 2-tuple : freq, rank

    # loop over files and get frequency distribution of words in text
    # i.e. a dictionary : lemma_cat to percentage_of_text, rank of lemma in general corpus
    maxrank = 10000
    #cranks = np.zeros(maxrank)
    tranks = np.zeros(maxrank)
    ranks = np.linspace(1,maxrank, num=maxrank)


    for filename in filenames:
        tree = ET.parse(filename)

        for node in tree.findall('node'):
            #treeInfo = node.get("tree")
            lemma = node.get("lemma")
            cat = node.get("cat")
            lemma_cat = lemma + "_" + cat

            if lemma_cat in lemma_cat2frequencyANDrank:
                freq, rank = lemma_cat2frequencyANDrank[lemma_cat]
                if rank <= maxrank:
                    tranks[rank-1] = 1
                    #cranks[rank-1] += freq

    # probabalise the distribution:
    #cranks = cranks/np.sum(cranks)
    #tranks = tranks/np.sum(tranks)

    func = logistic
    ranks = np.log(ranks)
    popt, pcov = curve_fit(func, ranks, tranks, p0=[2.5, -1]) # start with s = 5000

    print popt
    plt.figure()
    #plt.semilogy()
    #plt.semilogx()
    #plt.loglog()
    plt.plot(ranks, tranks, 'ko', label="data")
    #plt.plot(ranks, cranks, 'kx', label="corpus")
    plt.plot(ranks, func(ranks, *popt), 'r-', label="Fitted Curve")
    plt.legend()
    plt.show()
    #print popt
    #return popt[0]
    return 0

def getSalt2( filenames, lemma_cat2frequencyANDrank ):
    # filenames = list of filenames to be processed as one text
    # lemma_cat2frequencyANDrank is a dictionary with keys = 'lemma'+ '_' + 'cat', with values = 2-tuple : freq, rank

    # loop over files and get frequency distribution of words in text
    # i.e. a dictionary : lemma_cat to percentage_of_text, rank of lemma in general corpus
    lemma_cat2intextfrequency = {}
    for filename in filenames:
        tree = ET.parse(filename)

        for node in tree.findall('node'):
            #treeInfo = node.get("tree")
            lemma = node.get("lemma")
            cat = node.get("cat")
            lemma_cat = lemma + "_" + cat

            if lemma_cat in lemma_cat2frequencyANDrank:
                corpfreq, corprank = lemma_cat2frequencyANDrank[lemma_cat]

                if corprank not in lemma_cat2intextfrequency:
                    lemma_cat2intextfrequency[corprank] = 0
                lemma_cat2intextfrequency[corprank] += 1

    # loop over the frequency distribution in rank order to construct the cumulative percentage
    ranks = lemma_cat2intextfrequency.keys()
    textlength = sum(lemma_cat2intextfrequency.values())
    tranks = [lemma_cat2intextfrequency[x]/(textlength*corpusranks[x-1]) for x in ranks]

    #python numpy fit data
    ranks = np.array(ranks, dtype=float) # have to convert to np array of floats or will bug
    tranks = np.array(tranks, dtype=float)

    #func = SfunctionAltLogist
    #popt, pcov = curve_fit(func, ranks, cumufreqs, p0=[-0.25, 5000, 0.00001]) # start with s = 5000

    #print popt
    plt.figure()
    plt.loglog()
    #plt.semilogx()
    plt.plot(ranks, tranks, 'ko', label="data")
    #plt.plot(ranks, func(ranks, *popt), 'r-', label="Fitted Curve")
    plt.legend()
    plt.show()
    #print popt
    return 0








student2filelist = {}
getStudentFileLists(
    "/home/nparslow/Documents/fouille_de_textes/projet/lund/frmgXml",
    student2filelist
)


results = {}
analyseStudentGroupedFiles(
    student2filelist,
    lemmacat2freqrank,
    results,
    #getS
    #getP_Lex
    getSalt
    #getSalt2
)

print results

level2results = {}
levels = ['A', 'B', 'C', 'D', 'E']
for level in levels:
    level2results[level] = []
for student in results:
    level = student[0] # i.e. first letter
    level2results[level].append(results[student])

plt.boxplot([level2results[x] for x in levels])
plt.show()







