import re

__author__ = 'nparslow'


import json
import codecs
import math
import matplotlib.pyplot as plt
import numpy as np
import stat
import matplotlib.pyplot as plt
import numpy as np


def plotProbDistribution(title, dist):
    #fig = plt.subplot(111)
    #width = 0.8
    #fig.set_yscale('log')
    #plt.yscale('log')

    plt.figure(figsize=(8,7))
    plt.title(title, fontsize=32)
    plt.xlabel("MElt POS confidence", fontsize=24)
    plt.ylabel("frequency (log scale)", fontsize=24)
    plt.tick_params(axis='both', which = 'major', labelsize=18) # major axis markings
    plt.tick_params(axis='both', which = 'minor', labelsize=12)  # minor axis markings


    plt.hist(dist, bins=50, histtype='bar')
    #plt.semilogy()
    plt.yscale('log', nonposy='clip') # needed as log -> 0 causes problems for filling
    width = 1.0
    #fig.set_xticks(np.arange(len(keys)) + width/2)
    #fig.set_xticklabels(range(len(keys)), rotation=45)
    #plt.ylim((0,1000))
    #plt.xlim((0,136))

    #frame = plt.gca()
    #frame.axes.get_xaxis().set_visible(False)
    title = re.sub(ur'\s', '_', title, flags=re.UNICODE)
    title = re.sub(ur'[\(\)]', '', title, flags=re.UNICODE)

    plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/figures/meltprobs_" + title + ".png")
    plt.show()
    #exit(10)

jsonfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/meltprobs.json"
with codecs.open(jsonfilename, mode="r", encoding="utf8") as jfile:
    meltprobs = json.load(jfile)


othertags = []
others = []
allerrs = []
for x in meltprobs:
    if len(meltprobs[x]) > 50:
        #arr = np.array([math.log(y) for y in meltprobs[x]])
        arr = np.array(meltprobs[x])
        print "key:", x, len(arr), round(np.mean(arr, axis=0),3), round(np.std(arr, axis=0),3), round(math.sqrt(sum([math.pow(1-y,2) for y in arr])/len(arr)), 3)
        plotProbDistribution(x, arr)
    else:
        others.extend(meltprobs[x])
        othertags.append(x)
    if x != "NoError":
        allerrs.extend(meltprobs[x])


plotProbDistribution("other", others)
print "other:", othertags
print "key:", "other", len(others), round(np.mean(others, axis=0),3), round(np.std(others, axis=0),3), round(math.sqrt(sum([math.pow(1-y,2) for y in others])/len(others)))

plotProbDistribution("all errors", allerrs)
print "key:", "all errors", len(allerrs), round(np.mean(allerrs, axis=0),3), round(np.std(allerrs, axis=0),3), round(math.sqrt(sum([math.pow(1-y,2) for y in allerrs])/len(allerrs)))

exit(0)

jsonfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/meltsentprobs.json"
with codecs.open(jsonfilename, mode="r", encoding="utf8") as jfile:
    meltsentprobs = json.load(jfile)

def plotSentProbDistribution(xs, ys, title):
    #fig = plt.subplot(111)
    #width = 0.8
    #fig.set_yscale('log')
    #plt.yscale('log')


    plt.figure(figsize=(8,7))
    plt.title(title, fontsize=32)
    plt.xlabel("error density (errors/word)", fontsize=24)
    plt.ylabel("mean POS confidence", fontsize=24)
    plt.tick_params(axis='both', which = 'major', labelsize=18) # major axis markings
    plt.tick_params(axis='both', which = 'minor', labelsize=12)  # minor axis markings

    plt.ylim((0.5,1))
    plt.xlim((0,0.75))
    plt.scatter(xs, ys)
    #plt.title(title)
    #plt.semilogy()
    #plt.yscale('log', nonposy='clip') # needed as log -> 0 causes problems for filling
    width = 1.0
    #fig.set_xticks(np.arange(len(keys)) + width/2)
    #fig.set_xticklabels(range(len(keys)), rotation=45)

    #plt.title(title)
    #plt.xlabel("errors per word")
    #plt.ylabel("average MElt probability")
    #frame = plt.gca()
    #frame.axes.get_xaxis().set_visible(False)
    # convert title spaces to underscores:
    title = re.sub(ur'\s', '_', title, flags=re.UNICODE)
    title = re.sub(ur'[\(\)]', '', title, flags=re.UNICODE)

    plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/figures/meltsentprob_" + title + ".png")
    plt.show()
    #exit(10)


plotSentProbDistribution(meltsentprobs["eps"], meltsentprobs["geomean"], "geometric mean")

plotSentProbDistribution(meltsentprobs["eps"], meltsentprobs["algmean"], "arithmetic mean") # arithmetic mean


#exit(10)

