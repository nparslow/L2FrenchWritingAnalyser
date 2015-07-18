# coding=utf-8
__author__ = 'nparslow'

import math

testtext = u"The value of q is often referred to as the order of the diversity. It defines the sensitivity of the" \
           u" diversity value to rare vs. abundant species by modifying how the weighted mean of the species" \
           u" proportional abundances is calculated. With some values of the parameter q, the value of Mq−1 assumes" \
           u" familiar kinds of weighted mean as special cases. In particular, q = 0 corresponds to the weighted" \
           u" harmonic mean, q = 1 to the weighted geometric mean and q = 2 to the weighted arithmetic mean. As q" \
           u" approaches infinity, the weighted generalized mean with exponent q−1 approaches the maximum p_i value," \
           u" which is the proportional abundance of the most abundant species in the dataset. Generally, increasing " \
           u"the value of q increases the effective weight given to the most abundant species. This leads to obtaining " \
           u"a larger Mq−1 value and a smaller true diversity (qD) value with increasing q."

testtext += u"When q = 1, the weighted geometric mean of the p_i values is used, and each species is exactly" \
            u" weighted by its proportional abundance (in the weighted geometric mean, the weights are the exponents)." \
            u" When q > 1, the weight given to abundant species is exaggerated, and when q < 1, the weight given to" \
            u" rare species is. At q = 0, the species weights exactly cancel out the species proportional abundances," \
            u" such that the weighted mean of the p_i values equals 1 / R even when all species are not equally abundant." \
            u" At q = 0, the effective number of species, {}^0\!D, hence equals the actual number of species R. " \
            u"In the context of diversity, q is generally limited to non-negative values. This is because negative" \
            u" values of q would give rare species so much more weight than abundant ones that" \
            u" {}^q\!D would exceed R.[3][4]"

testtext = u"The girl was stolen a bread, but Chaplin take a fault. So, they are going to put a Chaplin in jail." \
           u" But a woman saw that the girl stolen the bread, so they take Chaplin and the girl. When they" \
           u" was going to jail the girl and Chaplin ran away. They go to sit and talk about where they live." \
           u" The girl say that she live no where. So they dreaming a home where they can take orange in the" \
           u" tree and eat a breakfast in a kitchen. The Chaplin say that do the work then we got a house."

words = testtext.split()

word2count = {}
for word in words:
    if word not in word2count: word2count[word] = 0
    word2count[word] += 1

ntypes = len(word2count.keys())
nwords = len(words)

diversity = 0.0
for type in word2count:
    proba = word2count[type] * 1.0 / nwords
    diversity -= proba * math.log(proba)  # note the minus equals

print "diversity", diversity

# http://swizec.com/blog/measuring-vocabulary-richness-with-python/swizec/2528
from itertools import groupby
d = { "a": 3 , "b":5, "c":5, "d":5, "e":5}
M2 = sum([len(list(g))*(freq**2) for freq,g in groupby(sorted(d.values()))])
print M2

for x,y in groupby(sorted(d.values())):
    #print x
    for z in y:
        print z