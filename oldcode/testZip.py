__author__ = 'nparslow'

import zipfile

direc = "/home/nparslow/Documents/AutoCorrige/Corpora/"
zipfilename = "CORPUS ECRIT VALETOPOULOS.zip"

zf = zipfile.ZipFile(direc + zipfilename, 'r')

for element in  zf.namelist()[:3]:
    print element
    print element.decode("CP437")