def plotWeightProbDistribution( ys, title):
    print "weight mean, sd", np.mean(ys), np.std(ys)
    #fig = plt.subplot(111)
    #width = 0.8
    #fig.set_yscale('log')
    #plt.yscale('log')
    #plt.scatter(xs, ys)
    xlow, xhigh = -2000, 2000
    plt.figure(figsize=(8,7))
    plt.xlim((xlow,xhigh))
    plt.hist( np.array([y for y in ys if y >= xlow and y < xhigh]), bins=20)
    #plt.title(title)
    #plt.semilogy()
    #plt.yscale('log', nonposy='clip') # needed as log -> 0 causes problems for filling
    width = 1.0
    #fig.set_xticks(np.arange(len(keys)) + width/2)
    #fig.set_xticklabels(range(len(keys)), rotation=45)
    #plt.ylim((0,1))
    plt.title(title, fontsize=24)
    #plt.title(title, fontsize=16)
    #plt.xlabel("errors per word", fontsize=24)
    plt.xlabel("sentence weight per word", fontsize=24)
    plt.tick_params(axis='both', which = 'major', labelsize=18) # major axis markings
    plt.tick_params(axis='both', which = 'minor', labelsize=9)  # minor axis markings
    #frame = plt.gca()
    #frame.axes.get_xaxis().set_visible(False)
    title = re.sub(ur'\s', '_', title, flags=re.UNICODE)
    title = re.sub(ur'[\(\)]', '', title, flags=re.UNICODE)
    plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/figures/frmgsentweight_" + title + ".png")
    plt.show()
    #exit(10)
    #if closeafter:
    #plt.close()

weightstoplotnoerror = []
weightstoplot = []
minweightstoplotnoerror = []
minweightstoplot = []
for i in range(len(meltsentprobs["origweight"])):
    #print meltsentprobs["origweight"][i]
    if meltsentprobs["eps"][i] == 0:
        weightstoplotnoerror.append(meltsentprobs["origweight"][i][0])
        minweightstoplotnoerror.append(meltsentprobs["origweight"][i][1])
    else:
        if meltsentprobs["origweight"][i][0] != 0:
            weightstoplot.append(meltsentprobs["origweight"][i][0])
            minweightstoplot.append(meltsentprobs["origweight"][i][1])
        # ignore == 0 as it is robust

#plotWeightProbDistribution(meltsentprobs["eps"], meltsentprobs["origweight"], "frmg weight")
plotWeightProbDistribution( weightstoplotnoerror, "Weight per word (sentences without errors)")
plotWeightProbDistribution( weightstoplot, "Weight per word (sentences with errors)")



def plotMaxWeightProbDistribution(ys, title):
    #fig = plt.subplot(111)
    #width = 0.8
    #fig.set_yscale('log')
    #plt.yscale('log')
    #plt.scatter(xs, ys)
    xlow, xhigh = -1000, 9000
    plt.figure(figsize=(8,7))
    plt.xlim((xlow,xhigh))
    plt.hist( np.array([y for y in ys if y >= xlow and y < xhigh]), bins=10)
    #plt.title(title)
    plt.tick_params(axis='both', which = 'major', labelsize=18) # major axis markings
    plt.tick_params(axis='both', which = 'minor', labelsize=9)  # minor axis markings
    #plt.semilogy()
    #plt.yscale('log', nonposy='clip') # needed as log -> 0 causes problems for filling
    width = 1.0
    #fig.set_xticks(np.arange(len(keys)) + width/2)
    #fig.set_xticklabels(range(len(keys)), rotation=45)
    #plt.ylim((0,1))

    plt.title(title, fontsize=32)
    plt.xlabel("max weight in sentence", fontsize=24)
    #plt.ylabel("sentence weight", fontsize=24)

    #frame = plt.gca()
    #frame.axes.get_xaxis().set_visible(False)
    title = re.sub(ur'\s', '_', title, flags=re.UNICODE)
    title = re.sub(ur'[\(\)]', '', title, flags=re.UNICODE)
    plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/figures/frmgsentweight_" + title + ".png")
    plt.show()
    #exit(10)
    #if closeafter:
    #plt.close()

plotMaxWeightProbDistribution( minweightstoplotnoerror, "Max Weight (sentences without errors)")
plotMaxWeightProbDistribution( minweightstoplot, "Max Weight (sentences without errors)")

print len(weightstoplotnoerror), len(weightstoplot)
print round(np.mean(weightstoplotnoerror, axis=0), 2), round(np.std(weightstoplotnoerror),2)
print round(np.mean(weightstoplot, axis=0), 2), round(np.std(weightstoplot),2)
print round(np.mean(minweightstoplotnoerror, axis=0), 2), round(np.std(minweightstoplotnoerror),2)
print round(np.mean(minweightstoplot, axis=0), 2), round(np.std(minweightstoplot),2)

#print weightstoplot
#plotWeightProbDistribution(meltsentprobs["eps"], meltsentprobs["corrweight"], "frmg weight")