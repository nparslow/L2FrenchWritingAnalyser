#!/usr/bin/python
import json
import math
import operator

__author__ = 'nparslow'

import os
import re
import codecs
import matplotlib.pyplot as plt
import numpy as np

#from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET

#import documentProperties

def getLogFileInfo(logFilename):
    sentenceinfos = []
    with codecs.open(logFilename, mode='r', encoding='latin-1') as infile:
        for line in infile:
            # each line of interest has 'analysis sentencenumber sentence'
            # we take the first 2
            #sentenceinfo = re.match(ur'(ok|robust|corrected)\s(\d+)', line, flags=re.UNICODE)
            sentenceinfo = re.match(ur'(\w+)\s(\d+)\s', line, flags=re.UNICODE)
            if sentenceinfo:
                #allpossibleresults.add(sentenceinfo.groups()[0])
                sentenceinfos.append(sentenceinfo.groups())
    return sentenceinfos

# needed to remove extras 70, 84, 162, 203, 394 (note it was hidden by double)
'''
rm analysed_SpellCheckerCorrected/entrycorrected_70/0/0/0/entrycorrected_70.E3.*
  ~/Documents/AutoCorrige/Corpora $vi analysed_SpellCheckerCorrected/entrycorrected_84.log
rm  ~/Documents/AutoCorrige/Corpora $rm analysed_SpellCheckerCorrected/entrycorrected_84/0/0/0/entrycorrected_84.E3.*
  ~/Documents/AutoCorrige/Corpora $vi analysed_SpellCheckerCorrected/entrycorrected_162.log
rm  ~/Documents/AutoCorrige/Corpora $rm analysed_SpellCheckerCorrected/entrycorrected_162/0/0/0/entrycorrected_162.E2.*
  ~/Documents/AutoCorrige/Corpora $vi analysed_SpellCheckerCorrected/entrycorrected_203.log
rm  ~/Documents/AutoCorrige/Corpora $rm analysed_SpellCheckerCorrected/entrycorrected_203/0/0/0/entrycorrected_203.E3.*
  ~/Documents/AutoCorrige/Corpora $vi analysed_SpellCheckerCorrected/entrycorrected_204.log
rm  ~/Documents/AutoCorrige/Corpora $rm analysed_SpellCheckerCorrected/entrycorrected_204/0/0/0/entrycorrected_204.E5.*
  ~/Documents/AutoCorrige/Corpora $vi analysed_SpellCheckerCorrected/entrycorrected_364.log
rm  ~/Documents/AutoCorrige/Corpora $rm analysed_SpellCheckerCorrected/entrycorrected_364/0/0/0/entrycorrected_364.E9.*
  ~/Documents/AutoCorrige/Corpora $vi analysed_SpellCheckerCorrected/entrycorrected_391.log
rm  ~/Documents/AutoCorrige/Corpora $rm analysed_SpellCheckerCorrected/entrycorrected_391/0/0/0/entrycorrected_391.E4.*
  # also 354 bugs and repeats a sentence: (no. 7 shouldn't exist in corrected)
  rm analysed_SpellCheckerCorrected/entrycorrected_354/0/0/0/entrycorrected_354.E7.*
  rm analysed_SpellCheckerCorrected/entrycorrected_354/0/0/0/entrycorrected_354.E8.*
'''
sentenceAlignments = {
    43: [(frozenset([1]), frozenset([1])), (frozenset([2]), frozenset([2])), (frozenset([3]), frozenset([3,4]))],
    212: [(frozenset([1]), frozenset([1,2])), (frozenset([2]), frozenset([3]))],
    191: [(frozenset([1]), frozenset([1,2])), (frozenset([2]), frozenset([3]))],
    363: [(frozenset([1]), frozenset([1])), (frozenset([2,3]), frozenset([2])), (frozenset([4]), frozenset([3])),
          (frozenset([5]), frozenset([4])), (frozenset([6]), frozenset([5])), (frozenset([7]), frozenset([6])),
          (frozenset([8]), frozenset([7])), (frozenset([9]), frozenset([8])), (frozenset([10]), frozenset([9])),
          (frozenset([11]), frozenset([10])), (frozenset([12]), frozenset([11])), (frozenset([13]), frozenset([12])),
          (frozenset([14]), frozenset([13])), (frozenset([15]), frozenset([14])), (frozenset([16]), frozenset([15])),
          (frozenset([17]), frozenset([16])), (frozenset([18]), frozenset([17])), (frozenset([19]), frozenset([18])),
          (frozenset([20]), frozenset([19])) ],
    193: [(frozenset([1]), frozenset([1,2])), (frozenset([2]), frozenset([3]))],
    271: [(frozenset([1]), frozenset([1,2])), (frozenset([2]), frozenset([3]))],
    338: [(frozenset([1]), frozenset([1,2])), (frozenset([2]), frozenset([3])), (frozenset([3]), frozenset([4])),
          (frozenset([4]), frozenset([5])), (frozenset([5]), frozenset([6])), (frozenset([6]), frozenset([7]))],
    369: [(frozenset([1]), frozenset([1])), (frozenset([2]), frozenset([2])), (frozenset([3]), frozenset([3])),
          (frozenset([4]), frozenset([4])), (frozenset([5]), frozenset([5])), (frozenset([6]), frozenset([6])),
          (frozenset([7]), frozenset([7])), (frozenset([8]), frozenset([8])), (frozenset([9]), frozenset([9,10])),
          (frozenset([10]), frozenset([11])), (frozenset([11]), frozenset([12])), (frozenset([12]), frozenset([13]))],
    199: [(frozenset([1]), frozenset([1])), (frozenset([2]), frozenset([2,3])) ],
    355: [(frozenset([1]), frozenset([1])), (frozenset([2]), frozenset([2])), (frozenset([3]), frozenset([3])),
          (frozenset([4]), frozenset([4,5])), (frozenset([5]), frozenset([6])) ],
    138: [(frozenset([1]), frozenset([1])), (frozenset([2]), frozenset([2,3])), ],
    55: [(frozenset([1]), frozenset([1])), (frozenset([2,3]), frozenset([2])), ],
    108: [(frozenset([1]), frozenset([1])), (frozenset([2]), frozenset([2,3])), ],
    214: [(frozenset([1]), frozenset([1,2])), (frozenset([2]), frozenset([3]))],
    185: [(frozenset([1]), frozenset([1])), (frozenset([2]), frozenset([2,3])), (frozenset([3]), frozenset([4]))],
    391: [(frozenset([1,2]), frozenset([1])), (frozenset([3]), frozenset([2])), (frozenset([4]), frozenset([3]))],
    382: [(frozenset([1]), frozenset([1])), (frozenset([2]), frozenset([2,3])), (frozenset([3]), frozenset([4])),
          (frozenset([4]), frozenset([5])), (frozenset([5]), frozenset([6]))],
    354: [(frozenset([1,2]), frozenset([1])), (frozenset([3]), frozenset([2])), (frozenset([4]), frozenset([3])),
          (frozenset([5]), frozenset([4])), (frozenset([6]), frozenset([5])), (frozenset([7]), frozenset([6]))],
    173: [(frozenset([1]), frozenset([1,2]))]
}

def analyse( path, corrpath, erroralignpath, meltorigpath, meltcorrpath ):
    sentenceCounts = {"orig":0, "corr":0, "diff":0,
                      "easyalign":0, "hardalign":0,
                      "analysed":set([]),
                      "matchcorrections" : 0, "allcorrections" : 0,
                      "noncorrections": {"found":{},
                                         "nonfound":{},},
                      "spelling": {
                          "found": {},
                          "notfound": {},
                          "foreign": {},
                          "changed": {},
                        },
                      "treecompare":{},
                      "treecomp_prec":  # [mean, n]
                          {"orig_ok":        {"corr_ok":[0.0, 0], "corr_corrected":[0.0, 0], "corr_robust":[0.0, 0]},
                           "orig_corrected": {"corr_ok":[0.0, 0], "corr_corrected":[0.0, 0], "corr_robust":[0.0, 0]},
                           "orig_robust":    {"corr_ok":[0.0, 0], "corr_corrected":[0.0, 0], "corr_robust":[0.0, 0]}
                          },
                      "treecomp_rec" :
                          {"orig_ok":        {"corr_ok":[0.0, 0], "corr_corrected":[0.0, 0], "corr_robust":[0.0, 0]},
                           "orig_corrected": {"corr_ok":[0.0, 0], "corr_corrected":[0.0, 0], "corr_robust":[0.0, 0]},
                           "orig_robust":    {"corr_ok":[0.0, 0], "corr_corrected":[0.0, 0], "corr_robust":[0.0, 0]}
                          },
                      "badtreecomp_prec":  # [mean, n]
                          {"orig_ok":        {"corr_ok":[0.0, 0], "corr_corrected":[0.0, 0], "corr_robust":[0.0, 0]},
                           "orig_corrected": {"corr_ok":[0.0, 0], "corr_corrected":[0.0, 0], "corr_robust":[0.0, 0]},
                           "orig_robust":    {"corr_ok":[0.0, 0], "corr_corrected":[0.0, 0], "corr_robust":[0.0, 0]}
                          },
                      "badtreecomp_rec" :
                          {"orig_ok":        {"corr_ok":[0.0, 0], "corr_corrected":[0.0, 0], "corr_robust":[0.0, 0]},
                           "orig_corrected": {"corr_ok":[0.0, 0], "corr_corrected":[0.0, 0], "corr_robust":[0.0, 0]},
                           "orig_robust":    {"corr_ok":[0.0, 0], "corr_corrected":[0.0, 0], "corr_robust":[0.0, 0]}
                          },
                      "same_trees": 0,
                      "error_dist" :
                          {"orig_ok":        {"corr_ok": [0.0, 0], "corr_corrected": [0.0, 0], "corr_robust": [0.0, 0]},
                           "orig_corrected": {"corr_ok": [0.0, 0], "corr_corrected": [0.0, 0], "corr_robust": [0.0, 0]},
                           "orig_robust":    {"corr_ok": [0.0, 0], "corr_corrected": [0.0, 0], "corr_robust": [0.0, 0]}
                          },
                      "no_errors" : 0, # i.e. zero errors
                      "meltProbs":{},
                      "err_per_sent":[], # these 2 to stock info for each sentence
                      "geo_melt_prob":[],
                      "alg_melt_prob":[],
                      "weights": {
                          "orig":[],
                          "corr":[],
                        },
                      }
    parseCounts = {"orig_ok":        {"corr_ok":0, "corr_corrected":0, "corr_robust":0},
                   "orig_corrected": {"corr_ok":0, "corr_corrected":0, "corr_robust":0},
                   "orig_robust":    {"corr_ok":0, "corr_corrected":0, "corr_robust":0}
                   }
    entrycount = 0
    errorAlignments = loadJsonErrorFile(erroralignpath)
    meltScores = loadJsonMEltFile(meltorigpath, meltcorrpath)
    if os.path.isdir(path):
        for element in os.listdir(path):
            # only look at the root here
            if os.path.isfile(os.path.join(path, element)):
                entrycount += 1
                analyseFile(os.path.join(path, element), corrpath, errorAlignments, sentenceCounts, parseCounts, meltScores)
    else:
        analyseFile(path, corrpath, errorAlignments, sentenceCounts, parseCounts, meltScores)
    print "no. entries:", entrycount
    return sentenceCounts, parseCounts

def loadTokensFile( filename ):
    tokens = []
    with codecs.open(filename, mode="r", encoding="utf8") as tfile:
        for line in tfile:
            if "\t" in line:
                num, token = line.split("\t")
                tokens.append(token.strip())
    return tokens

def loadSentenceLogFile( filename ):
    errors = []
    with codecs.open(filename) as lfile:
        for line in lfile:
            if re.match(ur'\+\+\+ Success correction_anchor', line, flags=re.UNICODE):
                #print line
                correction, startpos, endpos, cat, token =\
                    re.search(ur'\+\+\+ Success correction_anchor (.+) left1=(\d+) left2=(\d+) cat=([^ ]+) token=(.+)',
                              line, flags=re.UNICODE).groups()
                errors.append( (correction, startpos, endpos, cat, token) )
                #print "correction", correction
    return errors

def loadJsonErrorFile( filename ):
    jsoncorpus = {}
    with codecs.open( filename, mode='r', encoding='utf8') as injsonfile:
        for entrynum, origtext, correctedtext, errorlist in json.load(injsonfile):
            jsoncorpus[entrynum] = (origtext, correctedtext, errorlist)

    return jsoncorpus

def loadJsonMEltFile( origfilename, corrfilename ):
    jsoncorpus = {}
    with codecs.open( origfilename, mode='r', encoding='utf8') as injsonfile:
        jsoncorpus["orig"] = json.load(injsonfile)
    with codecs.open( corrfilename, mode='r', encoding='utf8') as injsonfile:
        jsoncorpus["corr"] = json.load(injsonfile)
    return jsoncorpus

