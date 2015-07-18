__author__ = 'nparslow'


import json
import codecs

import matplotlib.pyplot as plt
import numpy as np

jsonfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/treecompare.json"
with codecs.open(jsonfilename, mode="r", encoding="utf8") as jfile:
    treecompare = json.load(jfile)

print treecompare.keys()
#print treecompare[u'216']

precs = []
recs = []

for tid in sorted(treecompare.keys(), key=lambda x:len(treecompare[x]), reverse=True):
    tp = 1.0*sum([x[0] for x in treecompare[tid] ])
    precision = tp/sum(x[0]+x[1] for x in treecompare[tid])
    recall = tp/sum(x[0]+x[2] for x in treecompare[tid])

    print "tree id:", tid
    print "n sentences with it:", len(treecompare[tid])
    print "prec:", precision
    print "rec: ", recall
    precs.append(precision)
    recs.append(recall)


print len([x for x in treecompare if len(treecompare[x])>50])

print "ntrees:", len(treecompare.keys())

def plotTreeDistribution(treecompare):
    fig = plt.subplot(111)
    #width = 0.8
    keys = sorted([x for x in treecompare.keys()], key=lambda x:len(treecompare[x]), reverse=True) # if len(treecompare[x])>40
    plt.bar(range(len(keys)), [len(treecompare[x]) for x in keys])
    width = 1.0
    #fig.set_xticks(np.arange(len(keys)) + width/2)
    #fig.set_xticklabels(range(len(keys)), rotation=45)
    plt.ylim((0,1000))
    plt.xlim((0,136))
    #frame = plt.gca()
    #frame.axes.get_xaxis().set_visible(False)
    plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/figures/treedist.png")
    plt.show()

def plotPrecision(treecompare, precs, recs):
    fig = plt.subplot(111)
    fscore = [2*precs[i]*recs[i]/(precs[i]+recs[i]) for i in range(len(precs))]
    #width = 0.8
    keys = sorted([x for x in treecompare.keys()], key=lambda x:len(treecompare[x]), reverse=True)
    plt.bar(range(len(keys)), fscore)
    width = 1.0
    #fig.set_xticks(np.arange(len(keys)) + width/2)
    #fig.set_xticklabels(keys, rotation=45)
    plt.ylim((0,1.0))
    plt.xlim((0,136))
    #frame = plt.gca()
    #frame.axes.get_xaxis().set_visible(False)
    plt.savefig("/home/nparslow/Documents/AutoCorrige/Corpora/figures/treefscore.png")
    plt.show()

plotTreeDistribution(treecompare)

plotPrecision(treecompare, precs, recs)

