import codecs
import os
import re
import gensim
import Sentence
import calcPLex
import nGramModel
import optionsFileReader
import Text
from queryLexique380 import loadLexiqueToDict

__author__ = 'nparslow'

# from the corpus directory, base filename (w/o extension) [can include directory structure] and sentence number
# create the strings for the processed sentence file and the processed token file
# note baseFileName is used twice, once for the directory, once for the file
def getProcessedSentenceFilePaths(corpus, meltDir, baseFileName, sentenceNum):
    baseFileName = os.path.basename(baseFileName)

    path1 = sentenceNum/1000000
    path2 = (sentenceNum%1000000)/10000
    path3 = (sentenceNum%10000)/100

    processedPath = os.path.join(corpus, baseFileName, str(path1), str(path2), str(path3) )
    baseProcessedSentenceFile = os.path.join(processedPath, baseFileName + ".E" + str(sentenceNum))
    processedDepXMLFile = baseProcessedSentenceFile + ".dep.xml"
    processedTokenFile = baseProcessedSentenceFile + ".tokens"
    processedLogFile = baseProcessedSentenceFile + ".log"
    processedMEltFile = os.path.join(meltDir, baseFileName + ".E" + str(sentenceNum) + ".melted")
    return processedDepXMLFile, processedTokenFile, processedLogFile, processedMEltFile

# if possible returns the setence from the input info, if not possible, returns None
def getNextSentence( corpus, meltDir, baseFileName, sentenceNum, debug=False ):
    if debug: print "Getting Next Sentence, number:", sentenceNum
    processedDepXMLFile, processedTokenFile, processedLogFile, processedMEltFile  = \
        getProcessedSentenceFilePaths(corpus, meltDir, baseFileName, sentenceNum)
    # require either a melt file or a parse to proceed
    # note: due to a bug in frmg: do not test if a log file is there, as often one is produced for an 'N+1'th
    # sentence which doesn't exist
    if os.path.isfile(processedTokenFile) or os.path.isfile(processedMEltFile):
        return Sentence.Sentence(processedDepXMLFile, processedTokenFile, processedLogFile, processedMEltFile, debug)
    else:
        return None






#allpossibleresults = {'ok', 'robust', 'corrected'}
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

# get the properties of a document
# ngram info is a 3-tuple with (ngramdict, nmogramdict, totalcounts) # nmo = n-1
#def getDocumentProperties(resource2filename, variables, word2vecModel, ngramInfo, debug=False):
def getDocumentProperties(resource2filename, variables, debug=False):

    #text = Text([])
    paragraphs = [0]
    sentences = []

    baseFileName, extension = os.path.splitext(resource2filename["filename"])
    baseDir, baseFileName = os.path.split(baseFileName)

    #processedLogFile = baseFileName + ".log"
    #ddagfile = os.path.join(filenameResources["ddagdir"], os.path.basename(baseFileName) + ".ddag")

    #print corpus, processedLogFile
    print
    print "file:", resource2filename["filename"]



    #nGramDict, nmoGramDict, nGramCounts = ngramInfo

    sentenceNum = 1
    currentSentence = getNextSentence(resource2filename["frmgeddir"],
                                      resource2filename["melteddir"],
                                      baseFileName, sentenceNum, debug=debug)
    #currentSentence.addLexiqueInfo()

    while currentSentence is not None:
        sentences.append(currentSentence)
        sentenceNum += 1
        currentSentence = getNextSentence(resource2filename["frmgeddir"],
                                      resource2filename["melteddir"],
                                      baseFileName, sentenceNum, debug=debug)

    text = Text.Text( variables, resource2filename, sentences, debug=debug )

    '''
    paragraphLengths = [len(x.sentences) for x in text.paragraphs]
    print "all paragraphs:        ", paragraphLengths
    print "sum of para lengths:   ", sum(paragraphLengths)
    print "last real sentence:    ", sentenceNum -1
    print "expected no. sentences:", len(parsinginfos)
    if len(parsinginfos) != sum(paragraphLengths):
        print "PROBLEM!!!!!"
    '''


    #lexiqueDict = {}
    #loadLexiqueToDict(u"/home/nparslow/Documents/AutoCorrige/tools/Lexique380/Bases+Scripts/Lexique380.txt",
    #                  lexiqueDict)
    #print type(lexiqueDict)
    #text.addLexiqueInfo( lexiqueDict)
    #print "paras", text.paragraphs

    return text


