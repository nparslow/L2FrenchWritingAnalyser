# coding=utf-8
import codecs
import os

__author__ = 'nparslow'


import xml.etree.cElementTree as ET

path = "/home/nparslow/Documents/AutoCorrige/CEFLE/longitudinal"
for filename in os.listdir(path):
    tree = ET.parse(path + "/" + filename)

    root = tree.getroot()

    all_text = ""
    last_was_apostrophe = True # will put no space after a punct
    for child in root:
        # although punctuation is recognised, " is classed as ambiguous
        # add a space before punctuation: (or maybe use regex to search for alphanumeric first char?)
        if not last_was_apostrophe and child.attrib["class"] != "punct" and child.text not in  [ u'´', "'"]:
            all_text += " "

        last_was_apostrophe = child.text in [ '"', u'´', "'"]

        all_text += child.text
        #print child.text, child.attrib

    outfilename = os.path.splitext(filename)[0] + ".txt" # replace the .xml with .txt


    print all_text

    with codecs.open(path + "/" + outfilename, 'w', "utf-8") as of:
        of.write(all_text)