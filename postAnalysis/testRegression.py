import math

__author__ = 'nparslow'

# goal is to test the output of weka's regression
# maybe using R is smarter ?

from combineArffs import readarff


arfffile = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/outArff/linearregressionresults.arff"

header, variables, rows = readarff(arfffile)

print header, variables, rows

pred_i = variables.index((u"@attribute", u"predictedlevel", u"numeric"))
true_i = variables.index((u"@attribute", u"level", u"numeric"))

print pred_i, true_i

# todo : generalise this for arbitrary borders
def classify( pred ):
    if pred < 1.5:
        return 1
    elif pred < 2.5:
        return 2
    elif pred < 3.5:
        return 3
    elif pred < 5:
        return 4
    else:
        return 6

#all = {1:[], 2:[], 3:[], 4:[], 6:[]} # ided as not original
tps = {1:[], 2:[], 3:[], 4:[], 6:[]} # true positives
fns = {1:[], 2:[], 3:[], 4:[], 6:[]} # false negatives
fps = {1:[], 2:[], 3:[], 4:[], 6:[]} # false positives

bad_off_diagonals = 0

for row in rows:
    pred = float(row[pred_i])
    vrai = int(row[true_i])

    predclass = classify(pred)
    if predclass != vrai:
        fps[predclass].append(vrai)
    #all[predclass].append(pred)

    if abs(predclass-vrai) > 1:
        bad_off_diagonals += 1

    # we'll take the nearest class as the chosen one
    # this means edges must be treated differently:
    if vrai == 1:
        if pred < 1.5:
            tps[vrai].append(pred)
        else:
            fns[vrai].append(pred)
    elif vrai == 6:
        if pred >= 5:
            tps[vrai].append(pred)
        else:
            fns[vrai].append(pred)
    elif vrai == 4: # as there is no 5:
        if pred >= 3.5 and pred < 5:
            tps[vrai].append(pred)
        else:
            fns[vrai].append(pred)
    else:
        if pred >= vrai - 0.5 and pred < vrai + 0.5:
            tps[vrai].append(pred)
        else:
            fns[vrai].append(pred)

print tps

print fns

def precision( tp, fp):
    return 1.0*tp/(tp+fp)

def recall( tp, fn ):
    return 1.0*tp/(tp+fn)

def fscore( prec, rec):
    return 2.0*prec*rec/(prec+rec)


for level in [1,2,3,4,6]:
    prec = precision( len(tps[level]), len(fps[level]))
    rec = recall(len(tps[level]), len(fns[level]))
    fsc = fscore(prec, rec)
    print level, fsc

print "bad off diags", bad_off_diagonals