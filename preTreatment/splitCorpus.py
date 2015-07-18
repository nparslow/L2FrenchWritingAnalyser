import codecs
import os
import random

__author__ = 'nparslow'

# will take a corpus directory and create 3 files train, test, dev
# these will be cats of 80%, 10% and 10% in the directory (randomly?)

_TRAIN_ = 0.80
_TEST_  = 0.10
# and _DEV_ is the rest

latin1files = [
    "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_LITTAVANCE/M2_SYNTH_BOCH/CorpusTXT/05_BOCH_SYNTH.txt"
]
utf8files = [
    "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_LITTAVANCE/M2_SYNTH_BOCH/CorpusTXT/06_BOCH_SYNTH.txt",
    "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_LITTAVANCE/M2_SYNTH_BOCH/CorpusTXT/07_BOCH_SYNTH.txt",
]

def analyse( path, outputpath, filenumbers ):
    if os.path.isdir(path):
        filesindir = []
        dirsindir = []
        for element in os.listdir(path):
            fullelement = os.path.join(path, element)
            # we need to count the no. of files:
            if os.path.isfile(fullelement):
                filesindir.append(fullelement)
            else:
                dirsindir.append(fullelement)

        # the store and shuffle approach is to avoid random variation in size
        random.shuffle(filesindir)
        for i in range(len(filesindir)):
            category = getCategory(i, len(filesindir))
            filenumbers[category] +=1
            analyseFile(filesindir[i], category, outputpath)

        for dir in dirsindir:
            analyse(dir, outputpath, filenumbers)

    else:
        analyseFile(path, "split", outputpath)

# tries to account for directories with < 10 files favoring train:
def getCategory(i, total, filenumbers={"train":0, "test":0, "dev":0}):
    truetotal = total + sum(filenumbers.values())
    truetrain = (_TRAIN_*truetotal-filenumbers["train"])/truetotal
    truetest = ((_TRAIN_+_TEST_)*truetotal-(filenumbers["train"]+filenumbers["test"]))/truetotal
    segment = 1.0*i/total
    category = "train"
    if segment > truetrain:
        if segment > truetest:
            category = "dev"
        else:
            category = "test"
    return category

# category can be train, test, dev or split
# if split the lines of the file will be split into the parts
def analyseFile( filename, category, outputpath ):
    enc = "latin1"
    if filename in utf8files:
        enc = "utf8"
    if category == "split":
        lines = []
        with codecs.open(filename, mode='r', encoding=enc) as infile:
            lines = infile.readlines()
        random.shuffle(lines)
        for i in lines:
            category = getCategory(i, len(lines))
            if enc != "utf8":
                lines[i].encode('utf8')
            with codecs.open( os.path.join(outputpath, category + ".txt"), mode="a", encoding="utf8") as outfile:
                outfile.write(lines[i])
    else:
        print "reading file", filename, category
        with codecs.open( filename, mode="r", encoding=enc) as infile:
            data = infile.read()
            if enc != "utf8":
                data.encode('utf8')
            with codecs.open( os.path.join(outputpath, category + ".txt"), mode="a", encoding="utf8") as outfile:
                outfile.write(data)

'''
def splitCorpus(corpusDir, outputPath):

    for category in ["train", "test", "dev"]:
        fullfilename = os.path.join(outDir, category + ".txt")
        with codecs.open(fullfilename, mode="w", encoding="utf8") as cfile:
            cfile.write()

    analyse(corpusDir, outDir)
'''

corpusDir = "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_LITTAVANCE"
#corpusDir = "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_LITTAVANCE/L2_DOS_SORB/CorpusTXT/"

outDir = "/home/nparslow/Documents/AutoCorrige/Corpora/split/CORPUS_LITTAVANCE/"
for cat in ["train", "test", "dev"]:
    os.remove(os.path.join(outDir, cat + ".txt"))
analyse(corpusDir, outDir, {"train":0, "test":0, "dev":0})


# optirun not working atm :/
# python lstm.py --train ~/Documents/AutoCorrige/Corpora/split/CORPUS_LITTAVANCE/train.txt ~/Documents/AutoCorrige/Corpora/split/CORPUS_LITTAVANCE/dev.txt ~/Documents/AutoCorrige/Corpora/split/CORPUS_LITTAVANCE/test.txt  --hidden 100 --save-net firsttest.lstm-lm --vocabulary ~/Documents/AutoCorrige/Corpora/outputs/learner_vocab.list
# 50 words/s expected time 6:30 (no cuda)