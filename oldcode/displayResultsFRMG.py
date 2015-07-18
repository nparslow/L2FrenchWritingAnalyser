__author__ = 'nparslow'

import math
import json
import matplotlib.pyplot as plt
import numpy as np
import operator # for dictionary sorting
import re

def combineDictionary( indict ):
    outdict = {}
    for key in indict: # key will be the studentSentence
        for secondkey in indict[key]: # secondkey is the metagrammar tree id
            if secondkey not in outdict: outdict[secondkey] = 0
            outdict[secondkey] += indict[key][secondkey]
    return outdict

def combineDictionaryToStudent( indict ):
    outdict = {}
    student2NumSentences = {}
    for level in indict:
        for studentSentence in indict[level]: # key is the studentSentence
            #print studentSentence
            student = re.search(r"(?<=FRMG)\w+(?=Sentence)", studentSentence).group(0)
            #print student
            if student not in outdict: outdict[student] = {}
            if student not in student2NumSentences: student2NumSentences[student] = 0
            student2NumSentences[student] += 1
            for treeid in indict[level][studentSentence]:
                if treeid not in outdict[student]: outdict[student][treeid] = 0
                outdict[student][treeid] += indict[level][studentSentence][treeid]
    return outdict, student2NumSentences

def sortAndPlot( indict ):
    res = sorted(indict.iteritems(), key=operator.itemgetter(1), reverse=True)
    plt.bar(np.arange(len(res)), [math.log(y,10) for x,y in res])
    plt.show()



res2level2authorsentence = {}
with open("/home/nparslow/Documents/fouille_de_textes/projet/lund/frmgStats" + ".json", 'r') as infile:
    res2level2authorsentence = json.load(infile)

results_frmg = {}
for level in res2level2authorsentence.keys():
    results_frmg[level] = combineDictionary(res2level2authorsentence[level])
    print sorted(results_frmg[level].iteritems(), key=operator.itemgetter(1), reverse=True)

    '''
    sortAndPlot(results_frmg[level])
    '''

    #res = sorted(results_frmg[level].iteritems(), key=operator.itemgetter(1), reverse=True)
    # plot for the combined level:
    '''
    plt.bar(np.arange(len(res)), [math.log(y,10) for x,y in res])
    plt.show()
    '''

student2results, student2NumSentences = combineDictionaryToStudent( res2level2authorsentence)

student2info = {}
for student in student2results:
    tokens = sum(student2results[student].values())
    types = len(student2results[student].keys())
    sentences = student2NumSentences[student]

    print student, "types:", types,\
        "tree tokens:", tokens,\
        "sentences:", sentences, \
        "tok/sent:", 1.0*tokens/sentences,\
        "typ/sent:", 1.0*types/sentences

    if student not in student2info: student2info[student] = {}
    student2info[student]["tokens"] = tokens
    student2info[student]["types"] = types
    student2info[student]["sentences"] = sentences

    '''
    sortAndPlot(student2results[student])
    '''

level2info2data = {}
for student in student2info:
    level = student[0]
    if level not in level2info2data: level2info2data[level] = \
        {"tokens":[], "types":[], "sentences":[]}
    level2info2data[level]["tokens"].append(student2info[student]["tokens"])
    level2info2data[level]["types"].append(student2info[student]["types"])
    level2info2data[level]["sentences"].append(student2info[student]["sentences"])

level2tokratio = {}
for level in level2info2data:
    #if level not in level2tokratio: level2tokratio[level] = []
    level2tokratio[level] = [ 1.0*level2info2data[level]["tokens"][i]/level2info2data[level]["sentences"][i]
                        for i in range(len(level2info2data[level]["tokens"])) ]
plt.boxplot([level2tokratio[x] for x in ['A', 'B', 'C', 'D', 'E']])
plt.show()


# note this shouldn't be as good because will vary with length of text (only natives show a difference)
level2typratio = {}
for level in level2info2data:
    #if level not in level2tokratio: level2tokratio[level] = []
    level2typratio[level] = [ 1.0*level2info2data[level]["types"][i]/level2info2data[level]["sentences"][i]
                        for i in range(len(level2info2data[level]["types"])) ]
plt.boxplot([level2typratio[x] for x in ['A', 'B', 'C', 'D', 'E']])
plt.show()

level2ntypes = {}
for level in level2info2data:
    #if level not in level2tokratio: level2tokratio[level] = []
    level2ntypes[level] = [ level2info2data[level]["types"][i]
                        for i in range(len(level2info2data[level]["types"])) ]
plt.boxplot([level2ntypes[x] for x in ['A', 'B', 'C', 'D', 'E']])
plt.show()


'''
fig = plt.figure()
for student in student2time2score:
    xs = [x for x in ["1", "2", "3", "4"] if x in student2time2score[student]]
    ys = [student2time2score[student][x] for x in xs]
    print student, ys
    plt.plot(xs, ys)
plt.show()
'''


'''
# old version: for files by level
results_frmg = {}
print results_frmg

res_by_level = {}
for level in ['A', 'B', 'C', 'D', 'E']:
    with open("/home/nparslow/Documents/fouille_de_textes/projet/lund/frmgStats" + level + ".json", 'r') as infile:
        results_frmg[level] = json.load(infile)



for level in ['A', 'B', 'C', 'D', 'E']:
    print sorted(results_frmg[level].iteritems(), key=operator.itemgetter(1), reverse=True)
    res = sorted(results_frmg[level].iteritems(), key=operator.itemgetter(1), reverse=True)

    #print [x for x,y in res], [y for x,y in res]
    plt.bar(np.arange(len(res)), [math.log(y,10) for x,y in res])
    plt.show()
'''

#plt.boxplot([res_by_level[x] for x in ['A', 'B', 'C', 'D', 'E']])
#plt.show()