# orig and corr are 2-tuples (string, integer) corresponding to parse_info, sentence_num
def addToParseCounts(orig, corr, parseCounts, value = 1.0):
    #print orig, corr
    parseCounts["orig_"+orig[0]]["corr_"+corr[0]] += value
    if orig[0] == "robust" and corr[0] == "robust":
        print "robust/robust:", orig, corr
    if orig[0] == "ok" and corr[0] == "robust":
        print "ok/robust:", orig, corr
    if orig[0] == "corrected" and corr[0] == "robust":
        print "corrected/robust:", orig, corr
    if orig[0] == "robust" and corr[0] == "corrected":
        print "robust/corrected:", orig, corr
    if orig[0] == "ok" and corr[0] == "corrected":
        print "ok/corrected:", orig, corr
    if orig[0] == "corrected" and corr[0] == "corrected":
        print "corrected/corrected:", orig, corr

    return

'''
def getTokenFromCluster( xmlfilename, clusterLeft ): # todo change to list input and output so only open xml once
    with codecs.open(xmlfilename, mode= "r", encoding="utf8") as xmlfile:
        soup = BeautifulSoup(xmlfile)

    dep = soup.find('dependencies')
    for cluster in dep.findAll('cluster'):
        #print cluster, clusterLeft, int(cluster["left"]), int(cluster["left"]) == clusterLeft
        #if int(cluster["left"]) == clusterLeft:
        #    return cluster["token"]
        # can also be an element of a larger cluster: oddly correct d' in tout d'abbord???
        if int(cluster["left"]) <= clusterLeft and int(cluster["right"]) >= clusterLeft and \
            cluster["left"] != cluster["right"]: # can have 0 width clusters (i guess inserted at that point?)
            # E1F25|les
            #print cluster["lex"]
            tokenNumber, token = re.search(ur'E\d+F(\d+)\|(.)+$', cluster["lex"]).groups() # todo atm can only get a single token
            return cluster["token"], int(tokenNumber), token
    return None
'''
def getTokenFromCluster( xmlfilename, clusterLeft ): # todo change to list input and output so only open xml once
    #with codecs.open(xmlfilename, mode= "r", encoding="utf8") as xmlfile:
    #    soup = BeautifulSoup(xmlfile)
    tree = ET.parse(xmlfilename)

    #dep = soup.find('dependencies')
    dep = tree.getroot() # dependencies should be root
    #for cluster in dep.findAll('cluster'):
    for cluster in dep.findall('cluster'):
        #print cluster, clusterLeft, int(cluster["left"]), int(cluster["left"]) == clusterLeft
        #if int(cluster["left"]) == clusterLeft:
        #    return cluster["token"]
        # can also be an element of a larger cluster: oddly correct d' in tout d'abbord???
        #if int(cluster["left"]) <= clusterLeft and int(cluster["right"]) >= clusterLeft and \
        #    cluster["left"] != cluster["right"]: # can have 0 width clusters (i guess inserted at that point?)
        if int(cluster.get("left")) <= clusterLeft and int(cluster.get("right")) >= clusterLeft and \
            cluster.get("left") != cluster.get("right"): # can have 0 width clusters (i guess inserted at that point?)
            # E1F25|les
            #print cluster["lex"]
            #tokenNumber, token = re.search(ur'E\d+F(\d+)\|(.)+$', cluster["lex"]).groups() # todo atm can only get a single token
            tokenNumber, token = re.search(ur'E\d+F(\d+)\|(.)+$', cluster.get("lex")).groups() # todo atm can only get a single token
            #return cluster["token"], int(tokenNumber), token
            return cluster.get("token"), int(tokenNumber), token
    return None
