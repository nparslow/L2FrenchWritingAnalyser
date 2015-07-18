__author__ = 'nparslow'

import json

import numpy as np
import matplotlib.pyplot as plt

results_vocd = {}

with open("/home/nparslow/Documents/AutoCorrige/vocabulary/perl/vocd_results.txt", 'r') as infile:
    results_vocd = json.load(infile)

print results_vocd

res_by_level = {}
for level in ['A', 'B', 'C', 'D', 'E']:
    # could be more efficient with only one loop over dictionary
    res_by_level[level] = [value for key, value in results_vocd.iteritems() if key[0] == level]



#x = np.arange(0, 5, 0.1);
#y = np.sin(x)
#plt.plot(x, y)

for level in ['A', 'B', 'C', 'D', 'E']:
    print [(key, value) for key, value in results_vocd.iteritems() if key[0] == level]

plt.boxplot([res_by_level[x] for x in ['A', 'B', 'C', 'D', 'E']])
plt.show()


# for
results_mtld = {}

with open("/home/nparslow/Documents/AutoCorrige/vocabulary/perl/mtld_trans_results.txt", 'r') as infile:
    results_mtld = json.load(infile)

print results_mtld

res_by_level_mtld = {}
for level in ['A', 'B', 'C', 'D', 'E']:
    # could be more efficient with only one loop over dictionary
    res_by_level_mtld[level] = [value for key, value in results_mtld.iteritems() if key[0] == level]



#x = np.arange(0, 5, 0.1);
#y = np.sin(x)
#plt.plot(x, y)

for level in ['A', 'B', 'C', 'D', 'E']:
    print [(key, value) for key, value in results_mtld.iteritems() if key[0] == level]

plt.boxplot([res_by_level_mtld[x] for x in ['A', 'B', 'C', 'D', 'E']])
plt.show()

def getResultsToDict( jsonfile, toDict):
    rawresults = {}
    with open( jsonfile, 'r') as infile:
        rawresults = json.load(infile)

    #print rawresults

    for level in ['A', 'B', 'C', 'D', 'E']:
        # could be more efficient with only one loop over dictionary
        toDict[level] = [value for key, value in rawresults.iteritems() if key[0] == level]

def boxPlotByLevel( resultsByLevel, levels):
    plt.boxplot([resultsByLevel[x] for x in levels])
    plt.show()


# scatter plot of the two:
scatter = {}
#for level in ['A', 'B', 'C', 'D', 'E']:
for name in results_vocd:
    level = name[0]
    if level not in scatter: scatter[level] = {"xs":[], "ys":[]}
    scatter[level]["xs"].append(results_vocd[name])
    scatter[level]["ys"].append(results_mtld[name])

fig = plt.figure()

colors = ['b', 'g', 'r', 'c', 'm']
color_num = 0
for level in scatter:
    col =colors[color_num]
    plt.scatter(scatter[level]["xs"], scatter[level]["ys"], color=col)
    color_num += 1


plt.show()



# shows large variation for lower levels, but prob just related to low word count
varietyResults = {}
# re http://search.cpan.org/~axanthos/Lingua-Diversity/lib/Lingua/Diversity/VOCD.pm
varietyJSON = "/home/nparslow/Documents/fouille_de_textes/projet/lund/diversityVarietyMSP.json"
getResultsToDict(varietyJSON, varietyResults)

# ID, i.e. diff D with tokens v D with Lemma, seems a bit better actually than MSP
varietyDT = "/home/nparslow/Documents/fouille_de_textes/projet/lund/diversityVarietyDT.json"
varietyDTresults = {}
with open(varietyDT, 'r') as infile:
  varietyDTresults =  json.load(infile)
#getResultsToDict(varietyDT, varietyDTresults)
varietyDL = "/home/nparslow/Documents/fouille_de_textes/projet/lund/diversityVarietyDL.json"
varietyDLresults = {}
with open(varietyDL, 'r') as infile:
  varietyDLresults =  json.load(infile)
#getResultsToDict(varietyDL, varietyDLresults)
print  varietyDTresults
print  varietyDLresults

IDresults = {}
for name in varietyDLresults:
    level = name[0]
    if level not in IDresults: IDresults[level] = []
    IDresults[level].append(varietyDTresults[name] - varietyDLresults[name])
    # Next line = trying the relative difference
    #IDresults[level].append( (varietyDTresults[name] - varietyDLresults[name])/varietyDTresults[name])

boxPlotByLevel(IDresults, ['A', 'B', 'C', 'D', 'E' ])

# scatter plot of the DL and DT rather than just look at the difference:
scatterD = {}
#for level in ['A', 'B', 'C', 'D', 'E']:
for name in varietyDLresults: # note potentially DL has less results than DT as there is the 50 elements minimum
    level = name[0]
    if level not in scatterD: scatterD[level] = {"xs":[], "ys":[]}
    scatterD[level]["xs"].append(varietyDLresults[name])
    scatterD[level]["ys"].append(varietyDTresults[name])

fig = plt.figure()

colors = ['b', 'g', 'r', 'c', 'm']
color_num = 0
for level in scatter:
    col =colors[color_num]
    plt.scatter(scatterD[level]["xs"], scatterD[level]["ys"], color=col)
    color_num += 1

plt.show()
# scatter plot suggests LD and LT highly correlated and larger difference at high level prob just due to
# higher LD and LT values leading to a larger difference (but not a larger difference relative to LT)