# outfilepath : directory where outfile will go
# corpusname : will be used as a title and for the filename so choose wisely!
# header info : information to put in the header (can be split into lines separated by \n)
# should not include any %, @ signs
# varnametypes = list of 2-tuples (variable_name, type)
# [type can be NUMERIC, string, date or class (class not implemented atm) ]
# rows = list of lists each sublist = a row of info in the same order as the varnames
def savetoArff( outfilepath, corpusname, headerInfo, varnametypes, rows, levelAsClass=False):

    # todo need to add a class bit in the attribute part and convert the relevent column to a non-numeric

    # keep track of all levels as we'll need them for the variable declaration
    allLevels = set([])
    if levelAsClass:
        # we need to find the level indicator and change it to a class element:
        j_to_change = None
        for j_var in range(len(varnametypes)):
            if varnametypes[j_var][0] == "level":
                j_to_change = j_var
                break
        # now change the int value to a string in the rows:
        # as they are tuples, need to work a bit
        for i_row in range(len(rows)):
            allLevels.add(str(rows[i_row][j_to_change]))
            newrow = list(rows[i_row])
            newrow[j_to_change] = str(newrow[j_to_change])
            rows[i_row] = tuple(newrow)

    with codecs.open(os.path.join(outfilepath, corpusname + ".arff"), mode="w", encoding="utf8")as arfffile:
        for headerline in headerInfo.split("\n"):
            arfffile.write("% " + headerline + '\n')
        arfffile.write("@RELATION " + corpusname + '\n')
        arfffile.write('\n')

        for attribute, attributetype in varnametypes:
            if levelAsClass and attribute == "level":
                arfffile.write("@ATTRIBUTE class" +"\t" + "{" + ",".join(allLevels) +  "}")
            else:
                arfffile.write("@ATTRIBUTE " + attribute + "\t" + attributetype + '\n')
        arfffile.write('\n')
        arfffile.write("@DATA" + '\n')
        for row in rows:
            arfffile.write(",".join([unicode(x) if type(x) != unicode else x for x in row])+'\n')



def savetoTreeArff( outfilepath, corpusname, headerInfo, varnames, rows, levelAsClass=False):

    # todo need to add a class bit in the attribute part and convert the relevent column to a non-numeric

    # keep track of all levels as we'll need them for the variable declaration
    allLevels = set([])
    if levelAsClass:
        # we need to find the level indicator and change it to a class element:
        j_to_change = None
        for j_var in range(len(varnames)):
            if varnames[j_var] == "level":
                j_to_change = j_var
                break
        # now change the int value to a string in the rows:
        # as they are tuples, need to work a bit
        for i_row in range(len(rows)):
            allLevels.add(str(rows[i_row][j_to_change]))
            newrow = list(rows[i_row])
            newrow[j_to_change] = str(newrow[j_to_change])
            rows[i_row] = tuple(newrow)

    with codecs.open(os.path.join(outfilepath, corpusname + ".arff"), mode="w", encoding="utf8")as arfffile:
        for headerline in headerInfo.split("\n"):
            arfffile.write("% " + headerline + '\n')
        arfffile.write("@RELATION " + corpusname + '\n')
        arfffile.write('\n')

        for attribute in varnames:
            if levelAsClass and attribute == "level":
                arfffile.write("@ATTRIBUTE class" +"\t" + "{" + ",".join(allLevels) +  "}")
            else:
                arfffile.write("@ATTRIBUTE " + str(attribute) + "\t" + "{0,1}" + '\n')
        arfffile.write('\n')
        arfffile.write("@DATA" + '\n')
        for row in rows:
            arfffile.write(",".join([unicode(x) if type(x) != unicode else x for x in row])+'\n')


def allCorpusFiles( listbasepaths ):
    corpusFiles = []
    for path in listbasepaths:
        if os.path.isdir( path ):
            # os.listdir doesn't give the full path, so add it
            corpusFiles.extend( allCorpusFiles([os.path.join(path, x) for x in os.listdir(path)]) )
        else:
            corpusFiles.append( path )
    return corpusFiles

def variableAndParamsToString(variable, params):
    # link with underscores after removing any .s
    if len(params) > 0:
        return variable + "_" + "_".join( re.sub(ur'\.', '', str(x)) for x in params)
    # as we need the extra "_"
    return variable

