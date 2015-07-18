#!/usr/bin/python
import codecs
import os
import sys
import subprocess
import json

__author__ = 'nparslow'


if len(sys.argv) > 4: # first argument is always the name of the script
    print "Usage: ./corpusLoop base_directory measure output_filename"
    print "where measure is vocd or mtld, this will be prefixed to the outfile name with _"
    print "e.g. corpusLoop /home/nparslow/Documents/fouille_de_textes/projet/lund/all vocd trans_results.txt"
    exit(1)

path = "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_CEFLE"
if len(sys.argv) > 1:
    path = sys.argv[1]

#measure = "vocd"
measure = "mtld"
if len(sys.argv) > 2:
    measure = sys.argv[2]

outfilename = measure + "_" + os.path.basename(path) # note don't have a / at the end of path for this to work correctly!!!!
if len(sys.argv) > 3:
    outfilename = measure + "_" + sys.argv[3]

def analyse( path, results ):
    if os.path.isdir(path):
        for element in os.listdir(path):
            full_element = os.path.join(path, element)
            analyse(full_element, results)
    elif os.path.isfile(path):
        analyseFile(path, results)


def analyseFile( path, results ):
    # might be better to use subprocess.Popen() (as can use parallel)
    #os.system("/home/nparslow/Documents/AutoCorrige/vocabulary/perl/getVOCD.pl " + filename)
    #full_filename = path + "/" + filename
    result = None
    if measure.lower() == "vocd":
        result = subprocess.check_output(
            ["/home/nparslow/Documents/AutoCorrige/vocabulary/perl/getVOCD.pl", path])
    elif measure.lower() == "mtld":
        result = subprocess.check_output(
            ["/home/nparslow/Documents/AutoCorrige/vocabulary/perl/getMTLD.pl", path])
    name = os.path.splitext(path)[0] # removes the last dot extention, ie. .txt
    name = os.path.basename(name) # removes the directory structure, (so make sure filenames are unique)
    results[name] = float(result)



results = {}
analyse(path, results)

outfilepath = os.path.join("/home/nparslow/Documents/AutoCorrige/Corpora/vocabulary/", outfilename)
with codecs.open(outfilepath, mode='w', encoding="utf8") as outfile:
    json.dump(results, outfile)
#json.dump(results, open("/home/nparslow/Documents/AutoCorrige/vocabulary/perl/vocd_results.txt"))