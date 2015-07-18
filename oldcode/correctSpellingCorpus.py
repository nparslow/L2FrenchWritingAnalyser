# coding=utf-8
__author__ = 'nparslow'

'''
THIS DIDN'T WORK AT ALL
so I did search and replace in a text editor instead
'''

import re, collections, codecs
import xml.etree.cElementTree as ET

with codecs.open("/home/nparslow/Documents/AutoCorrige/SpellChecker/corpus.html", encoding="latin-1") as f:
    content = f.read()
    content.decode('latin-1')
    content.encode('utf-8')
    #re.sub(ur'ï¿œ', u'ê', content)
    re.sub(r'Ã©', ur'é', content)
    re.sub(ur'Ã´', ur'ô', content)
    re.sub(ur'Ã¨', ur'è', content)
    re.sub(ur'Ãª', ur'ê', content)
    re.sub(ur'Ã¹', ur'ù', content)
    re.sub(ur'Ã»', ur'û', content)
    re.sub(ur'Ã¢', ur'â', content)
    re.sub(ur'Ã§', ur'ç', content)
    re.sub(ur'Ã«', ur'ë', content)
    re.sub(ur'Ã¯', ur'ï', content)
    re.sub(ur'Ã®', ur'î', content)
    re.sub(ur'Ã ', ur'à', content)

    print content

'''
    ÃŽ ô
    Ãš è
    Ã  à
    Ãª ê
    Ã¹ ù
    Ã À
    Ã Ç
    Ã É

'''