def main():
    # todo add a debug variable and optionfilename variable

    optionsfilename = "settings/optionsfile.txt"
    globalparams, variableparams = optionsFileReader.readOptionsFile(optionsfilename)
    filenames = allCorpusFiles( globalparams["origtextdir"] )
    print filenames
    # todo for the moment we just take the first element for these
    #meltDir = globalparams["melteddir"][0]
    #ddagDir = globalparams["ddageddir"][0]
    #frmgDir = globalparams["frmgeddir"][0]
    filenameResources = {
        "filename": None,
        "melteddir" : globalparams["melteddir"][0],
        "ddageddir" : globalparams["ddageddir"][0],
        "frmgeddir" : globalparams["frmgeddir"][0],
    }

    print globalparams
    outarffdir = globalparams["outdir"][0]
    corpusName = globalparams["corpusName"][0]
    headerInfo = globalparams["headerInfo"][0]
    lexiquefile = globalparams["lexiqueDict"][0]

    gensimModelFile = globalparams["word2vecmodel"][0]

    variableTypes = set([x[0] for x in variableparams])

    lemmacat2freqrank = {}
    if "PLex" in variableTypes or "S" in variableTypes or "altS" in variableTypes or "LFP" in variableTypes:
        print "loading freq info"
        lemmacat2freqrank = calcPLex.loadLemmaCat2freqrank()

    word2vecModel = None
    if "w2vct" in variableTypes:
        print "loading word2vec model"
        word2vecModel = gensim.models.Word2Vec.load(gensimModelFile)

    nGramDict, nmoGramDict, totalcounts = {}, {}, 1000000000000000
    if "bigramLogProb" in variableTypes:
        print "loading bi-gram model"
        ngramModelFile = globalparams["bigrammodel"][0]
        nGramDict, nmoGramDict, totalcounts = nGramModel.getNgramDicts(ngramModelFile)

    lexiqueDict = {}
    if "syllablesPerWord" in variableTypes:
        loadLexiqueToDict(lexiquefile, lexiqueDict)

    # create a list of variables for the arff file:
    variables = [ ("filename", "string")] + \
        [ (variableAndParamsToString(vname, params), "numeric") for vname,params in variableparams] + \
        [ ("level", "numeric")] # note that level must go last!

    for x in variables:
        print x

    #filenames = ["/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_CEFLE/C/Catja.txt"]
    #filenames = ["/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_CEFLE/A/Arvid.txt"]
    #filenames = ["/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_CEFLE/A/Amie4.txt"]
    #filenames = ["/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_CEFLE/B/Bror2.txt"]
    filenames = ["/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_CEFLE/C/Caroline.txt"]
    filenames = ["/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_CEFLE/E/Eddy.txt"] # just to test an E


    resources = {
        "lemmacat2freqrank": lemmacat2freqrank,
        "word2vecModel": word2vecModel,
        "nGramDict": nGramDict,
        "nmoGramDict": nmoGramDict,
        "nGramCounts": totalcounts,
        "lexiqueDict": lexiqueDict
    }

    outputRows =[]


    allobservedtrees = set([])
    treespertext = []
    for filename in filenames:

        # we change the resouce filename with each round:
        filenameResources["filename"] = filename
        baseFileName = os.path.basename(filename)
        baseFileName, extension = os.path.splitext(baseFileName)
        filenameResources["ddagfile"] = os.path.join(filenameResources["ddageddir"],
                                                         os.path.basename(baseFileName) + ".ddag")

        print
        print filename
        #fname = os.path.join(baseDir, filename)
        #if "CEFLE" in baseDir:
        #    fname = os.path.join(baseDir, filename[0], filename)

        #text = getDocumentProperties(frmgDir, meltDir, ddagDir, fname, word2vecModel,
        #                             (nGramDict, nmoGramDict, totalcounts), debug=False)
        #text = getDocumentProperties(filenameResources, variables, word2vecModel,
        #                             (nGramDict, nmoGramDict, totalcounts), debug=False)
        text = getDocumentProperties(filenameResources, variableparams, debug=False)

        text.calcVariables( resources )

        for i in range(len(variableparams)+1):
            #variable, params = variableparams[i]
            varlabel = variables[i]
            # squeeze the filename in first:
            value = filename
            if i > 0:
                value = text.variablevalues[i-1]
            print varlabel, "\t", str(value)
        print 'level', "\t", text.level

        allobservedtrees.update(text.trees.keys())
        treespertext.append( (set(text.trees.keys()), text.level) )
        #print "mwpw", text.getMeanWeightPerWord()
        outputRows.append( [baseFileName] + text.variablevalues + [text.level] )


    savetoArff(outarffdir, corpusName, headerInfo, variables, outputRows )
    savetoArff(outarffdir, corpusName + "class", headerInfo, variables, outputRows, levelAsClass=True )

    arfftreefile = "testtrees"
    #corpusName = "test"
    #headerInfo = "a test corpus\n of stuff"
    treevariables = list(allobservedtrees)
    #print allobservedtrees
    #print treespertext
    treeoutputRows = [[1 if x in trees else 0 for x in treevariables] + [level] for trees, level in treespertext]
    treevariables.append("level")
    #print "ntrees", len(treevariables)
    #for a,b in zip(treevariables, treeoutputRows):
    #    print a,len(b), b

    savetoTreeArff(outarffdir, arfftreefile, headerInfo, treevariables, treeoutputRows, levelAsClass=True )


    #print "possible results", allpossibleresults





if __name__ == "__main__":
    main()