'''
def getFinalTokenFormsAndTreesAndWeight( xmlfilename ):
    tok2finalforms = {}
    tok2lemmacats = {}
    cid2token = {}
    token2cids = {}
    cid2form = {}
    cid2lemmacat = {}
    verb2info = {}
    trees = {} # we ignore the node numbers for the moment, and store treenum : list of (cat, treeinfo) tuples, where treeinfo is a list of properties
    #  (top list covers multiple trees of same type in the parse, lower level = all the properties added
    # actually bottow list = 2 tuple (cat, []) where [] is the list of properties
    weightperword = 0
    minweight = 0
    wordsbeforemainverb = None

    verb_ds = {}
    aux_ds = {}
    #print "xml analyse:", xmlfilename

    with codecs.open(xmlfilename, mode= "r", encoding="utf8") as xmlfile:
        soup = BeautifulSoup(xmlfile) # todo should prob use etree

    dep = soup.find('dependencies')

    if dep.has_attr('nw'):
        weightperword = int(dep["nw"])

    parsemode = dep["mode"] # robust, ok, corrected

    for cluster in dep.findAll("cluster"):
        id = cluster["id"]
        #tokenStart, tokenEnd= re.search(ur'E\d+c_(\d+)_(\d+)', id, flags=re.UNICODE).groups()
        #tokenStart, tokenEnd = int(tokenStart), int(tokenEnd)
        #token = cluster["token"]
        tokenNums = re.findall(ur"E\d+F(\d+)|.+(?: $)", cluster["lex"], flags=re.UNICODE)
        #print tokenNums
        tokenNums = [int(x) for x in tokenNums if len(x)>0] # somehow gets empty string
        #for tokenNumber in range(tokenStart, tokenEnd):
        for tokenNumber in tokenNums:
            if tokenNumber not in token2cids: token2cids[tokenNumber] = []
            token2cids[tokenNumber].append(id) # we'll change the id later
            cid2token[id] = tokenNumber
    #print token2cids
    #print cid2token
    lasttokennum = max(token2cids.keys())

    for node in dep.findAll('node'):
        cluster = node["cluster"]
        form = node["form"]
        cat = node["cat"]
        lemma = node["lemma"]
        #print type(form)
        #print form
        #print unicode(form)
        if type(form) != 'unicode': # soup returns a str if it can, a unicode otherwise
            form = unicode(form)
        if type(cat) != 'unicode': # soup returns a str if it can, a unicode otherwise
            cat = unicode(cat)
        if type(lemma) != 'unicode': # soup returns a str if it can, a unicode otherwise
            lemma = unicode(lemma)
        #print type(form)
        cid2form[cluster] = form
        cid2lemmacat[cluster] = (lemma, cat)

        treenum = node["tree"]
        treeinfo = ""
        if " " in treenum:
            treenum, treeinfo = node["tree"].split(' ',1)
        # for the moment we take just 'cat', not 'xcat'=parent?
        # treenum can be an integer or an id label "follow_coord" (for higher level trees?)
        try:
            treenum = int(treenum)
        except:
            pass
        treeinfo = treeinfo.split()
        cat = node["cat"]
        if treenum not in trees: trees[treenum] = []
        trees[treenum].append( (cat, treeinfo) )

        if cat == "v":
            if node.has_attr("deriv"):
                verb_ds[node["deriv"]] = (lemma, cluster)
            else:
                # robust analysis and no interpretation
                pass
        if cat == "aux":
            if node.has_attr("deriv"):
                aux_ds[node["deriv"]] = (lemma, cluster)
            else:
                # robust analysis and no interpretation
                pass



    #print cid2form
    #for a in cid2form: print type(cid2form[a])

    for tokenNum in token2cids:
        clusters = token2cids[tokenNum]
        # put clusters in order: (by their start point
        clusters = sorted(clusters,
                          key= lambda x: int(re.search(ur'^E\d+c_(\d+)_\d+', x, flags=re.UNICODE).groups()[0]))
        #print type(clusters[0])
        #print clusters[0]
        #print unicode(clusters[0])
        tok2finalforms[tokenNum] = [cid2form[x] for x in clusters]
        tok2lemmacats[tokenNum] = [cid2lemmacat[x] for x in clusters]

    for edge in dep.findAll('edge'):
        if edge.has_attr('w'):
            minweight = min(minweight, int(edge["w"]))

    maxspan = -1
    #print "verb ds", verb_ds
    for op in dep.findAll('op'):
        if op["deriv"] in verb_ds and op["cat"] == "S": # need S for gerundive ...

            # check if it is the main verb in the sentence:
            span = op["span"]
            # the span will have an even number of entries (2, 4 etc.) separated by a space,
            # we are looking for a span from 0 to end of sentence with no gaps in between:
            spansplit = span.split(" ")
            #print "span splitish", spansplit
            if len(spansplit) == 2:
                spanstart, spanend = int(spansplit[0]), int(spansplit[1])
                #print "span split", spanstart, spanend
                if parsemode == "robust":

                    # take the first verb
                    lemma, cluster = verb_ds[op["deriv"]]
                    position = cid2token[cluster] - 1
                    if wordsbeforemainverb is None: wordsbeforemainverb = 100000 # hopefully longer than any sentence we'll encounter!
                    if position < wordsbeforemainverb:
                        wordsbeforemainverb = position
                else:
                    if spanend - spanstart > maxspan:
                        maxspan = spanend-spanstart
                        #if spansplit[0] == 0 and spansplit[1] == 1 + lasttokennum:
                        lemma, cluster = verb_ds[op["deriv"]]
                        wordsbeforemainverb = cid2token[cluster] - 1

            verbinfos = []
            for narg in op.findAll('narg'):
                verbinfo = {}
                changetoinfintive = False
                for f in narg.findAll('f'):

                    if f["name"] in ["mode", "tense", "control", "extraction", "sat"]:
                        tmp = []
                        if not f.find("minus"):
                            for val in f.findAll('val'):
                                if len(val.text.strip()) > 0:
                                    #    and val.text.strip() not in ["sg", "fem", "3", "pl", "masc", "present", "infinitive", "indicative", "imperfect", "subjonctive", "cl", "1", "2" "rel", "acc" ]:
                                    #print val.text.strip()
                                    tmp.append(val.text.strip())
                                    #print narg
                                    #x = "case", "extraction", "sat", "lex" # don't need enum
                            if len(tmp) > 1:
                                # we need to disambiguate:
                                if "indicative" in tmp and "subjonctive" in tmp:
                                    if "conditional" in tmp:
                                        tmp = ["infinitive"] # something weird going on
                                        print "weird situation"
                                    else:
                                        tmp = ["indicative"] # (assume indicative)
                                elif "present" in tmp and "past-historic" in tmp:
                                    tmp = ["present"]
                                elif "adjx" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "cleft" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "causative" in tmp:
                                    tmp = ["causative"] # assume causative dominates
                                else:
                                    print "ambig1", tmp
                            #verbinfo.extend(tmp)
                            if len(tmp) > 0:
                                verbinfo[f["name"]]= tmp[0]
                    elif f["name"] == "xarg":
                        miniverbinfo = []
                        for fs in f.findAll('fs'):
                            for f2 in fs.findAll('f'): # "case", "lex"
                                if f2["name"] not in ["gender", "number"]:
                                    for val2 in f2.findAll('val'):
                                        #print "inner:", f2["name"], val2.text.strip()
                                        miniverbinfo.append(val2.text.strip())
                        if len(miniverbinfo) > 0:
                            verbinfo[f["name"]] = "_".join(miniverbinfo)
                            #print "adding mini", miniverbinfo, f["name"], op["deriv"]
                        #else:
                        #    if len(val.text.strip()) > 0 and val.text.strip() not in ['sg', 'pl', 'fem', '3', '2', '1', 'masc']:
                        #        print val.text.strip()
                if len(verbinfo) > 0:
                    if changetoinfintive:
                        verbinfos.append(["infinitive"]+verbinfo[1:])
                    else:
                         verbinfos.append(verbinfo)
            #print verbinfos
            verb, cluster = verb_ds[op["deriv"]]
            verb2info[verb] = verbinfos
            #print "verb S", verb, verbinfos
        if op["deriv"] in verb_ds and op["cat"] == "V": # need S for gerundive ...
            verbinfos = []
            for narg in op.findAll('narg'):
                verbinfo = {}
                for f in narg.findAll('f'):

                    if f["name"] in ["mode", "tense", "control", "extraction", "sat"]:
                        tmp = []
                        if not f.find("minus"):
                            for val in f.findAll('val'):
                                if len(val.text.strip()) > 0:
                                    #    and val.text.strip() not in ["sg", "fem", "3", "pl", "masc", "present", "infinitive", "indicative", "imperfect", "subjonctive", "cl", "1", "2" "rel", "acc" ]:
                                    #print val.text.strip()
                                    # not interesting: aux_req
                                    tmp.append(val.text.strip())
                            if len(tmp) > 1:
                                # we need to disambiguate:
                                if "indicative" in tmp and "subjonctive" in tmp:
                                    if "conditional" in tmp:
                                        tmp = ["infinitive"] # something weird going on
                                        print "weird situation"
                                    else:
                                        tmp = ["indicative"] # (assume indicative)
                                elif "present" in tmp and "past-historic" in tmp:
                                    tmp = ["present"]
                                elif "adjx" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "cleft" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "causative" in tmp:
                                    tmp = ["causative"] # assume causative dominates
                                else:
                                    print "ambig2", tmp
                            if len(tmp) > 0:
                                verbinfo[f["name"]]= tmp[0]
                    elif f["name"] == "xarg":
                        miniverbinfo = []
                        for fs in f.findAll('fs'):
                            for f2 in fs.findAll('f'):
                                if f2["name"] not in ["gender", "number"]:
                                    for val2 in f2.findAll('val'):
                                        #print "inner:", val2.text.strip()
                                        miniverbinfo.append(val2.text.strip())
                        if len(miniverbinfo) > 0:
                            verbinfo[f["name"]] = "_".join(miniverbinfo)
                        #else:
                        #    if len(val.text.strip()) > 0 and val.text.strip() not in ['sg', 'pl', 'fem', '3', '2', '1', 'masc']:
                        #        print val.text.strip()
                if len(verbinfo) > 0: verbinfos.append(verbinfo)
            #print verbinfos
            verb, cluster = verb_ds[op["deriv"]]
            verb2info[verb] = verbinfos
            #print "verb V", verb, verbinfos
        if op["deriv"] in aux_ds and op["cat"] == "Infl":
            verbinfos = []
            for narg in op.findAll('narg'): # each narg will be a new verb, second one won't be that linked?
                verbinfo = {}
                for f in narg.findAll('f'):
                    if f["name"] in ["mode", "tense", "control", "extraction", "sat"]:
                        tmp = []
                        if not f.find("minus"):
                            for val in f.findAll('val'):
                                if len(val.text.strip()) > 0:

                                    #    and val.text.strip() not in ["sg", "fem", "3", "pl", "masc", "present", "infinitive", "indicative", "imperfect", "subjonctive", "cl", "1", "2" "rel", "acc" ]:
                                    #print val.text.strip()
                                    tmp.append(val.text.strip())
                            if len(tmp) > 1:
                                # we need to disambiguate:
                                if "indicative" in tmp and "subjonctive" in tmp:
                                    if "conditional" in tmp:
                                        tmp = ["infinitive"] # something weird going on
                                        print "weird situation"
                                    else:
                                        tmp = ["indicative"] # (assume indicative)
                                elif "present" in tmp and "past-historic" in tmp:
                                    tmp = ["present"]
                                elif "adjx" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "cleft" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "causative" in tmp:
                                    tmp = ["causative"] # assume causative dominates
                                else:
                                    print "ambig3", tmp
                            if len(tmp) > 0:
                                verbinfo[f["name"]]= tmp[0]
                    elif f["name"] == "xarg":
                        miniverbinfo = []
                        for fs in f.findAll('fs'):
                            for f2 in fs.findAll('f'):
                                if f2["name"] not in ["gender", "number"]:
                                    for val2 in f2.findAll('val'):
                                        #print "inner:", val2.text.strip()
                                        miniverbinfo.append(val2.text.strip())
                        if len(miniverbinfo) > 0:
                            verbinfo[f["name"]] = "_".join(miniverbinfo)
                        #else:
                        #    if len(val.text.strip()) > 0 and val.text.strip() not in ['sg', 'pl', 'fem', '3', '2', '1', 'masc']:
                        #        print val.text.strip()
                if len(verbinfo) > 0: verbinfos.append(verbinfo)
            aux, cluster = aux_ds[op["deriv"]]
            verb2info[aux] = verbinfos
            #print "aux", aux, verbinfos
    #print verb2info
    #print "final type: ", type(tok2finalforms[1][0])
    #exit(10)
    if wordsbeforemainverb is None:
        # there is no verb:
        wordsbeforemainverb = -1
    #print "words before main verb", wordsbeforemainverb
    #exit(10)

    return tok2finalforms, tok2lemmacats, verb2info, trees, (weightperword, minweight), wordsbeforemainverb
'''
def getFinalTokenFormsAndTreesAndWeight( xmlfilename ):
    tok2finalforms = {}
    tok2lemmacats = {}
    cid2token = {}
    token2cids = {}
    cid2form = {}
    cid2lemmacat = {}
    verb2info = {}
    trees = {} # we ignore the node numbers for the moment, and store treenum : list of (cat, treeinfo) tuples, where treeinfo is a list of properties
    #  (top list covers multiple trees of same type in the parse, lower level = all the properties added
    # actually bottow list = 2 tuple (cat, []) where [] is the list of properties
    weightperword = 0
    minweight = 0
    wordsbeforemainverb = None

    verb_ds = {}
    aux_ds = {}
    #print "xml analyse:", xmlfilename

    #with codecs.open(xmlfilename, mode= "r", encoding="utf8") as xmlfile:
    #    soup = BeautifulSoup(xmlfile) # todo should prob use etree

    #dep = soup.find('dependencies')
    tree = ET.parse(xmlfilename)

    #dep = soup.find('dependencies')
    dep = tree.getroot() # dependencies should be root


    #if dep.has_attr('nw'):
    if 'nw' in dep.attrib:
        #weightperword = int(dep["nw"])
        weightperword = int(dep.get("nw"))

    #parsemode = dep["mode"] # robust, ok, corrected
    parsemode = dep.get("mode") # robust, ok, corrected

    #for cluster in dep.findAll("cluster"):
    for cluster in dep.findall("cluster"):
        #id = cluster["id"]
        id = cluster.get("id")
        #tokenStart, tokenEnd= re.search(ur'E\d+c_(\d+)_(\d+)', id, flags=re.UNICODE).groups()
        #tokenStart, tokenEnd = int(tokenStart), int(tokenEnd)
        #token = cluster["token"]
        #tokenNums = re.findall(ur"E\d+F(\d+)|.+(?: $)", cluster["lex"], flags=re.UNICODE)
        tokenNums = re.findall(ur"E\d+F(\d+)|.+(?: $)", cluster.get("lex"), flags=re.UNICODE)
        #print tokenNums
        tokenNums = [int(x) for x in tokenNums if len(x)>0] # somehow gets empty string
        #for tokenNumber in range(tokenStart, tokenEnd):
        for tokenNumber in tokenNums:
            if tokenNumber not in token2cids: token2cids[tokenNumber] = []
            token2cids[tokenNumber].append(id) # we'll change the id later
            cid2token[id] = tokenNumber
    #print token2cids
    #print cid2token
    lasttokennum = max(token2cids.keys())

    #for node in dep.findAll('node'):
    for node in dep.findall('node'):
        #cluster = node["cluster"]
        #form = node["form"]
        #cat = node["cat"]
        #lemma = node["lemma"]
        cluster = node.get("cluster")
        form = node.get("form")
        cat = node.get("cat")
        lemma = node.get("lemma")
        #print type(form)
        #print form
        #print unicode(form)
        if type(form) != 'unicode': # soup returns a str if it can, a unicode otherwise
            form = unicode(form)
        if type(cat) != 'unicode': # soup returns a str if it can, a unicode otherwise
            cat = unicode(cat)
        if type(lemma) != 'unicode': # soup returns a str if it can, a unicode otherwise
            lemma = unicode(lemma)
        #print type(form)
        cid2form[cluster] = form
        cid2lemmacat[cluster] = (lemma, cat)

        #treenum = node["tree"]
        treenum = node.get("tree")
        treeinfo = ""
        if " " in treenum:
            #treenum, treeinfo = node["tree"].split(' ',1)
            treenum, treeinfo = node.get("tree").split(' ',1)
        # for the moment we take just 'cat', not 'xcat'=parent?
        # treenum can be an integer or an id label "follow_coord" (for higher level trees?)
        try:
            treenum = int(treenum)
        except:
            pass
        treeinfo = treeinfo.split()
        #cat = node["cat"]
        cat = node.get("cat")
        if treenum not in trees: trees[treenum] = []
        trees[treenum].append( (cat, treeinfo) )

        if cat == "v":
            #if node.has_attr("deriv"):
            if "deriv" in node.attrib:
                #verb_ds[node["deriv"]] = (lemma, cluster)
                verb_ds[node.get("deriv")] = (lemma, cluster)
            else:
                # robust analysis and no interpretation
                pass
        if cat == "aux":
            #if node.has_attr("deriv"):
            if "deriv" in node.attrib:
                #aux_ds[node["deriv"]] = (lemma, cluster)
                aux_ds[node.get("deriv")] = (lemma, cluster)
            else:
                # robust analysis and no interpretation
                pass



    #print cid2form
    #for a in cid2form: print type(cid2form[a])

    for tokenNum in token2cids:
        clusters = token2cids[tokenNum]
        # put clusters in order: (by their start point
        clusters = sorted(clusters,
                          key= lambda x: int(re.search(ur'^E\d+c_(\d+)_\d+', x, flags=re.UNICODE).groups()[0]))
        #print type(clusters[0])
        #print clusters[0]
        #print unicode(clusters[0])
        tok2finalforms[tokenNum] = [cid2form[x] for x in clusters]
        tok2lemmacats[tokenNum] = [cid2lemmacat[x] for x in clusters]

    #for edge in dep.findAll('edge'):
    for edge in dep.findall('edge'):
        #if edge.has_attr('w'):
        if 'w' in edge.attrib:
            #minweight = min(minweight, int(edge["w"]))
            minweight = min(minweight, int(edge.get("w")))

    maxspan = -1
    #print "verb ds", verb_ds
    #for op in dep.findAll('op'):
    for op in dep.findall('op'):
        #if op["deriv"] in verb_ds and op["cat"] == "S": # need S for gerundive ...
        if op.get("deriv") in verb_ds and op.get("cat") == "S": # need S for gerundive ...

            # check if it is the main verb in the sentence:
            #span = op["span"]
            span = op.get("span")
            # the span will have an even number of entries (2, 4 etc.) separated by a space,
            # we are looking for a span from 0 to end of sentence with no gaps in between:
            spansplit = span.split(" ")
            #print "span splitish", spansplit
            if len(spansplit) == 2:
                spanstart, spanend = int(spansplit[0]), int(spansplit[1])
                #print "span split", spanstart, spanend
                if parsemode == "robust":

                    # take the first verb
                    #lemma, cluster = verb_ds[op["deriv"]]
                    lemma, cluster = verb_ds[op.get("deriv")]
                    position = cid2token[cluster] - 1
                    if wordsbeforemainverb is None: wordsbeforemainverb = 100000 # hopefully longer than any sentence we'll encounter!
                    if position < wordsbeforemainverb:
                        wordsbeforemainverb = position
                else:
                    if spanend - spanstart > maxspan:
                        maxspan = spanend-spanstart
                        #if spansplit[0] == 0 and spansplit[1] == 1 + lasttokennum:
                        #lemma, cluster = verb_ds[op["deriv"]]
                        lemma, cluster = verb_ds[op.get("deriv")]
                        wordsbeforemainverb = cid2token[cluster] - 1

            verbinfos = []
            #for narg in op.findAll('narg'):
            for narg in op.findall('narg'):
                verbinfo = {}
                changetoinfintive = False
                #for f in narg.findAll('f'):
                for f in narg.findall('f'):

                    #if f["name"] in ["mode", "tense", "control", "extraction", "sat"]:
                    if f.get("name") in ["mode", "tense", "control", "extraction", "sat"]:
                        tmp = []
                        if not f.find("minus"):
                            #for val in f.findAll('val'):
                            for val in f.findall('val'):
                                if len(val.text.strip()) > 0:
                                    #    and val.text.strip() not in ["sg", "fem", "3", "pl", "masc", "present", "infinitive", "indicative", "imperfect", "subjonctive", "cl", "1", "2" "rel", "acc" ]:
                                    #print val.text.strip()
                                    tmp.append(val.text.strip())
                                    #print narg
                                    #x = "case", "extraction", "sat", "lex" # don't need enum
                            if len(tmp) > 1:
                                # we need to disambiguate:
                                if "indicative" in tmp and "subjonctive" in tmp:
                                    if "conditional" in tmp:
                                        tmp = ["infinitive"] # something weird going on
                                        print "weird situation"
                                    else:
                                        tmp = ["indicative"] # (assume indicative)
                                elif "present" in tmp and "past-historic" in tmp:
                                    tmp = ["present"]
                                elif "adjx" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "cleft" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "causative" in tmp:
                                    tmp = ["causative"] # assume causative dominates
                                else:
                                    print "ambig1", tmp
                            #verbinfo.extend(tmp)
                            if len(tmp) > 0:
                                #verbinfo[f["name"]]= tmp[0]
                                verbinfo[f.get("name")]= tmp[0]
                    elif f["name"] == "xarg":
                        miniverbinfo = []
                        #for fs in f.findAll('fs'):
                        for fs in f.findall('fs'):
                            #for f2 in fs.findAll('f'): # "case", "lex"
                            for f2 in fs.findall('f'): # "case", "lex"
                                #if f2["name"] not in ["gender", "number"]:
                                if f2.get("name") not in ["gender", "number"]:
                                    #for val2 in f2.findAll('val'):
                                    for val2 in f2.findall('val'):
                                        #print "inner:", f2["name"], val2.text.strip()
                                        miniverbinfo.append(val2.text.strip())
                        if len(miniverbinfo) > 0:
                            #verbinfo[f["name"]] = "_".join(miniverbinfo)
                            verbinfo[f.get("name")] = "_".join(miniverbinfo)
                            #print "adding mini", miniverbinfo, f["name"], op["deriv"]
                        #else:
                        #    if len(val.text.strip()) > 0 and val.text.strip() not in ['sg', 'pl', 'fem', '3', '2', '1', 'masc']:
                        #        print val.text.strip()
                    '''
                    if f["name"] == "mode":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            verbinfo.append(val.text.strip())
                    if f["name"] == "tense":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            verbinfo.append(val.text.strip())
                    if f["name"] == "control":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            print "control", val.text.strip()
                            changetoinfintive = True
                    '''
                if len(verbinfo) > 0:
                    if changetoinfintive:
                        verbinfos.append(["infinitive"]+verbinfo[1:])
                    else:
                         verbinfos.append(verbinfo)
            #print verbinfos
            #verb, cluster = verb_ds[op["deriv"]]
            verb, cluster = verb_ds[op.get("deriv")]
            verb2info[verb] = verbinfos
            #print "verb S", verb, verbinfos
        #if op["deriv"] in verb_ds and op["cat"] == "V": # need S for gerundive ...
        if op.get("deriv") in verb_ds and op.get("cat") == "V": # need S for gerundive ...
            verbinfos = []
            #for narg in op.findAll('narg'):
            for narg in op.findall('narg'):
                verbinfo = {}
                #for f in narg.findAll('f'):
                for f in narg.findall('f'):

                    #if f["name"] in ["mode", "tense", "control", "extraction", "sat"]:
                    if f.get("name") in ["mode", "tense", "control", "extraction", "sat"]:
                        tmp = []
                        if not f.find("minus"):
                            #for val in f.findAll('val'):
                            for val in f.findall('val'):
                                if len(val.text.strip()) > 0:
                                    #    and val.text.strip() not in ["sg", "fem", "3", "pl", "masc", "present", "infinitive", "indicative", "imperfect", "subjonctive", "cl", "1", "2" "rel", "acc" ]:
                                    #print val.text.strip()
                                    # not interesting: aux_req
                                    tmp.append(val.text.strip())
                            if len(tmp) > 1:
                                # we need to disambiguate:
                                if "indicative" in tmp and "subjonctive" in tmp:
                                    if "conditional" in tmp:
                                        tmp = ["infinitive"] # something weird going on
                                        print "weird situation"
                                    else:
                                        tmp = ["indicative"] # (assume indicative)
                                elif "present" in tmp and "past-historic" in tmp:
                                    tmp = ["present"]
                                elif "adjx" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "cleft" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "causative" in tmp:
                                    tmp = ["causative"] # assume causative dominates
                                else:
                                    print "ambig2", tmp
                            if len(tmp) > 0:
                                verbinfo[f["name"]]= tmp[0]
                    #elif f["name"] == "xarg":
                    elif f.get("name") == "xarg":
                        miniverbinfo = []
                        #for fs in f.findAll('fs'):
                        for fs in f.findall('fs'):
                            #for f2 in fs.findAll('f'):
                            for f2 in fs.findall('f'):
                                #if f2["name"] not in ["gender", "number"]:
                                if f2.get("name") not in ["gender", "number"]:
                                    #for val2 in f2.findAll('val'):
                                    for val2 in f2.findall('val'):
                                        #print "inner:", val2.text.strip()
                                        miniverbinfo.append(val2.text.strip())
                        if len(miniverbinfo) > 0:
                            #verbinfo[f["name"]] = "_".join(miniverbinfo)
                            verbinfo[f.get("name")] = "_".join(miniverbinfo)
                        #else:
                        #    if len(val.text.strip()) > 0 and val.text.strip() not in ['sg', 'pl', 'fem', '3', '2', '1', 'masc']:
                        #        print val.text.strip()
                    '''
                    if f["name"] == "mode":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            verbinfo.append(val.text.strip())
                    if f["name"] == "tense":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            verbinfo.append(val.text.strip())def getFinalTokenFormsAndTreesAndWeight( xmlfilename ):
    tok2finalforms = {}
    tok2lemmacats = {}
    cid2token = {}
    token2cids = {}
    cid2form = {}
    cid2lemmacat = {}
    verb2info = {}
    trees = {} # we ignore the node numbers for the moment, and store treenum : list of (cat, treeinfo) tuples, where treeinfo is a list of properties
    #  (top list covers multiple trees of same type in the parse, lower level = all the properties added
    # actually bottow list = 2 tuple (cat, []) where [] is the list of properties
    weightperword = 0
    minweight = 0
    wordsbeforemainverb = None

    verb_ds = {}
    aux_ds = {}
    #print "xml analyse:", xmlfilename

    #with codecs.open(xmlfilename, mode= "r", encoding="utf8") as xmlfile:
    #    soup = BeautifulSoup(xmlfile) # todo should prob use etree

    #dep = soup.find('dependencies')
    tree = ET.parse(xmlfilename)

    #dep = soup.find('dependencies')
    dep = tree.getroot() # dependencies should be root


    #if dep.has_attr('nw'):
    if 'nw' in dep.attrib:
        #weightperword = int(dep["nw"])
        weightperword = int(dep.get("nw"))

    #parsemode = dep["mode"] # robust, ok, corrected
    parsemode = dep.get("mode") # robust, ok, corrected

    #for cluster in dep.findAll("cluster"):
    for cluster in dep.findall("cluster"):
        #id = cluster["id"]
        id = cluster.get("id")
        #tokenStart, tokenEnd= re.search(ur'E\d+c_(\d+)_(\d+)', id, flags=re.UNICODE).groups()
        #tokenStart, tokenEnd = int(tokenStart), int(tokenEnd)
        #token = cluster["token"]
        #tokenNums = re.findall(ur"E\d+F(\d+)|.+(?: $)", cluster["lex"], flags=re.UNICODE)
        tokenNums = re.findall(ur"E\d+F(\d+)|.+(?: $)", cluster.get("lex"), flags=re.UNICODE)
        #print tokenNums
        tokenNums = [int(x) for x in tokenNums if len(x)>0] # somehow gets empty string
        #for tokenNumber in range(tokenStart, tokenEnd):
        for tokenNumber in tokenNums:
            if tokenNumber not in token2cids: token2cids[tokenNumber] = []
            token2cids[tokenNumber].append(id) # we'll change the id later
            cid2token[id] = tokenNumber
    #print token2cids
    #print cid2token
    lasttokennum = max(token2cids.keys())

    #for node in dep.findAll('node'):
    for node in dep.findall('node'):
        #cluster = node["cluster"]
        #form = node["form"]
        #cat = node["cat"]
        #lemma = node["lemma"]
        cluster = node.get("cluster")
        form = node.get("form")
        cat = node.get("cat")
        lemma = node.get("lemma")
        #print type(form)
        #print form
        #print unicode(form)
        if type(form) != 'unicode': # soup returns a str if it can, a unicode otherwise
            form = unicode(form)
        if type(cat) != 'unicode': # soup returns a str if it can, a unicode otherwise
            cat = unicode(cat)
        if type(lemma) != 'unicode': # soup returns a str if it can, a unicode otherwise
            lemma = unicode(lemma)
        #print type(form)
        cid2form[cluster] = form
        cid2lemmacat[cluster] = (lemma, cat)

        #treenum = node["tree"]
        treenum = node.get("tree")
        treeinfo = ""
        if " " in treenum:
            #treenum, treeinfo = node["tree"].split(' ',1)
            treenum, treeinfo = node.get("tree").split(' ',1)
        # for the moment we take just 'cat', not 'xcat'=parent?
        # treenum can be an integer or an id label "follow_coord" (for higher level trees?)
        try:
            treenum = int(treenum)
        except:
            pass
        treeinfo = treeinfo.split()
        #cat = node["cat"]
        cat = node.get("cat")
        if treenum not in trees: trees[treenum] = []
        trees[treenum].append( (cat, treeinfo) )

        if cat == "v":
            #if node.has_attr("deriv"):
            if "deriv" in node.attrib:
                #verb_ds[node["deriv"]] = (lemma, cluster)
                verb_ds[node.get("deriv")] = (lemma, cluster)
            else:
                # robust analysis and no interpretation
                pass
        if cat == "aux":
            #if node.has_attr("deriv"):
            if "deriv" in node.attrib:
                #aux_ds[node["deriv"]] = (lemma, cluster)
                aux_ds[node.get("deriv")] = (lemma, cluster)
            else:
                # robust analysis and no interpretation
                pass



    #print cid2form
    #for a in cid2form: print type(cid2form[a])

    for tokenNum in token2cids:
        clusters = token2cids[tokenNum]
        # put clusters in order: (by their start point
        clusters = sorted(clusters,
                          key= lambda x: int(re.search(ur'^E\d+c_(\d+)_\d+', x, flags=re.UNICODE).groups()[0]))
        #print type(clusters[0])
        #print clusters[0]
        #print unicode(clusters[0])
        tok2finalforms[tokenNum] = [cid2form[x] for x in clusters]
        tok2lemmacats[tokenNum] = [cid2lemmacat[x] for x in clusters]

    #for edge in dep.findAll('edge'):
    for edge in dep.findall('edge'):
        #if edge.has_attr('w'):
        if 'w' in edge.attrib:
            #minweight = min(minweight, int(edge["w"]))
            minweight = min(minweight, int(edge.get("w")))

    maxspan = -1
    #print "verb ds", verb_ds
    #for op in dep.findAll('op'):
    for op in dep.findall('op'):
        #if op["deriv"] in verb_ds and op["cat"] == "S": # need S for gerundive ...
        if op.get("deriv") in verb_ds and op.get("cat") == "S": # need S for gerundive ...

            # check if it is the main verb in the sentence:
            #span = op["span"]
            span = op.get("span")
            # the span will have an even number of entries (2, 4 etc.) separated by a space,
            # we are looking for a span from 0 to end of sentence with no gaps in between:
            spansplit = span.split(" ")
            #print "span splitish", spansplit
            if len(spansplit) == 2:
                spanstart, spanend = int(spansplit[0]), int(spansplit[1])
                #print "span split", spanstart, spanend
                if parsemode == "robust":

                    # take the first verb
                    #lemma, cluster = verb_ds[op["deriv"]]
                    lemma, cluster = verb_ds[op.get("deriv")]
                    position = cid2token[cluster] - 1
                    if wordsbeforemainverb is None: wordsbeforemainverb = 100000 # hopefully longer than any sentence we'll encounter!
                    if position < wordsbeforemainverb:
                        wordsbeforemainverb = position
                else:
                    if spanend - spanstart > maxspan:
                        maxspan = spanend-spanstart
                        #if spansplit[0] == 0 and spansplit[1] == 1 + lasttokennum:
                        #lemma, cluster = verb_ds[op["deriv"]]
                        lemma, cluster = verb_ds[op.get("deriv")]
                        wordsbeforemainverb = cid2token[cluster] - 1

            verbinfos = []
            #for narg in op.findAll('narg'):
            for narg in op.findall('narg'):
                verbinfo = {}
                changetoinfintive = False
                #for f in narg.findAll('f'):
                for f in narg.findall('f'):

                    #if f["name"] in ["mode", "tense", "control", "extraction", "sat"]:
                    if f.get("name") in ["mode", "tense", "control", "extraction", "sat"]:
                        tmp = []
                        if not f.find("minus"):
                            #for val in f.findAll('val'):
                            for val in f.findall('val'):
                                if len(val.text.strip()) > 0:
                                    #    and val.text.strip() not in ["sg", "fem", "3", "pl", "masc", "present", "infinitive", "indicative", "imperfect", "subjonctive", "cl", "1", "2" "rel", "acc" ]:
                                    #print val.text.strip()
                                    tmp.append(val.text.strip())
                                    #print narg
                                    #x = "case", "extraction", "sat", "lex" # don't need enum
                            if len(tmp) > 1:
                                # we need to disambiguate:
                                if "indicative" in tmp and "subjonctive" in tmp:
                                    if "conditional" in tmp:
                                        tmp = ["infinitive"] # something weird going on
                                        print "weird situation"
                                    else:
                                        tmp = ["indicative"] # (assume indicative)
                                elif "present" in tmp and "past-historic" in tmp:
                                    tmp = ["present"]
                                elif "adjx" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "cleft" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "causative" in tmp:
                                    tmp = ["causative"] # assume causative dominates
                                else:
                                    print "ambig1", tmp
                            #verbinfo.extend(tmp)
                            if len(tmp) > 0:
                                #verbinfo[f["name"]]= tmp[0]
                                verbinfo[f.get("name")]= tmp[0]
                    elif f["name"] == "xarg":
                        miniverbinfo = []
                        #for fs in f.findAll('fs'):
                        for fs in f.findall('fs'):
                            #for f2 in fs.findAll('f'): # "case", "lex"
                            for f2 in fs.findall('f'): # "case", "lex"
                                #if f2["name"] not in ["gender", "number"]:
                                if f2.get("name") not in ["gender", "number"]:
                                    #for val2 in f2.findAll('val'):
                                    for val2 in f2.findall('val'):
                                        #print "inner:", f2["name"], val2.text.strip()
                                        miniverbinfo.append(val2.text.strip())
                        if len(miniverbinfo) > 0:
                            #verbinfo[f["name"]] = "_".join(miniverbinfo)
                            verbinfo[f.get("name")] = "_".join(miniverbinfo)
                            #print "adding mini", miniverbinfo, f["name"], op["deriv"]
                        #else:
                        #    if len(val.text.strip()) > 0 and val.text.strip() not in ['sg', 'pl', 'fem', '3', '2', '1', 'masc']:
                        #        print val.text.strip()
                    '''
                    if f["name"] == "mode":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            verbinfo.append(val.text.strip())
                    if f["name"] == "tense":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            verbinfo.append(val.text.strip())
                    if f["name"] == "control":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            print "control", val.text.strip()
                            changetoinfintive = True
                    '''
                if len(verbinfo) > 0:
                    if changetoinfintive:
                        verbinfos.append(["infinitive"]+verbinfo[1:])
                    else:
                         verbinfos.append(verbinfo)
            #print verbinfos
            #verb, cluster = verb_ds[op["deriv"]]
            verb, cluster = verb_ds[op.get("deriv")]
            verb2info[verb] = verbinfos
            #print "verb S", verb, verbinfos
        #if op["deriv"] in verb_ds and op["cat"] == "V": # need S for gerundive ...
        if op.get("deriv") in verb_ds and op.get("cat") == "V": # need S for gerundive ...
            verbinfos = []
            #for narg in op.findAll('narg'):
            for narg in op.findall('narg'):
                verbinfo = {}
                #for f in narg.findAll('f'):
                for f in narg.findall('f'):

                    #if f["name"] in ["mode", "tense", "control", "extraction", "sat"]:
                    if f.get("name") in ["mode", "tense", "control", "extraction", "sat"]:
                        tmp = []
                        if not f.find("minus"):
                            #for val in f.findAll('val'):
                            for val in f.findall('val'):
                                if len(val.text.strip()) > 0:
                                    #    and val.text.strip() not in ["sg", "fem", "3", "pl", "masc", "present", "infinitive", "indicative", "imperfect", "subjonctive", "cl", "1", "2" "rel", "acc" ]:
                                    #print val.text.strip()
                                    # not interesting: aux_req
                                    tmp.append(val.text.strip())
                            if len(tmp) > 1:
                                # we need to disambiguate:
                                if "indicative" in tmp and "subjonctive" in tmp:
                                    if "conditional" in tmp:
                                        tmp = ["infinitive"] # something weird going on
                                        print "weird situation"
                                    else:
                                        tmp = ["indicative"] # (assume indicative)
                                elif "present" in tmp and "past-historic" in tmp:
                                    tmp = ["present"]
                                elif "adjx" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "cleft" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "causative" in tmp:
                                    tmp = ["causative"] # assume causative dominates
                                else:
                                    print "ambig2", tmp
                            if len(tmp) > 0:
                                verbinfo[f["name"]]= tmp[0]
                    #elif f["name"] == "xarg":
                    elif f.get("name") == "xarg":
                        miniverbinfo = []
                        #for fs in f.findAll('fs'):
                        for fs in f.findall('fs'):
                            #for f2 in fs.findAll('f'):
                            for f2 in fs.findall('f'):
                                #if f2["name"] not in ["gender", "number"]:
                                if f2.get("name") not in ["gender", "number"]:
                                    #for val2 in f2.findAll('val'):
                                    for val2 in f2.findall('val'):
                                        #print "inner:", val2.text.strip()
                                        miniverbinfo.append(val2.text.strip())
                        if len(miniverbinfo) > 0:
                            #verbinfo[f["name"]] = "_".join(miniverbinfo)
                            verbinfo[f.get("name")] = "_".join(miniverbinfo)
                        #else:
                        #    if len(val.text.strip()) > 0 and val.text.strip() not in ['sg', 'pl', 'fem', '3', '2', '1', 'masc']:
                        #        print val.text.strip()
                    '''
                    if f["name"] == "mode":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            verbinfo.append(val.text.strip())
                    if f["name"] == "tense":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            verbinfo.append(val.text.strip())
                    '''
                if len(verbinfo) > 0: verbinfos.append(verbinfo)
            #print verbinfos
            #verb, cluster = verb_ds[op["deriv"]]
            verb, cluster = verb_ds[op.get("deriv")]
            verb2info[verb] = verbinfos
            #print "verb V", verb, verbinfos
        #if op["deriv"] in aux_ds and op["cat"] == "Infl":
        if op.get("deriv") in aux_ds and op.get("cat") == "Infl":
            verbinfos = []
            #for narg in op.findAll('narg'): # each narg will be a new verb, second one won't be that linked?
            for narg in op.findall('narg'): # each narg will be a new verb, second one won't be that linked?
                verbinfo = {}
                #for f in narg.findAll('f'):
                for f in narg.findall('f'):
                    #if f["name"] in ["mode", "tense", "control", "extraction", "sat"]:
                    if f.get("name") in ["mode", "tense", "control", "extraction", "sat"]:
                        tmp = []
                        if not f.find("minus"):
                            #for val in f.findAll('val'):
                            for val in f.findall('val'):
                                if len(val.text.strip()) > 0:

                                    #    and val.text.strip() not in ["sg", "fem", "3", "pl", "masc", "present", "infinitive", "indicative", "imperfect", "subjonctive", "cl", "1", "2" "rel", "acc" ]:
                                    #print val.text.strip()
                                    tmp.append(val.text.strip())
                            if len(tmp) > 1:
                                # we need to disambiguate:
                                if "indicative" in tmp and "subjonctive" in tmp:
                                    if "conditional" in tmp:
                                        tmp = ["infinitive"] # something weird going on
                                        print "weird situation"
                                    else:
                                        tmp = ["indicative"] # (assume indicative)
                                elif "present" in tmp and "past-historic" in tmp:
                                    tmp = ["present"]
                                elif "adjx" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "cleft" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "causative" in tmp:
                                    tmp = ["causative"] # assume causative dominates
                                else:
                                    print "ambig3", tmp
                            if len(tmp) > 0:
                                verbinfo[f["name"]]= tmp[0]
                    #elif f["name"] == "xarg":
                    elif f.get("name") == "xarg":
                        miniverbinfo = []
                        #for fs in f.findAll('fs'):
                        for fs in f.findall('fs'):
                            #for f2 in fs.findAll('f'):
                            for f2 in fs.findall('f'):
                                #if f2["name"] not in ["gender", "number"]:
                                if f2.get("name") not in ["gender", "number"]:
                                    #for val2 in f2.findAll('val'):
                                    for val2 in f2.findall('val'):
                                        #print "inner:", val2.text.strip()
                                        miniverbinfo.append(val2.text.strip())
                        if len(miniverbinfo) > 0:
                            verbinfo[f["name"]] = "_".join(miniverbinfo)
                        #else:
                        #    if len(val.text.strip()) > 0 and val.text.strip() not in ['sg', 'pl', 'fem', '3', '2', '1', 'masc']:
                        #        print val.text.strip()
                    '''
                    if f["name"] == "mode":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            verbinfo.append(val.text.strip())
                    if f["name"] == "tense":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            verbinfo.append(val.text.strip())
                    '''
                if len(verbinfo) > 0: verbinfos.append(verbinfo)
            #aux, cluster = aux_ds[op["deriv"]]
            aux, cluster = aux_ds[op.get("deriv")]
            verb2info[aux] = verbinfos
            #print "aux", aux, verbinfos
    #print verb2info
    #print "final type: ", type(tok2finalforms[1][0])
    #exit(10)
    if wordsbeforemainverb is None:
        # there is no verb:
        wordsbeforemainverb = -1
    #print "words before main verb", wordsbeforemainverb
    #exit(10)

    return tok2finalforms, tok2lemmacats, verb2info, trees, (weightperword, minweight), wordsbeforemainverb, parsemode

                    '''
                if len(verbinfo) > 0: verbinfos.append(verbinfo)
            #print verbinfos
            #verb, cluster = verb_ds[op["deriv"]]
            verb, cluster = verb_ds[op.get("deriv")]
            verb2info[verb] = verbinfos
            #print "verb V", verb, verbinfos
        #if op["deriv"] in aux_ds and op["cat"] == "Infl":
        if op.get("deriv") in aux_ds and op.get("cat") == "Infl":
            verbinfos = []
            #for narg in op.findAll('narg'): # each narg will be a new verb, second one won't be that linked?
            for narg in op.findall('narg'): # each narg will be a new verb, second one won't be that linked?
                verbinfo = {}
                #for f in narg.findAll('f'):
                for f in narg.findall('f'):
                    #if f["name"] in ["mode", "tense", "control", "extraction", "sat"]:
                    if f.get("name") in ["mode", "tense", "control", "extraction", "sat"]:
                        tmp = []
                        if not f.find("minus"):
                            #for val in f.findAll('val'):
                            for val in f.findall('val'):
                                if len(val.text.strip()) > 0:

                                    #    and val.text.strip() not in ["sg", "fem", "3", "pl", "masc", "present", "infinitive", "indicative", "imperfect", "subjonctive", "cl", "1", "2" "rel", "acc" ]:
                                    #print val.text.strip()
                                    tmp.append(val.text.strip())
                            if len(tmp) > 1:
                                # we need to disambiguate:
                                if "indicative" in tmp and "subjonctive" in tmp:
                                    if "conditional" in tmp:
                                        tmp = ["infinitive"] # something weird going on
                                        print "weird situation"
                                    else:
                                        tmp = ["indicative"] # (assume indicative)
                                elif "present" in tmp and "past-historic" in tmp:
                                    tmp = ["present"]
                                elif "adjx" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "cleft" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "causative" in tmp:
                                    tmp = ["causative"] # assume causative dominates
                                else:
                                    print "ambig3", tmp
                            if len(tmp) > 0:
                                verbinfo[f["name"]]= tmp[0]
                    #elif f["name"] == "xarg":
                    elif f.get("name") == "xarg":
                        miniverbinfo = []
                        #for fs in f.findAll('fs'):
                        for fs in f.findall('fs'):
                            #for f2 in fs.findAll('f'):
                            for f2 in fs.findall('f'):
                                #if f2["name"] not in ["gender", "number"]:
                                if f2.get("name") not in ["gender", "number"]:
                                    #for val2 in f2.findAll('val'):
                                    for val2 in f2.findall('val'):
                                        #print "inner:", val2.text.strip()
                                        miniverbinfo.append(val2.text.strip())
                        if len(miniverbinfo) > 0:
                            verbinfo[f["name"]] = "_".join(miniverbinfo)
                        #else:
                        #    if len(val.text.strip()) > 0 and val.text.strip() not in ['sg', 'pl', 'fem', '3', '2', '1', 'masc']:
                        #        print val.text.strip()
                    '''
                    if f["name"] == "mode":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            verbinfo.append(val.text.strip())
                    if f["name"] == "tense":
                        #for val in f.findAll('val'):
                        for val in f.findall('val'):
                            verbinfo.append(val.text.strip())
                    '''
                if len(verbinfo) > 0: verbinfos.append(verbinfo)
            #aux, cluster = aux_ds[op["deriv"]]
            aux, cluster = aux_ds[op.get("deriv")]
            verb2info[aux] = verbinfos
            #print "aux", aux, verbinfos
    #print verb2info
    #print "final type: ", type(tok2finalforms[1][0])
    #exit(10)
    if wordsbeforemainverb is None:
        # there is no verb:
        wordsbeforemainverb = -1
    #print "words before main verb", wordsbeforemainverb
    #exit(10)

    return tok2finalforms, tok2lemmacats, verb2info, trees, (weightperword, minweight), wordsbeforemainverb, parsemode


