# coding=utf-8
__author__ = 'nparslow'

import codecs
import matplotlib.pyplot as plt
import numpy as np
import re
import matplotlib.mlab as mlab

filename = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/outArff/test.arff"
#data = []
#ys = []
xs = []
attributes = []
with codecs.open(filename, mode="r", encoding="utf8") as f:
    started = False
    for line in f:
        line = line.strip()
        if started:
            datum = line.split(",")
            #ys.append(datum[-1])
            xs.append(datum) # note will be in string format
        elif "@DATA" in line:
            started = True
        elif line.startswith("@ATTRIBUTE"):
            info, typ = line.split('\t')
            attlabel, attname = info.split(' ',1)
            attributes.append(attname)
print attributes

'''
labels = [
      ("filename", "string"),
      ("level", "NUMERIC"),
      ("Number of Paragraphs", "NUMERIC"),
      ("Number of Sentences", "NUMERIC"),
      ("Number of Words", "NUMERIC"),
      ("Sentences per Paragraph", "NUMERIC"),
      ("Stand Dev of SentsPerPara", "NUMERIC"),
      ("Words per sentence", "NUMERIC"),
      ("sdWordsPerSent", "NUMERIC"),
      ("letters per word", "NUMERIC"),
      ("sdLettersPerWord", "NUMERIC"),
      ("Syllables per word", "NUMERIC"),
      ("sdSyllablesPerWord", "NUMERIC"),
      ("PLex", "NUMERIC"),
      ("S", "NUMERIC"),
      ("vocd", "NUMERIC"),
      ("mtld", "NUMERIC"),
      ("hdd", "NUMERIC"),
      ("vocab 1k", "NUMERIC"),
      ("vocab 2k", "NUMERIC"),
      ("vocab 3k", "NUMERIC"),
      ("vocab 4k", "NUMERIC"),
      ("vocab 8k", "NUMERIC"),
      ("vocab >8k", "NUMERIC"),
      ("Other vocab", "NUMERIC"),
      ("No. Spelling Corrections", "NUMERIC"),
      ("No. of MElt differences", "NUMERIC"),
      ("parsedok", "NUMERIC"),
      ("parsedcorr", "NUMERIC"),
      ("parsedrob", "NUMERIC"),
      ("Average weight per word", "NUMERIC"),
      ("single verbs", "NUMERIC"),
      ("auxiliary verbs", "NUMERIC"),
      ("compound verbs", "NUMERIC"),
      ("indicative verbs", "NUMERIC"),
      ("conditional verbs", "NUMERIC"),
      ("subjunctive verbs", "NUMERIC"),
      ("imperfect verbs", "NUMERIC"),
      ("future verbs", "NUMERIC"),
      ("vpresent", "NUMERIC"),
      ("non-finite verbs", "NUMERIC"),
      ("relative clauses", "NUMERIC"),
      ("nominative clauses", "NUMERIC"),
      ("accusative clauses", "NUMERIC"),
      ("locative clauses", "NUMERIC")
        ]
'''
# list of 4-tuples, will do a set of level plots for each (name in arff file, name for plot, (xmin, xmax), ymax)
# where xmin and xmax are for the plots
labels = [
      (u"wordsPerSent", u"Words per sentence", (0,25), 14),
      (u"PLex", u"PLex", (1.5,3.5), 10),
      (u"hdd", u"HD-D", (22,34), 14),
      (u"meltdiff", u"No. of MElt differences", (0,0.4), 18),
      (u"vaux", u"auxiliary verbs", (0,0.8), 40),
      (u"meanWordWordct", u"word to word cosθ",(0.7,1), 14),
      (u"toksBeforeMainVerb", u"Words before main verb", (0,12), 20),
]


# xlimits is a 2-tuple (xmin, xmax)
def plotProbDistribution(xlabel, title, mean, sigma, dist, xlimits=None, ymax=None):
    #fig = plt.subplot(111)
    #width = 0.8
    #fig.set_yscale('log')
    #plt.yscale('log')
    info =  ', $\mu=' + str(round(mean,2)) + ', \sigma=' + str(round(sigma,2)) + '$'


    plt.figure(figsize=(8,7))
    plt.title(title + " " + info, fontsize=32)
    plt.xlabel(xlabel, fontsize=32)
    #plt.ylabel("frequency (log scale)", fontsize=24)

    plt.tick_params(axis='both', which = 'major', labelsize=24) # major axis markings
    plt.tick_params(axis='both', which = 'minor', labelsize=16)  # minor axis markings
    plt.tight_layout() # adjusts the margins
    #plt.tick_params(axis='x', labelsize=48)  # minor axis markings

    #rc={'font.size': 32, 'axes.labelsize': 32, 'legend.fontsize': 32.0,
    #'axes.titlesize': 32, 'xtick.labelsize': 32, 'ytick.labelsize': 32}
    #plt.rcParams.update(**rc)

    print dist

    if ymax:
        plt.ylim(0, ymax)
    if xlimits:
        plt.xlim(xlimits)
        nbins = 15
        dx = (xlimits[1]-xlimits[0])/(1.0*nbins)
        binning = np.linspace(xlimits[0], xlimits[1], nbins+1)
        plt.hist(dist, bins=binning, histtype='bar')
        #dx = result[1][1] - result[1][0]
        scale = len(data)*dx
        plotbinning = np.linspace(xlimits[0], xlimits[1], 100) # plot with 50 bins for the gaussian

        plt.plot(plotbinning,mlab.normpdf(plotbinning,mean,sigma)*scale)
    else:
        plt.hist(dist, 10, histtype='bar')



    #plt.semilogy()
    #plt.yscale('log', nonposy='clip') # needed as log -> 0 causes problems for filling
    #width = 1.0
    #fig.set_xticks(np.arange(len(keys)) + width/2)
    #fig.set_xticklabels(range(len(keys)), rotation=45)
    #plt.ylim((0,1000))
    #plt.xlim((0,136))

    #frame = plt.gca()
    #frame.axes.get_xaxis().set_visible(False)
    title = re.sub(ur'\s', '_', title, flags=re.UNICODE)
    title = re.sub(ur'[\(\),\$\\>=\.\:]', '', title, flags=re.UNICODE)
    xlabel = re.sub(ur'\s', '_', xlabel, flags=re.UNICODE)
    xlabel = re.sub(ur'[\(\),\$\\>=\.\:]', '', xlabel, flags=re.UNICODE)

    plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/figures/afterlastminute/" + title + xlabel + ".png")
    #plt.show()
    #exit(10)

levelcolumn = attributes.index("level")
level2cefr = {1:"A1", 2:"A2", 3:"B1", 4:"B2", 6:"Native"}
for i in range(len(labels)):

    origlabel, title, xlimits, ymax = labels[i]
    colnum = attributes.index(origlabel)
    for level in [1,2,3,4,6]:
        data = [float(xs[k][colnum]) for k in range(len(xs)) if int(xs[k][levelcolumn])==level]
        mu = np.mean(data)
        sd = np.std(data)

        plotProbDistribution(title, u"level: " + level2cefr[level] , mu, sd, data, xlimits, ymax )

