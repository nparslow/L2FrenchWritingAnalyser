#!/usr/bin/python
__author__ = 'nparslow'

import os
import sys
import json
import re
import subprocess


if len(sys.argv) != 2: # first argument is always the name of the script
    print len(sys.argv)
    print("Usage: ./corpusLoopXML  script_to_call") # script to call takes a student_name as input param
    print("e.g. corpusLoopXML  /home/nparslow/Documents/AutoCorrige/vocabulary/perl/getVariety.pl")
    exit(1)
#inpath = sys.argv[1]
#outpath = sys.argv[2]
#script = " ".join(sys.argv[1:])
script = sys.argv[1]

inbasepath = "/home/nparslow/Documents/fouille_de_textes/projet/lund/frmgXml"

def analyseDirectory( inbasepath, results_msp, results_dt, results_dl ):
    # it's a directory:
    for element in os.listdir(inbasepath ):
        in_full_element = inbasepath + os.sep + element # note don't use 'pathsep' as it's a colon

        if os.path.isfile(in_full_element):
            analyseFile(in_full_element, results_msp, results_dt, results_dl  )
        else:
            # analyse the directory
            analyseDirectory(in_full_element, results_msp, results_dt, results_dl  )

# doesn't overwrite output
def analyseFile( filename, results_msp, results_dt, results_dl ):
    basefilename = os.path.split(filename)[-1]
    #print basefilename
    student = re.search(r"(?<=FRMG)\w+(?=Sentence\d+\.xml)", basefilename).group(0)
    if student not in results_msp:
        output = subprocess.check_output([script, student]).strip()
        #print output.split("\t")
        '''
        msp, id = output.split("\t")
        msp = float(msp)
        id = float(id)
        results_msp[student] = msp
        if id > -1: # -1 will occur if there is less than 50 lemmas recognised in the text, so don't retain it (?)
            results_id[student] = id
        '''
        msp, dt, dl = output.split("\t")
        msp = float(msp)
        dt = float(dt)
        dl  = float(dl)
        results_msp[student] = msp
        if dt > -1 : # -1 will occur if there is less than 50 tokens recognised in the text, so don't retain it (?)
            results_dt[student] = dt
        if dl > -1 : # -1 will occur if there is less than 50 lemmas recognised in the text, so don't retain it (?)
            results_dl[student] = dl


results_msp = {}
results_dl = {}
results_dt = {}

analyseDirectory(inbasepath, results_msp, results_dt, results_dl)

print results_msp
print results_dt

outfilename = "/home/nparslow/Documents/fouille_de_textes/projet/lund/diversityVarietyMSP.json"
with open(outfilename, 'w') as outfile:
    json.dump(results_msp, outfile)

outfilename = "/home/nparslow/Documents/fouille_de_textes/projet/lund/diversityVarietyDT.json"
with open(outfilename, 'w') as outfile:
    json.dump(results_dt, outfile)

outfilename = "/home/nparslow/Documents/fouille_de_textes/projet/lund/diversityVarietyDL.json"
with open(outfilename, 'w') as outfile:
    json.dump(results_dl, outfile)