# will ignore *** tokens are they are only punctuation
# use lower case to overcome case corrections
# the goal is use up all the tokens but not neccessarily all the worderrors, as others can follow
def align( tokens, worderrors ):
    assert len(tokens) > 0 , "empty tokens list in align!"
    assert len(worderrors) > 0, "empty worderrors list in align!"
    itoken, jworderror = 0,0
    token, worderror = tokens[0].lower(), worderrors[0]
    worderrortoken = worderror[0].lower()
    alignments = [] # will be a 4 tuple of 2 int ranges (i.e. low-high)
    currentlow_t, currentlow_we = 0, 0
    currenthigh_t, currenthigh_we = 0, 0
    while itoken < len(tokens) and jworderror < len(worderrors):
        # get the tokens if it has no alphanumerics in it:
        if not re.search(ur'[^\W_]', token, flags=re.UNICODE):
            token = tokens[itoken].lower()
            # may be multiples:
            #while not re.search(ur'[^\W_]', token, flags=re.UNICODE) and itoken + 1 < len(tokens):
            #    itoken += 1
            #    currenthigh_t = itoken
            #    token = tokens[itoken].lower()
        #  and strip any external punctuation
        token = re.sub(ur'(^[\W_]+|[\W_]+$)', u'', token, flags=re.UNICODE)

        # same for word errors
        if not re.search(ur'[^\W_]', worderrortoken, flags=re.UNICODE):
            #print "yo"
            worderror = worderrors[jworderror]
            worderrortoken = worderror[0].lower()
            #while not re.search(ur'[^\W_]', worderrortoken, flags=re.UNICODE) and jworderror + 1 < len(worderrors):
            #    jworderror += 1
            #    currenthigh_we = jworderror
            #    worderror = worderrors[jworderror]
            #    worderrortoken = worderror[0].lower()
        #  and strip any external punctuation
        worderrortoken = re.sub(ur'(^[\W_]+|[\W_]+$)', u'', worderrortoken, flags=re.UNICODE)

        #print token, worderrortoken
        # check if token is at the start of worderrortoken:
        if re.match(re.escape(token), worderrortoken, flags=re.UNICODE):
            worderrortoken = re.sub(ur'^'+re.escape(token), u"", worderrortoken, flags=re.UNICODE)
            token = ""
            currenthigh_t = itoken
            currenthigh_we = jworderror
            itoken += 1

            # test if the word error is also used up, and add to list if so:
            if not re.search(ur'[^\W_]', worderrortoken, flags=re.UNICODE):
                #print "adding", (currentlow_t, currenthigh_t, currentlow_we, currenthigh_we)
                alignments.append( (currentlow_t, currenthigh_t, currentlow_we, currenthigh_we) )
                jworderror += 1
                currentlow_we = jworderror
                currentlow_t = itoken
                currenthigh_we = jworderror
                currenthigh_t = itoken

        elif re.match(re.escape(worderrortoken), token, flags=re.UNICODE):
            token = re.sub(ur'^'+re.escape(worderrortoken), u"", token, flags=re.UNICODE)
            #worderror = None
            worderrortoken = ""
            currenthigh_we = jworderror
            currenthigh_t = itoken
            jworderror += 1

            # test if the token is also used up, and add to list if so:
            if not re.search(ur'[^\W_]', token, flags=re.UNICODE):
                #print "adding", (currentlow_t, currenthigh_t, currentlow_we, currenthigh_we)
                alignments.append( (currentlow_t, currenthigh_t, currentlow_we, currenthigh_we) )
                itoken += 1
                currentlow_we = jworderror
                currentlow_t = itoken
                currenthigh_we = jworderror
                currenthigh_t = itoken
        else:
            print "major problem, no alignment match!!!", itoken, jworderror
            print tokens
            print worderrors
            assert False, "major problem, no alignment match!!!"

    #print alignments
    if len(tokens)-1 > alignments[-1][1]:
        alignments[-1] = (alignments[-1][0], len(tokens) - 1, alignments[-1][2], alignments[-1][3])
    #if len(worderrors)-1 > alignments[-1][3]:
    #    alignments[-1] = (alignments[-1][0], alignments[-1][1], alignments[-1][2], len(worderrors) -1)

    #print "align", alignments
    #print "align", tokens, len(tokens)
    #print "align", worderrors, len(worderrors)

    #exit(10)
    return alignments

