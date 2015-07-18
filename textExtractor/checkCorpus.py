#!/usr/bin/python
__author__ = 'nparslow'

import os
import sys
import re

students = {}
filesizes = {}

def analyse( path ):
    if os.path.isdir(path):
        for element in os.listdir(path):
            analyse(os.path.join(path, element))
    else:
        analyseFile(path)


def analyseFile( filename ):
    basefilename = os.path.splitext(os.path.basename(filename))[0]
    corpus, year, time, location, level, activity, surname, firstname = basefilename.split("_",7)
    print year, activity, surname, firstname
    if (surname, firstname) not in students: students[(surname, firstname)] = []
    year = int(year)
    level = int(level)
    activity = int(re.search(ur'\d+', activity, flags=re.UNICODE).group())
    students[(surname, firstname)].append( (year, level, activity))

    size = (int(os.path.getsize(filename)))
    if size not in filesizes: filesizes[size] = []
    filesizes[size].append(filename)


inpath = u"/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_ECRIT_VALETOPOULOS/CORPUS_CENTRE-FLE"
#analyseDirectory(inpath, ".")
analyse(inpath)

for student in sorted(students.keys()):
    print student, students[student], len(students[student])

for i in range(1,7):
    print "i is", i
    x = [(student, students[student]) for student in students if len(students[student])==i]
    print len(x)
    print x
    print

for size in filesizes:
    if len(filesizes[size]) > 1:
        print filesizes[size]