# coding=utf-8
import codecs
import re
__author__ = 'nparslow'


#note this will overwrite the orig
corpushtmlfile = "/home/nparslow/Documents/AutoCorrige/SpellChecker/errorsCorpusCorrected.html"
#newcorpushtmlfile = "/home/nparslow/Documents/AutoCorrige/SpellChecker/errorsCorpusCorrected.html"

newtext = ""
with codecs.open(corpushtmlfile, mode="r", encoding='latin1') as origfile:
    origtext = origfile.read()
    newtext = re.sub(ur'Â«', u'«', origtext, flags=re.UNICODE)
    newtext = re.sub(ur'Â»', u'»', newtext, flags=re.UNICODE)

with codecs.open(corpushtmlfile, mode="w", encoding='latin1') as newfile:
    newfile.write(newtext)