def joinTokens(tokens):
    if len(tokens) == 0: return ""
    # remove any ,."?! at the end or beginning
    outtoken = re.sub(ur'(^\s*[\.,"\?!]+\s*|\s*[\.,"\?!]+\s*$)', u"", tokens[0], flags=re.UNICODE)
    #outtoken = tokens[0]
    for i in range(1, len(tokens)):
        t = tokens[i]
        if t == tokens[i-1]:
            continue
        t = re.sub(ur'(^\s*[\.,"\?!]+\s*|\s*[\.,"\?!]+\s*$)', u"", tokens[i], flags=re.UNICODE)
        # don't add repeated tokens (as they are overlapping ones
        if not re.match(ur'[\W_]+$', t, flags=re.UNICODE):
            if len(outtoken) > 2 and outtoken[-2:] == u"-_":
                outtoken = outtoken[:-2] + u"-"
            if len(outtoken) > 0 and len(t) > 0:
                if outtoken[-1] not in u"'-" and t[0] not in u"'-":
                    outtoken += u" "
            outtoken += t
    return outtoken

# tree1 = observed, tree2 = ideal
def compareTrees( tree1, tree2):
    # trees in structure as given by getFinalTokenFormsAndTrees
    outcomparison = {} # dict treeid -> confusion matrix for all trees with that id
    avPrecision = 0
    avRecall = 0
    for treeid in set(tree1.keys()).intersection(set(tree2.keys())):
        comparison = [0,0,0] # in both, in tree1 but not tree2, in tree2, but not tree1
        val1, val2 = 0, 0
        if treeid in tree1: val1 = len(tree1[treeid])
        if treeid in tree2: val2 = len(tree2[treeid])
        comparison[0] = min(val1, val2)
        if val1 > val2:
            comparison[1] = val1 - val2
        else:
            comparison[2] = val2 - val1

        outcomparison[treeid] = comparison


    tp = 1.0*sum([outcomparison[id][0] for id in outcomparison ])
    precision = tp/sum(outcomparison[id][0]+outcomparison[id][1] for id in outcomparison)
    recall = tp/sum(outcomparison[id][0]+outcomparison[id][2] for id in outcomparison)
    #print tp
    return outcomparison, precision, recall

