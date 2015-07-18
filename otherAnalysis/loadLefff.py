# -*- coding: utf-8 -*-
__author__ = 'nparslow'
# adapted from /home/nparslow/exportbuild/bin/serialize_lefff.py


import os
import sys
import codecs
import optparse
from collections import defaultdict
import codecs
try:
    from cjson import dumps, loads
except ImportError:
    try:
        from simplejson import dumps, loads
    except ImportError:
        from json import dumps, loads


usage = "usage: %prog [options] <input_file>"
parser = optparse.OptionParser(usage=usage)
parser.add_option("-p", "--path", action="store", help="path for dump", default="./lefff_dict.json")
(options, args) = parser.parse_args()


lefff_file = codecs.open( args[0], 'r', encoding="utf8" )


lefff_dict = defaultdict(dict)
for line in lefff_file:
    line = line.strip()
    if not line:
        continue
    splitted_line = line.split('\t')
    if len(splitted_line) >= 3:
        if len(splitted_line) == 3:
            wd, tag, lemma = tuple(splitted_line)
            val = 1
        else:
            wd, tag, lemma, val = tuple(splitted_line)
        lefff_dict[wd][tag] = val
    else:
        print >> sys.stderr, "Ignoring the following line in the lexicon:", line

def serialize(datastruct, filepath, encoding="utf-8"):
    _file = codecs.open( filepath, 'w', encoding=encoding )
    _file.write( dumps( datastruct ) )
    _file.close()
    return

serialize(lefff_dict,options.path)
