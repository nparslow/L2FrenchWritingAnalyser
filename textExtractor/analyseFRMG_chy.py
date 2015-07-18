# -*- coding: utf-8 -*-
# note, if you put an encoding here, the program will crash, as the std in/out used in os will use this instead
# of ascii, I don't have a good way to fix it

__author__ = 'nparslow'

import json
import os
import codecs
import chardet
import re



# keep track of the results and students found
results = {}
students = {}


def analyseDirectory( path, results ):

    for element in os.listdir(path):

        full_element = path + '/' + element
        if os.path.isfile(full_element): # only analyse .txt files

            filenamebase, filenameextension = os.path.splitext(element) # remove the extention
            # only analyse .out files:
            if filenameextension == ".out":
            #if filenameextension == ".txt":
                level, analysed = analyseFile(path, element) # analysed should be a 5-tuple
                if level not in results: results[level] = {}
                # for the moment we don't do any further decomposition of the filename, though we could
                results[level][filenamebase] = analysed

        else:
            # it's a directory:
            results[element] = {}
            analyseDirectory(full_element, results[element])


def analyseFile( path, filename ):
    # might be better to use subprocess.Popen() (as can use parallel)
    #os.system("/home/nparslow/Documents/AutoCorrige/vocabulary/perl/getVOCD.pl " + filename)
    level = splitFilename(filename)

    full_filename = path + "/" + filename
    #return level, get_parse_counts(full_filename)
    #return level, doNothing(full_filename)
    return level, get_parse_counts(full_filename)


# takes a filename in corpus ChyFLE format and extracts the level info from it
def splitFilename( filename ):
    level = 0
    firstname = None
    surname = None
    # strip the extension:
    filename, fileExtension = os.path.splitext(filename)
    # need to have max no. of splits as some first names are double with a '_' in between
    if filename.startswith("centreFLE"):
        subcorpus, year, timeconstraint, place, levelPlacement, activity, surname, firstname = filename.split("_", 7)
        attempt = 1 # for one activity, one student has 2 attempts
        if re.search( ur'\d+$', firstname, flags=re.UNICODE):
            firstname, attempt = firstname.rsplit('_', 1)
        level = placement2CEFR(levelPlacement)
        activity = activity.replace("Activite", "")
    elif filename.startswith("hellasFLE"):

        subcorpus, year, timeconstraint, place, levelTest, activity, candidateID = filename.split("_", 6)
        level = convertCEFR2number(levelTest)
        activity = activity.replace("Activite", "")
        candidateID = candidateID.replace("candidat", "")
    elif filename.startswith("chyFLE"):
        print filename.split("_")
        subcorpus, year, timeconstraint, place, levelYear, activity, firstname, surname = filename.split("_", 7)
        # surname, name is not very consistent for this subcorpus
        if firstname.isupper(): # not sure which is which if both are uppercase ...
            firstname, surname = surname, firstname
        level = year2CEFR(levelYear)
    if surname:
        if surname.lower() not in students: students[surname.lower()] = []
        students[surname.lower()].append(firstname.lower())
    return level


def year2CEFR( levelYear):
    # Les étudiants de l'Université de Chypre ont à priori un niveau entre B1.1. et B1.2.
    if levelYear == "1A":
        return convertCEFR2number("B1")
    elif levelYear == "4":
        return convertCEFR2number("B2")
    else:
        raise("Unknown school year "+ levelYear)

# convert a 2-character CEFR string to a number in the range 1-6
def convertCEFR2number(levelString):
    if levelString == "A1":
        return 1
    elif levelString == "A2":
        return 2
    elif levelString == "B1":
        return 3
    elif levelString == "B2":
        return 4
    elif levelString == "C1":
        return 5
    elif levelString == "C2":
        return 6
    else:
        raise("Unknown CEFR level " + levelString)