# note : returns the
def rollingMean( oldmean, oldn, newvalue, repeated=1):
    if oldn == 0:
        return newvalue, repeated
    else:
        newmeanp = (oldmean*oldn + newvalue*repeated)/(0.0+oldn+repeated)
        return newmeanp, oldn + repeated

def geomean(iterable):
    return (reduce(operator.mul, iterable)) ** (1.0/len(iterable))

def analyseFile( origLogFilename, corrpath, errorAlignments, sentenceCounts, parseCounts, meltScores ):
    print "analysing file", origLogFilename
    baseFileName = os.path.basename(origLogFilename)
    baseDir = os.path.dirname(origLogFilename)
    #print baseFileName
    entryNum = int(re.search(ur'entry_(\d+)', baseFileName, flags=re.UNICODE).groups()[0])
    #print entryNum
    # we'll assume less than 100 sentences for each entry:
    detailedInfoDir = os.path.join(baseDir, "entry_"+str(entryNum), "0", "0", "0")
    #print os.path.abspath(os.path.join(baseDir, "..", "analysed_SpellCheckerCorrected"))
    detailedCorrInfoDir = os.path.join(corrpath, "entrycorrected_"+str(entryNum), "0", "0", "0")
    corrLogFilename = os.path.join(corrpath, "entrycorrected_"+str(entryNum) + ".log" )

    #sentenceInfosOrig = documentProperties.getLogFileInfo(origLogFilename)
    #sentenceInfosCorr = documentProperties.getLogFileInfo(corrLogFilename)
    sentenceInfosOrig = getLogFileInfo(origLogFilename)
    sentenceInfosCorr = getLogFileInfo(corrLogFilename)
    #print "oinfo", sentenceInfosOrig
    #print "cinfo", sentenceInfosCorr

    totaleasyalligned = 0
    totalhardalligned = 0
    if entryNum in sentenceAlignments:
        for origsentences, corrsentences in sentenceAlignments[entryNum]:
            print entryNum
            for i in origsentences:
                for j in corrsentences:
                    #print i, j, len(sentenceInfosOrig), len(sentenceInfosCorr), len(origsentences), len(corrsentences)
                    #if sentenceInfosOrig[i-1][0] not in [u"ok", u"corrected", u"robust"] or sentenceInfosCorr[j-1][0] not in [u"ok", u"corrected", u"robust"]:
                    #    print "info orig:", sentenceInfosOrig[i-1]
                    #    print "info corr:", sentenceInfosCorr[j-1]
                    #addToParseCounts(sentenceInfosOrig[i-1], sentenceInfosCorr[j-1], parseCounts, value=1.0/(len(origsentences)*len(corrsentences)))
                    # only divide by no. corr sentences so total = no. of orig sentences
                    addToParseCounts(sentenceInfosOrig[i-1], sentenceInfosCorr[j-1], parseCounts, value=1.0/len(corrsentences))
                    sentenceCounts["hardalign"] += 1.0/(len(corrsentences))
                sentenceCounts["analysed"].add( (entryNum, i) )


    else:
        # break means the break occurs just before this position
        lastSentenceBreak = 0
        thisSentenceBreak = 0
        for orig, corr in zip(sentenceInfosOrig, sentenceInfosCorr):
            print "Sentence Number", corr[1]
            addToParseCounts( orig, corr, parseCounts)
            sentenceCounts["easyalign"] += 1
            sentenceCounts["analysed"].add( (entryNum, int(orig[1])) )

            # look for the last origtoken: - but it might have multiple words, or punctuation, last token will usually just be punctuation
            origtokens = loadTokensFile(os.path.join(detailedInfoDir, "entry_"+str(entryNum)+".E"+orig[1]+".tokens" ))
            corrtokens = loadTokensFile(os.path.join(detailedCorrInfoDir, "entrycorrected_"+str(entryNum)+".E"+orig[1]+".tokens" ))

            finaltokens, origlemmacats, origverb2info, origtrees, origweight, wordsbeforemainverb, parsed =\
                getFinalTokenFormsAndTreesAndWeight(os.path.join(detailedInfoDir, "entry_"+str(entryNum)+".E"+orig[1]+".dep.xml" ))

            corrfinaltokens, corrlemmacats, corrverb2info, corrtrees, corrweight, corrwordsbeforemainverb, parsed =\
                getFinalTokenFormsAndTreesAndWeight(os.path.join(detailedCorrInfoDir, "entrycorrected_"+str(entryNum)+".E"+orig[1]+".dep.xml" ))

            # compare the trees:
            comparison, tprecision, trecall = compareTrees(origtrees, corrtrees)
            for treeid in comparison:
                if treeid not in sentenceCounts["treecompare"]: sentenceCounts["treecompare"][treeid] = []
                sentenceCounts["treecompare"][treeid].append(comparison[treeid])

            sentenceCounts["treecomp_prec"]["orig_"+orig[0]]["corr_"+corr[0]] = rollingMean( sentenceCounts["treecomp_prec"]["orig_"+orig[0]]["corr_"+corr[0]][0],
                                                           sentenceCounts["treecomp_prec"]["orig_"+orig[0]]["corr_"+corr[0]][1],
                                                           tprecision)
            sentenceCounts["treecomp_rec"]["orig_"+orig[0]]["corr_"+corr[0]] = rollingMean( sentenceCounts["treecomp_rec"]["orig_"+orig[0]]["corr_"+corr[0]][0],
                                                          sentenceCounts["treecomp_rec"]["orig_"+orig[0]]["corr_"+corr[0]][1],
                                                          trecall)
            if tprecision > 0.99999 and trecall > 0.99999:
                sentenceCounts["same_trees"] += 1
            else:
                # record info only when trees don't match:
                sentenceCounts["badtreecomp_prec"]["orig_"+orig[0]]["corr_"+corr[0]] = rollingMean( sentenceCounts["treecomp_prec"]["orig_"+orig[0]]["corr_"+corr[0]][0],
                                                           sentenceCounts["treecomp_prec"]["orig_"+orig[0]]["corr_"+corr[0]][1],
                                                           tprecision)
                sentenceCounts["badtreecomp_rec"]["orig_"+orig[0]]["corr_"+corr[0]] = rollingMean( sentenceCounts["treecomp_rec"]["orig_"+orig[0]]["corr_"+corr[0]][0],
                                                          sentenceCounts["treecomp_rec"]["orig_"+orig[0]]["corr_"+corr[0]][1],
                                                          trecall)
                #print "non matching!!!!", entryNum, orig[1]

            #print "prec/rec", tprecision, trecall

            # this is an frmg bug we fix manually for the moment:
            if entryNum == 370 and int(corr[1]) == 8:
                finaltokens[11] = [u"-les"]
            elif entryNum == 377 and int(corr[1]) == 5:
                finaltokens[32] = [u"-moi"]
            elif entryNum == 145 and int(corr[1]) == 2:
                finaltokens[8] = [u"-moi"]

            #for ot, ft in zip(origtokens, finaltokens):
            #    print ot, ft, origtokens[ft-1]

            if len(origtokens) != len(finaltokens):
                print "alignment issue!!!"
                print origtokens
                print finaltokens



            lastOrigTokens = ""
            #print origtokensf
            #for y in origtokens: print y
            tnum = -1
            while lastOrigTokens == u"" and tnum > -len(origtokens):
                lastOrigTokens = re.sub(ur'(^\W+|\W+$)', u'', origtokens[tnum], flags=re.UNICODE)
                tnum -= 1
            #lastOrigTokens = lastOrigTokens.split()
            lastOrigTokens = re.split(ur'\W+', lastOrigTokens, flags=re.UNICODE)
            worderrorlist = errorAlignments[entryNum][2]
            #print "looking for:", lastOrigTokens
            #print lastSentenceBreak, worderrorlist[lastSentenceBreak:]
            #print [x[3] if x[3] is not None else x[0] for x in worderrorlist[lastSentenceBreak:]]
            #print lastOrigTokens, len(lastOrigTokens)

            if entryNum == 46 and int(orig[1]) == 1:
                # this is bugged in sxpipe so we skip it
                thisSentenceBreak = 13
                pass
            else:
                #print "this time", entryNum, orig[1]
                alignment = align(origtokens, worderrorlist[lastSentenceBreak:] )
                #print alignment
                thisSentenceBreak = lastSentenceBreak + alignment[-1][3] + 1

                # count no. of words with errors marked:
                ignore_errs =[u"CAS",u"NPR", u"BRU", u"FOUND", u"INC"]
                n_errorspots = len([x for x in worderrorlist[lastSentenceBreak:thisSentenceBreak]
                                    if len([y for y in x[1] if y not in ignore_errs]) > 0])
                sentenceCounts["error_dist"]["orig_"+orig[0]]["corr_"+corr[0]]  = rollingMean( sentenceCounts["error_dist"]["orig_"+orig[0]]["corr_"+corr[0]][0],
                                                                         sentenceCounts["error_dist"]["orig_"+orig[0]]["corr_"+corr[0]][1],
                                                                         n_errorspots)
                if n_errorspots == 0:
                    sentenceCounts["no_errors"] += 1

                errors = loadSentenceLogFile(os.path.join(detailedInfoDir, "entry_"+str(entryNum)+".E"+orig[1]+".log" ))
                for error in errors:
                    sentenceCounts["allcorrections"] += 1
                    errorname, left1, left2, cat, errortoken = error
                    left1 = int(left1)
                    left2 = int(left2)
                    #print error

                    cluster, tokNumber, origtoken = getTokenFromCluster(
                        os.path.join(detailedInfoDir, "entry_"+str(entryNum)+".E"+orig[1]+".dep.xml" ),
                        int(left1)) # .decode("utf8")
                    #print cluster, tokNumber, origtoken

                    emin, emax = None, None
                    for a,b,c,d in alignment:
                        if a <= tokNumber and tokNumber <= b:
                            emin, emax = c,d
                            break
                    #print alignment, emin, emax, tokNumber
                    foundmatch = False
                    for i in range(emin-1, emax):
                        #print "Compare:", errorname, errortoken, worderrorlist[lastSentenceBreak:][i]
                        if worderrorlist[lastSentenceBreak:][i][3] is not None:
                            foundmatch = True
                    if foundmatch:
                        sentenceCounts["matchcorrections"] += 1
                        for i in range(emin-1, emax):
                            if len(errorAlignments[entryNum][2][lastSentenceBreak+i][1]) > 0:
                                # add the error "FOUND" to the error list, we'll loop over later to look for it
                                errorAlignments[entryNum][2][lastSentenceBreak+i][1].append("FOUND")
                        #print "Check correction quality"

                # now stock the errors to compare which ones are found and which aren't
                # (again skip 46 # 1)

                # get the melt probabilities for the sentence todo corr will need its own alignment?
                meltSentScores = meltScores["orig"][unicode(entryNum)][unicode(orig[1])]
                #print "melt", meltSentScores

                sentenceCounts["err_per_sent"].append(1.0*n_errorspots/(thisSentenceBreak-lastSentenceBreak))
                sentenceCounts["geo_melt_prob"].append(geomean([x[2] for x in meltSentScores]))
                sentenceCounts["alg_melt_prob"].append(sum([x[2] for x in meltSentScores])/(1.0*len(meltSentScores)))
                sentenceCounts["weights"]["orig"].append( (1.0*origweight[0], origweight[1]) )
                sentenceCounts["weights"]["corr"].append( (1.0*corrweight[0], corrweight[1]) )

                #for worderror in worderrorlist[lastSentenceBreak:thisSentenceBreak]:
                pos_in_sent = 0
                #print alignment
                a,b,c,d = alignment[pos_in_sent]
                for i_we in range(lastSentenceBreak,thisSentenceBreak):

                    worderror = worderrorlist[i_we]

                    if i_we - lastSentenceBreak > d:
                        pos_in_sent += 1
                    a,b,c,d = alignment[pos_in_sent]
                    toks = origtokens[a:b+1]
                    #if b+1 > a+1: print "double"

                    #print "toks", toks, worderror
                    #print "melt scores", meltSentScores[a:b+1]
                    #print meltSentScores[a:b+1]
                    meltProb = geomean([x[2] for x in meltSentScores[a:b+1]])

                    es = worderror[1]
                    #print es
                    if len(es) > 0:

                        errorGroupings = {
                           u"INS": u"Spell",
                           u"OMI": u"Spell",
                           u"SUB": u"Spell",
                           u"INV": u"Spell",
                           u"PHG": u"Spell",
                           u"PHO": u"Spell",
                           u"LNF": u"Spell",
                           u"DIA": u"Spell",
                           u"SPC": u"Spell",
                           u"SEP": u"Spell",
                           u"EMP": u"Spell",
                           u"HPO": u"Spell",
                           u"MOR": u"Verbal",
                           u"TPS": u"Verbal",
                           u"MOD": u"Verbal",
                           u"TMP": u"Verbal",
                           u"AUX": u"Verbal",
                           u"CPL": u"Syntax",
                           u"MAN": u"Syntax",
                           u"ORD": u"Syntax",
                           u"SUP": u"Syntax"
                        }

                        spellingerrors = {u"INS", u"OMI", u"SUB", u"INV", u"PHG",
                           u"PHO", u"LNF", u"DIA", u"SPC", u"SEP", u"EMP", u"HPO"}
                        key = frozenset([errorGroupings[x] if x in errorGroupings else x for x in es if x not in [u"CAS",u"NPR", u"BRU", u"FOUND", u"INC"]])

                        if key not in sentenceCounts["meltProbs"]: sentenceCounts["meltProbs"][key] = []
                        sentenceCounts["meltProbs"][key].append(meltProb)

                        if "FOUND" in es:
                            if key not in sentenceCounts["noncorrections"]["found"]:
                                sentenceCounts["noncorrections"]["found"][key] = 0
                            sentenceCounts["noncorrections"]["found"][key] += 1
                        else:
                            #print "not found:", worderror
                            if key not in sentenceCounts["noncorrections"]["nonfound"]:
                                sentenceCounts["noncorrections"]["nonfound"][key] = 0
                            sentenceCounts["noncorrections"]["nonfound"][key] += 1
                            if u"AGR" in es:
                                #print "AGR", worderror, origtokens
                                pass
                            if u"MOR" in es or u"TPS" in es or u"MOD" in es or u"TMP" in es or u"AUX" in es:
                                #print "verbal",  worderror, origtokens
                                pass
                            #for e in es:
                            spellinges = frozenset(e for e in es if e in spellingerrors)
                            # require:
                            # a spelling mistake
                            # an original word which has non-punctuation in it
                            # the i_we is the first of its group (to avoid counting the same error twice
                            origtoken = joinTokens(origtokens[a:b+1])
                            #print origtoken, a, b, origtokens[a:b+1]
                            if len(spellinges) > 0 and not re.match(ur'[\W_]+$', origtoken, flags=re.UNICODE) and i_we == lastSentenceBreak + c:
                                # from a to b in original,
                                flattend_ftokens = []
                                for y in [finaltokens[x] for x in range(a+1,b+2)]:
                                    flattend_ftokens.extend(y)
                                #origtoken = origtokens[a]

                                #print origtoken, origtokens
                                #print len(corrtokens), a, corrtokens
                                #correctedtoken = corrtokens[a]
                                correctedtoken = worderror[3]
                                #print "corr?", correctedtoken, worderror, worderrorlist

                                if b > a:
                                    #origtoken = joinTokens(origtokens[a:b+1])
                                    correctedtoken = joinTokens([x[3] if x[3] is not None else x[0] for x in worderrorlist[lastSentenceBreak+c:lastSentenceBreak+d+1]])
                                #print origtoken, origtokens
                                sxpipetoken = flattend_ftokens[0]
                                if len(flattend_ftokens) > 1:
                                    flattend_ftokens = [x for x in flattend_ftokens if not re.match(ur'[\W_]+$', x, flags=re.UNICODE)]
                                    sxpipetoken = flattend_ftokens[0]
                                    if len(flattend_ftokens) > 1:
                                        #print "length prob", flattend_ftokens
                                        #print [x for x in enumerate(origtokens)]
                                        #print [x for x in enumerate(y[0] for y in worderrorlist[lastSentenceBreak:thisSentenceBreak])]
                                        #print alignment
                                        sxpipetoken = joinTokens(flattend_ftokens)
                                        #print "length prob string:", flattend_ftokens, sxpipetoken

                                #print origtoken, origtokens
                                origtoken = origtoken.lower()
                                if correctedtoken is None:
                                    correctedtoken = origtoken
                                else:
                                    correctedtoken = correctedtoken.lower()
                                sxpipetoken = sxpipetoken.lower()
                                #print "sp:", correctedtoken, "|", sxpipetoken, "|", origtoken, "|", re.sub(ur'e$', u"'", sxpipetoken, flags=re.UNICODE)
                                #allow for e.g. que -> qu' if sxpipe has the long form, but not vice versa

                                if correctedtoken == sxpipetoken or re.sub(ur'e$', u"'", sxpipetoken, flags=re.UNICODE) == correctedtoken:
                                    #print "spelling found!", spellinges, origtokens[a:b+1], correctedtoken,\
                                    #    flattend_ftokens
                                    if spellinges not in sentenceCounts["spelling"]["found"]:
                                        sentenceCounts["spelling"]["found"][spellinges] = []
                                    sentenceCounts["spelling"]["found"][spellinges].append( (origtoken, correctedtoken, sxpipetoken))
                                elif origtoken == sxpipetoken:
                                    #print "spelling not found", spellinges, origtokens[a:b+1], correctedtoken,\
                                    #    flattend_ftokens
                                    if spellinges not in sentenceCounts["spelling"]["notfound"]:
                                        sentenceCounts["spelling"]["notfound"][spellinges] = []
                                    sentenceCounts["spelling"]["notfound"][spellinges].append( (origtoken, correctedtoken, sxpipetoken))
                                elif u"EMP" in spellinges and u"_ETR".lower() == sxpipetoken: # todo 2 cases, changed and unchanged
                                    #print "foreign import found", spellinges, origtokens[a:b+1], correctedtoken,\
                                    #    flattend_ftokens
                                    if spellinges not in sentenceCounts["spelling"]["foreign"]:
                                        sentenceCounts["spelling"]["foreign"][spellinges] = []
                                    sentenceCounts["spelling"]["foreign"][spellinges].append( (origtoken, correctedtoken, sxpipetoken))
                                else:
                                    #print "spelling changed but wrong", spellinges, origtokens[a:b+1], correctedtoken,\
                                    #    flattend_ftokens
                                    if spellinges not in sentenceCounts["spelling"]["changed"]:
                                        sentenceCounts["spelling"]["changed"][spellinges] = []
                                    sentenceCounts["spelling"]["changed"][spellinges].append( (origtoken, correctedtoken, sxpipetoken))

                    else:
                        # i.e. no error found:
                        key = frozenset(["NoError"])
                        if key not in sentenceCounts["meltProbs"]: sentenceCounts["meltProbs"][key] = []
                        sentenceCounts["meltProbs"][key].append(meltProb)

                    # to avoid double counts:
                    if i_we == lastSentenceBreak + c:
                        if meltProb < 0.4:
                            print "low MElt", meltProb, entryNum, orig[1], worderror, meltSentScores[a:b+1]
                            print origtokens



                #exit(3)
                #break

            lastSentenceBreak = thisSentenceBreak


    #print sentenceCounts["meltProbs"]
    #exit(10)
    nSentences = 0

    # find a sentence alignment:
    '''
    alignments = [] # will a list of pairs of sets origSentences : corrSentences
    nextOrigSentNum =  1
    nextCorrSentNum =  1
    allDone = False
    while not allDone:
        origSentNum = set([])
        corrSentNum = set([])
        origTokens = []
        corrTokens = []
        nextOrigTokFileName = os.path.join(detailedInfoDir, "entry_" + str(entryNum) + ".E"
                                                                    + str(nextOrigSentNum) + ".tokens")

        print "intermed", nextOrigTokFileName, os.path.isfile(nextOrigTokFileName)
        didsomething = True
        while didsomething:
            didsomething = False
            while (len(origTokens) == 0 or
                           (len(corrTokens) > len(origTokens) and
                               len([x for x in corrTokens if x not in origTokens]) > 0.2 * len(corrTokens) )) and \
                    os.path.isfile(nextOrigTokFileName):
                # load token files till we can't
                origTokens.extend(loadTokensFile(nextOrigTokFileName))
                origSentNum.add(nextOrigSentNum)
                nextOrigSentNum += 1
                nextOrigTokFileName = os.path.join(detailedInfoDir, "entry_" + str(entryNum) + ".E"
                                                                        + str(nextOrigSentNum) + ".tokens")
                print "intermedin", nextOrigTokFileName, os.path.isfile(nextOrigTokFileName), [x for x in corrTokens if x not in origTokens]
                print "checks1:", len([x for x in corrTokens if x not in origTokens]), len(corrTokens), nextOrigSentNum, nextCorrSentNum
                didsomething = True
            nextCorrTokFileName = os.path.join(detailedCorrInfoDir, "entrycorrected_" + str(entryNum) + ".E"
                                                                        + str(nextCorrSentNum) + ".tokens")

            while (len(corrTokens) == 0 or
                           (len(origTokens) > len(corrTokens) and
                                len([x for x in origTokens if x not in corrTokens]) > 0.2 * len(origTokens))) and \
                    os.path.isfile(nextCorrTokFileName):
                corrTokens.extend(loadTokensFile(nextCorrTokFileName))
                corrSentNum.add(nextCorrSentNum)
                nextCorrSentNum += 1
                nextCorrTokFileName = os.path.join(detailedCorrInfoDir, "entrycorrected_" + str(entryNum) + ".E"
                                                                        + str(nextCorrSentNum) + ".tokens")
                print "intermedun", nextCorrTokFileName, os.path.isfile(nextCorrTokFileName), [x for x in origTokens if x not in corrTokens]
                print "checks2:", len([x for x in origTokens if x not in corrTokens]), len(origTokens), nextOrigSentNum, nextCorrSentNum
                didsomething = True
        print "finished", len(origTokens), len(corrTokens), nextOrigSentNum, nextCorrSentNum
        if len(origTokens) == 0 or len(corrTokens) == 0: # or means we break out even if we bug (`and' will go forever)
            if len(origTokens) == 0 and len(corrTokens) == 0:
                allDone = True
            else:
                print "Bug!", alignments
                exit(10)
        else:
            alignments.append( (origSentNum, corrSentNum) )
    print "alignments:", alignments
    '''

    for detailedfilename in os.listdir(detailedInfoDir):
        base, ext = os.path.splitext(detailedfilename)
        if ext == ".xml":
            base, ext2 = os.path.splitext(base)
            ext = ext + ext2
            if not os.path.isfile(os.path.join(detailedInfoDir, base + ".tokens")): print "problem", base
        origsentNumber = int(re.search(ur"\.E(\d+)", base, flags=re.UNICODE).groups()[0])
        #print base, ext


        if ext == ".tokens": # don't use .log as an extra empty file seems to be being produced
            nSentences += 1
            if (entryNum, origsentNumber) not in sentenceCounts["analysed"]:
                print "problem:", entryNum, origsentNumber
            #if not os.path.isfile(os.path.join(detailedInfoDir, base + ".dep.xml")): print "problem", base
        '''
        origsentNumber = int(re.search(ur"\.E(\d+)", base, flags=re.UNICODE).groups()[0])

        if ext == ".tokens":
            with codecs.open(os.path.join(detailedInfoDir,detailedfilename)) as detfile:
                origtokens = detfile.read()
            nTokensOrig = len(origtokens.split('\n'))
            nTokensCorr = 0
            while ( nTokensCorr -nTokensOrig) > 2:
                with codecs.open(detailedcorrfilename) as detcorrfile:
                    origtokens = detcorrfile.read()
                print "orig", len(origtokens.split()), "corr", len(origtokens.split())

            detailedcorrfilename = os.path.join(detailedCorrInfoDir, 'entrycorrected_' + str(entryNum) +
                                            '.E' + str(sentNumber) + ext)
        '''

    nCorrSentences = 0
    for detailedcorrfilename in os.listdir(detailedCorrInfoDir):
        base, ext = os.path.splitext(detailedcorrfilename)
        if ext == ".xml":
            base, ext2 = os.path.splitext(base)
            ext = ext + ext2
        #print base, ext

        if ext == ".tokens": # don't use log
            nCorrSentences += 1

    if nSentences != nCorrSentences:
        print "entrynum:", entryNum, nSentences, nCorrSentences
        sentenceCounts["diff"] += 1
        #print "allyo", alignments
    #if len([x for x,y in alignments if len(x)>1 or len(y)>1]):
        #print "align:", alignments

    sentenceCounts["orig"] += nSentences
    sentenceCounts["corr"] += nCorrSentences

    #exit(10)





