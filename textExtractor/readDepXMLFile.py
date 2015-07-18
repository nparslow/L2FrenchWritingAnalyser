# coding=utf-8
import codecs
import os
import re
import subprocess
import xml.etree.cElementTree as ET

__author__ = 'nparslow'


# from http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
def run_command(command1, args1, command2, args2):
    # run_command("echo", charmatch.group(), "/home/nparslow/exportbuild/bin/yadecode", '-u -l=fr')
    p1 = subprocess.Popen([command1, args1], stdout=subprocess.PIPE)
    p2 = subprocess.Popen([command2, args2], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = p2.communicate()[0]
    # print output.decode('latin1')#, type(output.decode('latin1'))
    # print output.strip(), type(output)
    # print output.strip().decode('latin1') #.decode('utf8')
    # return output.strip().decode('utf8')
    # return output.strip().decode('latin1') #.decode('utf8')
    return output.strip().decode('utf8')

    '''
    # returns a tuple (0, 'output we want')
    # only works on *nix
    # returns wrong format
    output = commands.getstatusoutput(command)
    return output[1]
    '''
    '''
    print command
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    return iter(p.stdout.readline, b'')
    '''


def fixMixedEncodings(token):
    chars = re.finditer(ur'(?:&#\d\d\d\;)+', token, flags=re.UNICODE)
    newtoken = u""
    usedpos = 0
    for charmatch in chars:
        newtoken += token[usedpos:charmatch.start()]
        usedpos = charmatch.end()
        # translate the character:
        command = 'echo "' + charmatch.group() + '" |' \
                                                 ' /home/nparslow/exportbuild/bin/yadecode -u -l=fr'
        # os.system(command)
        # translation = "".join(run_command(command))
        # c = run_command(command)
        c = run_command("echo", charmatch.group(), "/home/nparslow/exportbuild/bin/yadecode", '-u -l=fr')
        # print c, type(c)
        # print c.decode('utf8'), type(c.decode('utf8'))
        newtoken += c
    newtoken += token[usedpos:]
    if newtoken != token:
        # print token, newtoken
        token = newtoken
        # for x in translation:
        #    print x

    # todo some empty tokens arrive here:
    return token
    if len(token) > 0:
        pass


# currently only a problem with &, but there are lots of potential ones:
# see https://www.utexas.edu/learn/html/spchar.html
def removeHTMLchars(token):
    code2char = {
        ur"\&amp": u"&"
    }
    for code in code2char:
        token = re.sub(code, code2char[code], token, flags=re.UNICODE)
    return token


def getTokensFromFile(processedTokenFile):
    tokens = []
    if os.path.isfile(processedTokenFile):
        # print "*** using tokens ***", processedTokenFile
        # .tokens files are in utf-8 if run individually, latin-1 if run over corpus
        with codecs.open(processedTokenFile, mode="r", encoding='utf8') as tokenFile:
            for tokenline in tokenFile:
                # check for a tab as the last line is empty
                if '\t' in tokenline:
                    # print tokenline
                    tokenNum_token = tokenline.strip().split('\t')
                    # can have empty tokens, ignore them:
                    if len(tokenNum_token) > 1:
                        tokenNum, token = tokenline.strip().split('\t')
                        # take all tokens at this point, including punctuation
                        # if re.search(ur'[^\W_]', token, flags=re.UNICODE):

                        # hack to fix the euro problem:
                        token = fixMixedEncodings(token)
                        token = removeHTMLchars(token)
                        # token = re.sub(ur'\&\#226;\&\#130;\&\#172;', u'€', token, flags=re.UNICODE)
                        tokens.append(token)
    # print "got raw toks", tokens
    return tokens


def readDepXMLFile(xmlfilename, debug=False):
    if debug: print "readDepCMLFile:", xmlfilename

    tok2finalforms = {}
    tok2lemmacats = {}
    cid2token = {}
    token2cids = {}
    cid2form = {}
    cid2lemmacat = {}
    verb2info = {}
    trees = {}  # we ignore the node numbers for the moment, and store treenum : list of (cat, treeinfo) tuples, where treeinfo is a list of properties
    #  (top list covers multiple trees of same type in the parse, lower level = all the properties added
    # actually bottow list = 2 tuple (cat, []) where [] is the list of properties
    weightperword = 0
    minweight = 0
    wordsbeforemainverb = None

    verb_ds = {}
    aux_ds = {}

    tree = ET.parse(xmlfilename)

    dep = tree.getroot()  # dependencies should be the root

    if 'nw' in dep.attrib:
        weightperword = int(dep.get("nw"))

    parsemode = dep.get("mode")  # robust, ok, corrected

    for cluster in dep.findall("cluster"):
        id = cluster.get("id")
        tokenNums = re.findall(ur"E\d+F(\d+)|.+(?: $)", cluster.get("lex"), flags=re.UNICODE)
        if debug: print "token numbers:", tokenNums
        tokenNums = [int(x) for x in tokenNums if len(x) > 0]  # somehow gets empty string
        for tokenNumber in tokenNums:
            if tokenNumber not in token2cids: token2cids[tokenNumber] = []
            token2cids[tokenNumber].append(id)  # we'll change the id later
            cid2token[id] = tokenNumber

    for node in dep.findall('node'):
        cluster = node.get("cluster")
        form = node.get("form")
        cat = node.get("cat")
        lemma = node.get("lemma")
        if type(form) != 'unicode':  # soup returns a str if it can, a unicode otherwise
            form = unicode(form)
        if type(cat) != 'unicode':  # soup returns a str if it can, a unicode otherwise
            cat = unicode(cat)
        if type(lemma) != 'unicode':  # soup returns a str if it can, a unicode otherwise
            lemma = unicode(lemma)
        cid2form[cluster] = form
        cid2lemmacat[cluster] = (lemma, cat)

        treenum = node.get("tree")
        treeinfo = ""
        if " " in treenum:
            treenum, treeinfo = node.get("tree").split(' ', 1)
        # for the moment we take just 'cat', not 'xcat'=parent?
        # treenum can be an integer or an id label "follow_coord" (for higher level trees?)
        try:
            treenum = int(treenum)
        except:
            pass
        treeinfo = treeinfo.split()
        cat = node.get("cat")
        if treenum not in trees: trees[treenum] = []
        trees[treenum].append((cat, treeinfo))

        if cat == "v":
            if "deriv" in node.attrib:
                verb_ds[node.get("deriv")] = (lemma, cluster)
            else:
                # in case of robust analysis and no interpretation
                pass
        if cat == "aux":
            if "deriv" in node.attrib:
                aux_ds[node.get("deriv")] = (lemma, cluster)
            else:
                # robust analysis and no interpretation
                pass

    for tokenNum in token2cids:
        clusters = token2cids[tokenNum]
        # put clusters in order: (by their start point
        clusters = sorted(clusters,
                          key=lambda x: int(re.search(ur'^E\d+c_(\d+)_\d+', x, flags=re.UNICODE).groups()[0]))
        tok2finalforms[tokenNum] = [cid2form[x] for x in clusters]
        tok2lemmacats[tokenNum] = [cid2lemmacat[x] for x in clusters]

    for edge in dep.findall('edge'):
        if 'w' in edge.attrib:
            minweight = min(minweight, int(edge.get("w")))

    maxspan = -1
    for op in dep.findall('op'):
        if op.get("deriv") in verb_ds and op.get("cat") == "S":  # need S for gerundive ...

            # check if it is the main verb in the sentence:
            span = op.get("span")
            # the span will have an even number of entries (2, 4 etc.) separated by a space,
            # we are looking for a span from 0 to end of sentence with no gaps in between:
            spansplit = span.split(" ")
            if len(spansplit) == 2:
                spanstart, spanend = int(spansplit[0]), int(spansplit[1])

                if parsemode == "robust":
                    # take the first verb
                    lemma, cluster = verb_ds[op.get("deriv")]
                    position = cid2token[cluster] - 1
                    # hopefully 100000 is longer than any sentence we'll encounter!
                    if wordsbeforemainverb is None: wordsbeforemainverb = 100000
                    if position < wordsbeforemainverb:
                        wordsbeforemainverb = position
                else:
                    if spanend - spanstart > maxspan:
                        maxspan = spanend - spanstart
                        lemma, cluster = verb_ds[op.get("deriv")]
                        wordsbeforemainverb = cid2token[cluster] - 1

        if (op.get("deriv") in verb_ds and (op.get("cat") == "S" or op.get("cat") == "V")) or \
                (op.get("deriv") in aux_ds and op.get("cat") == "Infl"):
            #print "checking", op.get("deriv")

            verbinfos = []
            for narg in op.findall('narg'):
                #print "narging"
                verbinfo = {}
                changetoinfintive = False  # todo probably only relevant for S? at this point not used
                for fs in narg.findall('fs'):
                  for f in fs.findall('f'):
                    #print "effing", f.get("name"), f.attrib, f

                    if f.get("name") in ["mode", "tense", "control", "extraction", "sat"]:
                        #print "yo", f.get("name")
                        tmp = []
                        if not f.find("minus"):
                            for val in f.findall('val'):
                                if len(val.text.strip()) > 0:
                                    #    and val.text.strip() not in ["sg", "fem", "3", "pl", "masc", "present", "infinitive", "indicative", "imperfect", "subjonctive", "cl", "1", "2" "rel", "acc" ]:
                                    tmp.append(val.text.strip())
                            if len(tmp) > 1:
                                # we need to disambiguate:
                                if "indicative" in tmp and "subjonctive" in tmp:
                                    if "conditional" in tmp:
                                        tmp = ["infinitive"]  # something weird going on
                                        print "weird situation"
                                    else:
                                        tmp = ["indicative"]  # (assume indicative)
                                elif "present" in tmp and "past-historic" in tmp:
                                    tmp = ["present"]
                                elif "adjx" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "cleft" in tmp and "estceaux" in tmp:
                                    tmp = ["estceaux"]
                                elif "causative" in tmp:
                                    tmp = ["causative"]  # assume causative dominates
                                else:
                                    print "ambig1", tmp
                            #print "tmp", tmp
                            if len(tmp) > 0:
                                verbinfo[f.get("name")] = tmp[0]
                    elif f.get("name") == "xarg":
                        #print "xarg yoy"
                        miniverbinfo = []
                        for fs2 in f.findall('fs'):
                            #print "fs2"
                            for f2 in fs2.findall('f'):  # "case", "lex"
                                #print "f2"
                                if f2.get("name") not in ["gender", "number"]:
                                    #print "f2 name"
                                    for val2 in f2.findall('val'):
                                        miniverbinfo.append(val2.text.strip())
                        #print "mini info", miniverbinfo
                        if len(miniverbinfo) > 0:
                            verbinfo[f.get("name")] = "_".join(miniverbinfo)
                if len(verbinfo) > 0:
                    if changetoinfintive:
                        verbinfos.append(["infinitive"] + verbinfo[1:])
                    else:
                        verbinfos.append(verbinfo)
            if op.get("deriv") in verb_ds:
                verb, cluster = verb_ds[op.get("deriv")]
                verb2info[verb] = verbinfos
            elif op.get("deriv") in aux_ds:
                aux, cluster = aux_ds[op.get("deriv")]
                verb2info[aux] = verbinfos

    if wordsbeforemainverb is None:
        # there is no verb:
        wordsbeforemainverb = -1
    # print "words before main verb", wordsbeforemainverb
    # exit(10)

    # 'W' nodes are 'words' which can include multiple tokens, e.g. 'bien que' is one word
    # .iter for recursive, .findall for depth of 1
    # id the cluster then get the lex element from the cluster (we'll process it later)
    # also correct the encodings and remove epsilons
    # todo is this now redundant?
    wordsforms = [(x.attrib['lemma'], x.attrib['form'], x.attrib['cluster'],
                   fixMixedEncodings(tree.findall("cluster[@id='" + x.attrib['cluster'] + "']")[0].attrib["lex"]))
                  for x in tree.iter('node') if len(x.get('lemma')) > 0 and x.get('lemma') != "_EPSILON"]
    if debug:
        print "wordsforms"
        print wordsforms

    #print "xml", verb2info
    outinfo = {
        "tok2finalforms": tok2finalforms,
        "tok2lemmacats": tok2lemmacats,
        "verb2info": verb2info,
        "trees": trees,
        "weightperword": weightperword,
        "minweight": minweight,
        "wordsbeforemainverb": wordsbeforemainverb,
        "parsemode": parsemode,
        "wordforms": wordsforms,
    }
    return outinfo