# converts a placement level to a CEFL level (as an integer 1-6)
# TODO find out what corresponds to what
def placement2CEFR( levelPlacement ):
    #if levelPlacement == "1":
    #    return 1
    #elif levelPlacement == "2":
    #    return 2
    #elif levelPlacement == "3":
    #    return 3
    if levelPlacement == "4":
        return convertCEFR2number("B1")
    elif levelPlacement == "5":
        return convertCEFR2number("B2")
    elif levelPlacement == "6":
        return convertCEFR2number("C1")
    elif levelPlacement == "7":
        return convertCEFR2number("C2")
        # todo unknown, but we assume higher than placement level 6, so either C1(high) or C2
    else:
        raise("Unknown placement level " + levelPlacement)


# looks at an xml-like version of frmg's output and returns a five-tuple of info:
def get_parse_counts( pathfilename ):
    nSentences = 0                      # total no. of sentences
    nSentencesSolution = 0              # total no. of sentences successfully parsed
    nSentencesSolutionCorrected = 0     # total no. of sentences successfully parsed by using a correction
    nNoSolutionFull = 0                 # total no. of sentences with no found solution
    nNoSolutionCorr = 0                 # total no. of sentences with no found solution even with a correction used

    nLineBreaks = 0                     # total no. of \n between sentences (so actually less than the total \n)
                                        # estimated by each reset of EX to E1
    nParagraphs = 0                     # estimated by each reset of EX to E1 at least passing by E2 (but will ignore
                                        # double \n ... e.g. Ben: "blah", Bill "blah" \n\n Bill a vu ... would be 1 para)

    with codecs.open(pathfilename, "r", "latin-1") as infile:

        sentence_tokens = []
        for line in infile:
            line = line.rstrip()
            #print line
            if line.startswith("<token>"):
                splitLine = line.split()
                print line, pathfilename, len(splitLine)
                tokenlabel, tokenNum, token = None, None, None
                if len(splitLine) == 3:
                    tokenlabel, tokenNum, token = splitLine
                elif len(splitLine) == 2:
                    # this maybe happens with amalgames, eg. 'du' which in effect has 2 tokens merged into 1
                    tokenlabel, tokenNum = splitLine

                print tokenlabel, tokenNum, token
                sentNum = re.match(r'E(\d+)F(\d+)', tokenNum).groups(0)[0]
                print sentNum, token
            # for no solution found:
            # mode=corrected best=no
            # otherwise mode=full best=yes or mode=corrected best=yes
            #if line.startswith("## sentence="):
            elif "Sentence id=" in line:
                nSentences += 1
                #print "last chars", line[-1]
                #if line.endswith("best=yes"):
                if 'best="yes"' in line:
                    #print "yo"
                    nSentencesSolution += 1
                    if u'mode="corrected"' in line:
                        nSentencesSolutionCorrected += 1
                #elif line.endswith("best=no"):
                elif 'best="no"' in line:
                    if u'mode="full"' in line:
                        nNoSolutionFull += 1
                    elif u'mode="corrected"' in line:
                        nNoSolutionCorr += 1
                    else:
                        print "Warning: strange (inner) line: ", line
                else:
                    print "Warning: strange (outer) line: ", line
                # reset the token list
                sentence_tokens = []



    #print nSentences, nSentencesSolution, nSentencesSolutionCorrected
    #print round(1.0* nSentencesSolution/nSentences, 2), round(1.0* nSentencesSolutionCorrected/nSentences, 2)
    return nSentences, nSentencesSolution, nSentencesSolutionCorrected, nNoSolutionFull, nNoSolutionCorr

basedir = '/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_ECRIT_VALETOPOULOS/'
#basedir = '/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_ECRIT_VALETOPOULOS/'

analyseDirectory(basedir, results)
print results

outfilename = u"chy_parse_tally.out"
baseoutdir = u"/home/nparslow/Documents/AutoCorrige/Corpora/outputs/"
#with open("/home/nparslow/PycharmProjects/DownloadCEFLE/" + outfilename, 'w') as outfile:
with open(baseoutdir + outfilename, 'w') as outfile:
    json.dump(results, outfile)


'''
# checking for misnamed files (where surname is written in place of firstname)
for surname in students:
    print surname, students[surname]
    for firstname in students[surname]:
        if firstname in students:
            print "possible problem", firstname
'''