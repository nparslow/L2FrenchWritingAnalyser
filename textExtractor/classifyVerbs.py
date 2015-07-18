# coding=utf-8
__author__ = 'nparslow'


def addToCount( info2count, base, tense, mood):
    if tense not in info2count[base]: info2count[base][tense] = {}
    if mood not in info2count[base][tense]: info2count[base][tense][mood] = 0
    info2count[base][tense][mood] += 1

def classifyVerbs( verb2info ):
    info2count = {
        "single": {},
        "aux": {},
        "compound":{},
        "clause": {},
    }
    output = {}
    for verb, info in verb2info.items():

        if len(info) == 1:
            tense = "notense"
            if "tense" in info[0]:
                tense = info[0]["tense"]
            mood = "infinitive" # sometimes mood is not there
            if "mode" in info[0]:
                mood = info[0]["mode"]
            if mood == "indicative" and tense == "notense":
                mood = "infinitive" # coordination screws it up
            addToCount(info2count, "single", tense, mood)
            if "extraction" in info[0]:
                base = "clause"
                extr = info[0]["extraction"]
                xarg = "noxarg"
                if "xarg" in info[0]:
                    xarg = info[0]["xarg"]
                addToCount(info2count, base, extr, xarg)

        elif len(info) ==2:
            v1info, v2info = info
            base = "compound"
            if verb in [u"être", u"avoir"]:
                base = "aux"
            tense = "notense"
            if "tense" in info[1]:
                tense = info[1]["tense"]
            mood = "infinitive" # sometimes mood is not there
            if "mode" in info[1]:
                mood = info[1]["mode"]
            addToCount(info2count, base, tense, mood)
            if mood == "indicative" and tense == "notense":
                mood = "infinitive" # coordination screws it up
            if "extraction" in info[1]:
                base = "clause"
                extr = info[1]["extraction"]
                xarg = "noxarg"
                if "xarg" in info[1]:
                    xarg = info[1]["xarg"]
                addToCount(info2count, base, extr, xarg)
        else:
            if "multi" not in output: output["multi"] = 0
            output["multi"] += 1 # todo work out what these are
            #assert False, "problem chain of 3 verbs!"


    # we extract some basic verb info, can work on more advanced later
    #print
    #print "info to count"
    #print info2count
    output = {}
    # basically linearise the data by projecting, this gives non-independent info, but should be usually > 0
    for struc in info2count: # should be single, aux, compound, clause
        #output[struc] = sum([info2count[struc][x][y] for x in info2count["single"] for y in info2count["single"][x]])


        for x in info2count[struc]:
            for y in info2count[struc][x]:
                count = info2count[struc][x][y]

                if struc == "clause":
                    if x not in output: output[x] = 0
                    output[x] += 1 # hopefully will count no. rel clauses
                    for case in ["nom", "acc", "loc"]:
                        if case in y: # as in string-wise
                            if case not in output: output[case] = 0
                            output[case] += count

                else:
                    if struc not in output: output[struc] = 0
                    output[struc] += count
                    if y not in output: output[y] = 0
                    output[y] += count
                    if x not in output: output[x] = 0
                    output[x] += count

    totalverbgroups = len(verb2info.items())
    return output, totalverbgroups