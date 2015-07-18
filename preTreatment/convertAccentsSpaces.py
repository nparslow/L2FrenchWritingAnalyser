__author__ = 'nparslow'

import unidecode
import os


# convert the filename to utf-8
# replace spaces by underscores
# remove brackets
def modifyPath( basepath, path ):

    newfilename = path

    #print type(path), path
    if type(path) == unicode:
        newfilename = unidecode.unidecode(path)

        newfilename = newfilename.encode('utf-8')
        #print "new file name", type(newfilename)

    newfilename = newfilename.replace(" ", "_")
    newfilename = newfilename.replace("(", "")
    newfilename = newfilename.replace(")", "")
    #newfilename = newfilename.replace("ActivitA", "Activite")
    #newfilename = newfilename.replace("Activit?", "Activite")
    #newfilename = newfilename.replace("Activit-", "Activite")

    #newfilename = newfilename.replace("Activit", "Activite")
    #newfilename = newfilename.replace("Hlne", "Helene")

    print newfilename #, type(newfilename)

    full_old_path = basepath + "/" + path
    full_new_path = basepath + "/" + newfilename



    if not os.path.exists(full_new_path):
        try:
            #print full_old_path
            os.rename(full_old_path, full_new_path)
        except TypeError :
            print "TypeError for:", full_old_path
        except OSError:
            print "OSerror for:", full_old_path
    else:
        #raise("must overwrite file! " + path)
        if not full_old_path == full_new_path:
            print "file already exists, skipping:", newfilename
    return newfilename


def modifyDir( basepath, path ):

    newfname = modifyPath(basepath, path)
    new_full_path = basepath + "/"+ newfname
    # it's a directory, so recurse:
    if os.path.isdir( new_full_path ):
        for subfiledir in os.listdir(new_full_path):

            modifyDir( new_full_path, subfiledir )

#basepath = u"/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_ECRIT_VALETOPOULOS/"
#basepath = u"/home/nparslow/Documents/AutoCorrige/Corpora/analysed_CORPUS_ECRIT_VALETOPOULOS/"
basepath = u"/home/nparslow/Documents/AutoCorrige/Corpora/"
path = u"CORPUS ECRIT VALETOPOULOS/"
modifyDir(basepath, path)