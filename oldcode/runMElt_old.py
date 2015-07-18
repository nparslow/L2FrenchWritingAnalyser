# coding=utf-8
import os
import subprocess

__author__ = 'nparslow'

# requires a tokenised sentence, without the e.g. '_NUMBER' style tags

# sentence is a sequence of tokens
def getMElt( sentence ):

    if "/home/nparslow/exportbuild/bin/" not in os.environ['PATH']:
        os.environ['PATH'] += ":/home/nparslow/exportbuild/bin/"


    command1 = 'echo'
    args1 = ' '.join(sentence)
    command2 = 'MElt'
    args2 = '-P'
    #print "running", args1
    p1 = subprocess.Popen([command1, args1], stdout=subprocess.PIPE)
    p2 = subprocess.Popen([command2, args2], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a fileName, fileExtension = os.path.splitext(SIGPIPE if p2 exits.
    output = p2.communicate()[0].decode('utf8')

    # list of 3-tuples : token, tag, proba
    print output
    outlist = []
    for ttp in output.split(' '):
        # to deal with a MElt bug: of disappearing tag with the proba option
        try:
            tok, tag, prob = ttp.rsplit('/',2)
        except:
            tok, prob = ttp.rsplit('/',1)
            tag = "NPP"
        #tok = tok
        #tag = tag.decode('utf8')
        prob = float(prob)
        outlist.append((tok, tag, prob))

    # if we had multi-word tokens we may have to re-fuse them
    if len(outlist) == len(sentence):
        return outlist
    else:
        new_outlist = []
        i = -1
        to_merge = []
        for orig_i in range(len(sentence)):
            to_merge = []
            orig_tok = sentence[orig_i]
            tok, tag, prob = None, None, None
            while (tok != orig_tok):
                i += 1
                nexttok, nexttag, nextprob = outlist[i]
                #print i, nexttok, nexttag, nextprob
                to_merge.append((nexttok, nexttag, nextprob))
                if len(to_merge) > 0:
                    tok, tag, prob = mergeInfo(to_merge)
                else:
                    tok, tag, prob = nexttok, nexttag, nextprob

            new_outlist.append((tok,tag,prob))
        return  new_outlist


import operator
def geomean(iterable):
    return (reduce(operator.mul, iterable)) ** (1.0/len(iterable))



# to merge should be a list of tok-tag-prob 3-tuples
# tok and tag are concated with a space, prob has geometric mean taken
def mergeInfo( to_merge ):
    print to_merge
    return (" ".join(x[0] for x in to_merge), " ".join(x[1] for x in to_merge), geomean([x[2] for x in to_merge]))



#melted = getMElt([u'il', u'a', u'une', u'pommé de terre'])
#for a,b,c in melted:
#    print a,b,c