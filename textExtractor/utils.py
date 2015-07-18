
import itertools
from operator import mul

__author__ = 'nparslow'

# generally useful functions


def flatten2LevelList( inlist ):
    return list(itertools.chain(*inlist))

# returns the product of elements in a list
def product( somelist ):
    return reduce(mul, somelist, 1)

def combineCountDicts( listofdicts ):
    outdict = {}
    for dic in listofdicts:
        for key in dic:
            if key not in outdict: outdict[key] = 0
            outdict[key] += dic[key]
    return outdict

# note : returns the
def rollingMean( oldmean, oldn, newvalue, repeated=1):
    if oldn == 0:
        return newvalue, repeated
    else:
        newmeanp = (oldmean*oldn + newvalue*repeated)/(0.0+oldn+repeated)
        return newmeanp, oldn + repeated

def geomean(iterable):
    return (reduce(operator.mul, iterable)) ** (1.0/len(iterable))