def main():
    origpath = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/"
    corrpath = "/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellCheckerCorrected/"
    erroralignpath = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellCheckerJson/entry.json"
    origmeltpath = "/home/nparslow/Documents/AutoCorrige/Corpora/outputs/melted_orig.json"
    corrmeltpath = "/home/nparslow/Documents/AutoCorrige/Corpora/outputs/melted_corr.json"

    sentenceCounts, parseCounts = analyse(origpath, corrpath, erroralignpath, origmeltpath, corrmeltpath)
    print sentenceCounts

    types = ["ok", "corrected", "robust"]
    print parseCounts
    print "corr", types
    for origt in types:
        print origt, "&", " & ".join([str(parseCounts["orig_"+origt]["corr_"+x]) for x in types]) + " \\\\"

    # percentatages
    tot = 0
    for origt in types:
        tot += sum(parseCounts["orig_"+origt].values())
        #print origt, "&", " & ".join([str(parseCounts["orig_"+origt]["corr_"+x]/) for x in types]) + " \\\\"
    print tot

    print "tot easy/hard/sum aligned:", sentenceCounts["easyalign"], sentenceCounts["hardalign"], sentenceCounts["easyalign"] + sentenceCounts["hardalign"]

    print "all corrections", sentenceCounts["allcorrections"]
    print "matched corrections", sentenceCounts["matchcorrections"], "=", 1.0*sentenceCounts["matchcorrections"]/sentenceCounts["allcorrections"]

    #tokens = ["a", "***", "bc"]
    #errors = [["ab"], ["c"]]
    ##tokens = ["a", "b"]
    ##errors = [["ab"] ]
    #print align(tokens, errors)

    print
    print "corrections:"
    print sentenceCounts["noncorrections"]["found"]
    print sentenceCounts["noncorrections"]["nonfound"]


    #print [tuple(set(errorGroupings[y] if y in errorGroupings else y for y in x))for x in sentenceCounts["noncorrections"]["found"]]
    #print dict([tuple(set(errorGroupings[y] if y in errorGroupings else y for y in x), sum( sentenceCounts["noncorrections"]["nonfound"]])) for x in sentenceCounts["noncorrections"]["nonfound"]])


    # simplify again the error counts:
    newerrorcounts = {u"PNC":0, u"Spell":0, u"AGR":0, u"Verbal":0, u"Syntax":0, u"LEX":0, "nonerror":0}
    for x,y in sentenceCounts["noncorrections"]["nonfound"].iteritems():
        added = False
        for label in [u"PNC", u"Spell", u"Syntax", u"LEX", u"AGR", u"Verbal"]:
            if label in x:
                newerrorcounts[label] += y
                added = True
                break
        if not added:
            if len(x) == 0:
                newerrorcounts["nonerror"] += y
            else:
                print x
                #if x not in newerrorcounts:
                #    newerrorcounts[x] = 0
                #newerrorcounts[x] += y
                if "other" not in newerrorcounts: newerrorcounts["other"] = 0
                newerrorcounts["other"] += y

    print "newcounts", newerrorcounts

    keys = sorted(newerrorcounts.keys(), key=lambda x: newerrorcounts[x])

    def plotMissedErrors(newerrorcounts):
        fig = plt.subplot(111)
        #width = 0.8
        plt.bar(range(len(keys)), [newerrorcounts[x] for x in keys])
        width = 0.8
        fig.set_xticks(np.arange(len(keys)) + width/2)
        fig.set_xticklabels(keys, rotation=45)
        plt.ylim((0,850))
        plt.savefig("missederrors.png")
        plt.show()

    #plotMissedErrors(newerrorcounts)


    #print getFinalTokenForms("/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_329/0/0/0/entry_329.E1.dep.xml") # simple
    #print getFinalTokenForms("/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_361/0/0/0/entry_361.E3.dep.xml") # with 'par example'
    #print getFinalTokenForms("/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_361/0/0/0/entry_361.E7.dep.xml") # with 'au'
    #print getFinalTokenForms("/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_81/0/0/0/entry_81.E1.dep.xml") # with 'plus ou moins'
    # frmg bugs:
    #print getFinalTokenForms("/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_145/0/0/0/entry_145.E2.dep.xml") #
    #print getFinalTokenForms("/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_370/0/0/0/entry_370.E8.dep.xml")
    #print getFinalTokenForms("/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_377/0/0/0/entry_377.E5.dep.xml")


    print sentenceCounts["spelling"]["found"]
    print sentenceCounts["spelling"]["notfound"]
    print sentenceCounts["spelling"]["foreign"]
    print sentenceCounts["spelling"]["changed"]

    def frozenset2string( fset ):
        return "_".join(sorted([x for x in fset]))

    outspelling = {}
    for y in ["found", "notfound", "foreign", "changed"]:
        outspelling[y] = {}
        print
        print y + " spelling:", sum(len(sentenceCounts["spelling"][y][x]) for x in sentenceCounts["spelling"][y])
        for x in sentenceCounts["spelling"][y]:
            print x, len(sentenceCounts["spelling"][y][x]),"\t", sentenceCounts["spelling"][y][x]
            outspelling[y][frozenset2string(x)] = sentenceCounts["spelling"][y][x]

    print outspelling

    outfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/spelling.json"
    with codecs.open(outfilename, mode="w", encoding="utf8") as ofile:
        json.dump(outspelling, ofile)


    outmelt = {}
    for x in sentenceCounts["meltProbs"]:
        print x, len(sentenceCounts["meltProbs"][x]),"\t", sentenceCounts["meltProbs"][x]
        key = frozenset2string(x)
        if len(key) == 0:
            key = "NoError"
        if key not in outmelt:
            outmelt[key] = []
        outmelt[key].extend( sentenceCounts["meltProbs"][x] )

    print outmelt

    outfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/meltprobs.json"
    with codecs.open(outfilename, mode="w", encoding="utf8") as ofile:
        json.dump(outmelt, ofile)

    outmeltweightsentence = {}
    outmeltweightsentence["eps"] = sentenceCounts["err_per_sent"]
    outmeltweightsentence["geomean"] = sentenceCounts["geo_melt_prob"]
    outmeltweightsentence["algmean"] = sentenceCounts["alg_melt_prob"]
    outmeltweightsentence["origweight"]= sentenceCounts["weights"]["orig"]
    outmeltweightsentence["corrweight"]= sentenceCounts["weights"]["corr"]

    outfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/meltsentprobs.json"
    with codecs.open(outfilename, mode="w", encoding="utf8") as ofile:
        json.dump(outmeltweightsentence, ofile)


    print
    print "tree comparison"
    print "no. sentences with same trees:", sentenceCounts["same_trees"]
    print
    for tid in sentenceCounts["treecompare"]:
        print tid, len(sentenceCounts["treecompare"][tid])
        print sentenceCounts["treecompare"][tid]

    for orig in types:
        for corr in types:
            print "orig", orig, "corr", corr
            print "mean precision", sentenceCounts["treecomp_prec"]["orig_"+orig]["corr_"+corr][0]
            print "mean recall", sentenceCounts["treecomp_rec"]["orig_"+orig]["corr_"+corr][0]
            print "mean bad only precision", sentenceCounts["badtreecomp_prec"]["orig_"+orig]["corr_"+corr][0]
            print "mean bad only recall", sentenceCounts["badtreecomp_rec"]["orig_"+orig]["corr_"+corr][0]

    outfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/treecompare.json"
    with codecs.open(outfilename, mode="w", encoding="utf8") as ofile:
        json.dump(sentenceCounts["treecompare"], ofile)


    # error count by parsing dist
    print
    print "Sentences w/o errors", sentenceCounts["no_errors"]
    print
    print "error dis:"
    for orig in types:
        for corr in types:
            print "orig:", orig, "corr:", corr
            print "n with errors:", sentenceCounts["error_dist"]["orig_"+orig]["corr_"+corr][1], \
                "mean errors:",  sentenceCounts["error_dist"]["orig_"+orig]["corr_"+corr][0]



    '''
    # tree testing:
    entryNum = 2
    sentNum = 1
    detailedInfoDir = u"/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellChecker/entry_" + str(entryNum) + "/0/0/0/"
    detailedCorrInfoDir = u"/home/nparslow/Documents/AutoCorrige/Corpora/analysed_SpellCheckerCorrected/entrycorrected_" + str(entryNum) + "/0/0/0/"

    finaltokens, origlemmacats, origtrees, origweight, wordsbeforemainverb = getFinalTokenFormsAndTreesAndWeight(os.path.join(detailedInfoDir, "entry_"+str(entryNum)+".E"+ str(sentNum) +".dep.xml" ))

    corrfinaltokens, corrlemmacats, corrtrees, corrweight, corrwordsbeforemainverb = getFinalTokenFormsAndTreesAndWeight(os.path.join(detailedCorrInfoDir, "entrycorrected_"+str(entryNum)+".E"+str(sentNum)+".dep.xml" ))

    # compare the trees:
    comparison, tprecision, trecall = compareTrees(origtrees, corrtrees)
    print comparison
    print tprecision
    print trecall
    print "weights", origweight, corrweight
    '''

if __name__=='__main__':
    main()