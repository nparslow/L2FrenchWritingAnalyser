# coding=utf-8
import re
import os

__author__ = 'nparslow'


# in this .py:
# ways to read filenames from the various corpora and get the relevant info from them:


# designed to be applied to the text .log files, might work for others though
def getCorpusInfo(filename):
    # first we need to work out which corpus it is (CEFLE, CHY or FIPSORTHO)
    # split off the extention, and reduce to the basename
    base, ext = os.path.splitext(filename)
    base = os.path.basename(base)

    level = None
    if base.startswith("entry_"):
        # we are in the original part of the FipsOrtho
        level = splitFilenameFipsOrtho(base)
    elif base.startswith("entrycorrected_"):
        # we are in the corrected part of FipsOrtho
        level = splitFilenameFipsOrtho(base)
    elif base.startswith("centreFLE"):
        # we are in centre FLE
        level = splitFilenameCHY(base)
    elif base.startswith("hellasFLE"):
        # we are in hellas FLE
        level = splitFilenameCHY(base)
    elif base.startswith("chyFLE"):
        # we are in chy FLE
        level = splitFilenameCHY(base)
    elif base[0] in ["A", "B", "C", "D", "E"]:
        # we are (hopefully) in CEFLE longi or trans
        level = splitFilenameCEFLE(base)
    return level

def splitFilenameFipsOrtho(filename):
    entryNum = re.search(ur"_(\d+)", filename, flags=re.UNICODE).groups()[0]
    # since we only want the level
    return None

def splitFilenameCEFLE(filename):
    assert len(filename) > 0
    if filename[0] == "A":
        return convertCEFR2number("A1")
    elif filename[0] == "B":
        return convertCEFR2number("A2")
    elif filename[0] == "C":
        return convertCEFR2number("B1")
    elif filename[0] == "D":
        return convertCEFR2number("B2")
    elif filename[0] == "E":
        return convertCEFR2number("C2")

# takes a filename in corpus ChyFLE format and extracts the level info from it
def splitFilenameCHY( filename ):
    #students = {}
    #print "splitfilename", filename
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
    #if surname:
    #    if surname.lower() not in students: students[surname.lower()] = []
    #    students[surname.lower()].append(firstname.lower())
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
    # todo check for the longi info also
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


def main():
    # testing
    filename = "Amie1.log"
    filename = "entry_202.log"
    filename = "centreFLE_2006_TL_CFLETP_4_Activite2_LAMO_Clara.log"
    print getCorpusInfo(filename), type(getCorpusInfo(filename))





if __name__ == "__main__":
    main()