# coding=utf-8
import operator
import codecs

__author__ = 'nparslow'


def getMEltDiffs(tok2lemmacats, meltToks, debug=False):
    # todo: not sure of the best place to put this
    # note v is both a non-terminal and a terminal in frmg
    # see http://alpage.inria.fr/frmgwiki/content/tagset-frmg
    # epsilon in frmg goes to none,
    meltTag2frmgTag = {
        u"v": {u"aux", u"v"}, # MElt: v is an indicative verb (not subjonctive)
        u"vinf": {u"v", u"aux", u"vmodprep"},
        u"vimp": {u"v", u"aux"},
        u"vs": {u"aux", u"v"}, # Melt: subjunctive verb, should go to same as "v" in frmg
        u"vpp": {u"v", u"aux"}, # MElt past participle
        u"ppr": {u"v", u"aux", u"vmodprep"}, # Melt present participle
        u"nc": {u"nc", u"ncpred", u"ncpred2"}, # melt common noun
        u"npp": {u"np", u"title"}, # melt proper noun
        u"cc": {u"coo"},  # melt coordinating conjunction
        u"cs": { u"csu", u"que", u"pri"}, # melt subordinating conjunction # que shouldn't be here???
        u"adj": {u"adj", u"number"}, # number here as well as elsewhere?
        u"adjwh": {u"adj"},
        u"adv": {u"advneg", u"adv", u"clneg", u"predet"},
        u"advwh": {u"adv"},
        u"cls": {u"cln", u"pro", u"ilimp", u"caimp", u"ce"}, # subject clitic , can ça (caimp) go here?
        u"clo": {u"cld", u"cla", u"cll", u"clr", u"caimp", u"clg", u"cll"}, # object clitic
        u"clr": {u"cla", u"clr"}, # reflexive clitic # can cla (accusative clitic) be here?
        u"p": {u"prep"}, # preposition
        u"p+d": {u"det", u"prep"}, # prep + det amalgam
        u"p+pro": {u"prep", u"xpro", u"pri", u"prel"}, # prep + pronoun amalgam ? auquel?
        u"i": {u"pres", u"adv", u"np", u"nc"}, # interjection (not really treated in frmg, results are very random
        u"ponct": {u"_", u"poncts", u"ponctw", u"incise"}, # incise = for commas for incisions etc.
        u"et": {u"_ETR"}, # foreign word
        u"prowh": {u"pri"}, # inter. Pronoun
        u"prorel":{u"prel", u"pri"}, # relative pronoun
        u"pro": {u"xpro"}, # other pronoun
        u"detwh":{u"det",}, # inter. determinant
        u"det": {u"det", u"number"}, # other det.
    }
    meltdiffs = 0
    if len(tok2lemmacats) != len(meltToks):
        print "YIKES! melt token mismatch", len(tok2lemmacats), len(meltToks)
    else:
        for i in range(len(tok2lemmacats)):
            #if tok2lemmacats[i+1][1].lower() != meltToks[i][1].lower():
            #if meltToks[i][1].lower() not in [x[1] for x in tok2lemmacats[i+1]]:
            #    print "blaldajf1"
            if i+1 in tok2lemmacats: # normally should pass here w/o problem
                if meltToks[i][1] != "ET": # melt has a very broad et count, so just ignore it
                    melttags = {meltToks[i][1].lower()}
                    if meltToks[i][1].lower() in meltTag2frmgTag:
                        melttags = meltTag2frmgTag[meltToks[i][1].lower()]
                    if len( melttags.intersection( set([x[1] for x in tok2lemmacats[i+1]]))) == 0\
                            and len([x for x in tok2lemmacats[i+1] if x[0] == "_"]) == 0: # i.e. ignore any time frmg has an underscore
                        if debug: print "meltdiff:", tok2lemmacats[i+1], meltToks[i]
                        meltdiffs += 1
    return meltdiffs


def geomean(iterable):
    return (reduce(operator.mul, iterable)) ** (1.0/len(iterable))

# to merge should be a list of tok-tag-prob 3-tuples
# tok and tag are concated with a space, prob has geometric mean taken
def mergeInfo( to_merge , divider = " "):
    #print to_merge, [x[2] for x in to_merge]
    return (divider.join(x[0] for x in to_merge), " ".join(x[1] for x in to_merge), geomean([x[2] for x in to_merge]))


def loadMEltFile( meltfilename ):
    meltTokens = []
    with codecs.open(meltfilename, mode="r", encoding="utf8") as mfile:
        for line in mfile:
            line = line.strip()
            token, pos, prob = line.split('\t')
            prob = float(prob)
            meltTokens.append((token, pos, prob))
    return meltTokens


def alignToksMeltToks( tokens, meltTokens):
        # if we had multi-word tokens we may have to re-fuse them
    if len(meltTokens) == len(tokens):
        return meltTokens
    else:
        new_outlist = []
        i = -1
        to_merge = []
        old_orig, old_tok = None, None
        for orig_i in range(len(tokens)):
            to_merge = []
            orig_tok = tokens[orig_i]
            if old_orig is not None:
                orig_tok = old_orig + "_" + orig_tok
                old_orig = None
            tok, tag, prob = None, None, None
            if old_tok is not None:
                tok = old_tok
                old_tok = None
            while tok != orig_tok :
                #print tok, "yo", orig_tok, tok==u':_)', orig_tok == u":"
                if tok is not None and len(tok) > len(orig_tok):
                    old_orig = orig_tok
                    old_tok = tok
                    break
                else:
                    i += 1
                    nexttok, nexttag, nextprob = meltTokens[i]
                    #print i, nexttok, nexttag, nextprob
                    to_merge.append((nexttok, nexttag, nextprob))
                    if len(to_merge) > 0:
                        #print "merging", to_merge
                        tok, tag, prob = mergeInfo(to_merge)
                    else:
                        tok, tag, prob = nexttok, nexttag, nextprob
            #if tok == u':_)' and orig_tok == u":":

            #else:
            new_outlist.append((tok,tag,prob))
        return  new_outlist


def loadAndAlign(meltfile, tokens):
    meltToks = loadMEltFile(meltfile)
    #print meltToks
    return alignToksMeltToks(tokens, meltToks)
