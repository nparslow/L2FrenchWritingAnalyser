# coding=utf-8
__author__ = 'nparslow'

import unicodedata
import codecs
import os
import shutil
import chardet # this didn't detect accurately at all, probably searching too many possibilities?
import re
import unidecode
import sys

# to use frmg_shell and whole corpus:
# or use the python loop script
# echo "corpus converted/CORPUS_ECRIT_VALETOPOULOS analysed_CORPUS_ECRIT_VALETOPOULOS :xml:utf8:robust:dis:transform" | frmg_shell

def printDebug(filename, line, reason, cut=False):
    print "in file           :", filename
    if cut:
        print "line beginning cut:", line.rstrip()
    else:
        print "line deleted      :", line.rstrip()
    print "because           :", reason
    print

def proposeSubstitution( line, startindex, stopindex, replacementString, do_all=False, debug=False):
    response = "y"
    searchedline = line[:stopindex]
    if not do_all:
        response = "n"
        print "User input required for line:"
        print line.rstrip()
        print "Should I replace", line[startindex:stopindex], "with", replacementString, "(y)es/(n)o (default = no)?"
        response = sys.stdin.readline().strip()
    if response == "y" or response == "yes":
        if debug: print "replacing", line[:startindex], replacementString
        searchedline = line[:startindex] + replacementString
    return searchedline




# stock all observed characters (to see if we need to replace any or if there are any strange ones)
allChars = set([])

# the equivalent in the shell is e.g.:
# iconv -f WINDOWS-1252 -t UTF-8  filename.txt
# debug will print out whever a line is skipped with a reason why
def reEncodeFile( basedir, outbasedir, filename,
                  origencoding,
                  removeActivityNumber=False,
                  removeHeadTailSectionInfo=False,
                  debug=False):

    if "LAMO_SOTELO_Clara" in filename:
        # there should be three of these
        print "ignoring double file:", filename
        return

    print "converting file:", filename, "\tusing\t", origencoding

    '''
    # try to work out the encoding:
    rawdata = open(basedir + "/" + filename, 'r').read()
    result = chardet.detect(rawdata)
    print result, "but using", origencoding
    '''

    # get the first name and surname if we can
    firstname = None
    surname = None
    # strip the extension:
    baseFilename, fileExtension = os.path.splitext(filename)
    # need to have max no. of splits as some first names are double with a '_' in between
    if removeHeadTailSectionInfo and (baseFilename.startswith('chyFLE') or baseFilename.startswith('centreFLE') ):
        subcorpus, year, timeconstraint, place, levelYear, activity, firstname, surname = baseFilename.split("_", 7)
        firstname = firstname.lower()
        surname = surname.lower()

    # get the no. of lines in the file (basically loop over it in advance)
    # +1 as last line usually has no \n:
    totalLines = 0
    with codecs.open(basedir + "/" + filename, encoding=origencoding, mode='rb') as infile:
        # note next line is not accurate on a windows encoded file! (it underestimates!!)
        #totalLines = infile.read().count("\n") + 1
        for line in infile:
            totalLines += 1

    outlines = []
    with codecs.open(basedir + "/" + filename, encoding=origencoding, mode='rb') as infile:
        lineNumber = 0

        # we potentially need to replace windows end of lines with unix ones:
        # (commented as this is taken care of elsewhere)
        #text = infile.read() #.replace('\r\n', '\n')

        for line in infile:
            #print line
            # windows to unix conversion leaves an extra char at the end of each line
            # (^M), but also somehow the carriage return is getting lost so ...
            line = line.rstrip() + "\n"

            # ad hoc conversions for
            # hellasFLE_2010_TL_KPG_B2_Activite1_candidat17
            line = line.replace(u'\x00', u"è")
            line = line.replace(u'Õ', u"'")
            line = line.replace(u'ˆ', u"à")
            line = line.replace(u'Ž', u"é")

            # 'hellasFLE_2010_TL_KPG_C1_Activite2_candidat26.txt',
            line = line.replace(u'¨º', u'ê')
            line = line.replace(u'¨¦', u'é')
            line = line.replace(u'¨¨', u'è')
            line = line.replace(u'¨´', u'ù')
            # 'zero with no-break space' appears in hellasFLE_2010_TL_KPG_C1_Activite1_candidat26.txt
            line = line.replace(u'\U0000FEFF', u'')

            # chyFLE_2011_TI_UCY_4_Autoobservation_ODYSSEOS_Maria
            line = line.replace(u'–', u'-') # not sure what is best with this one, used for 'pronunced -t'

            # should we replace tabs??

            # centreFLE_2005_TL_CFLETP_5_Activite1_CATANESE_Giovanna
            # has an underscore in a strange position

            # because of a strange  in hellasFLE_2010_TL_KPG_C1_Activite2_candidat16
            # looks like a corrupted file as other è exist in the file,
            #  though it could be ê or ë via a spelling error
            #re.sub(ur'\x8f', u'è', line)
            line = line.replace(u'\x8f', u'è')

            # there is a strange \xb7 in chyFLE_2010_TL_UCY_1A_Strategies_Rafaella_Georgiou.txt
            line = line.replace(u'\xb7', u',')

            # there can be unusual space characters: \xa0
            line = line.replace(u'\xa0', u' ')

            # replace apostrophes
            # frmg_lexer can handle: “ and  ”
            #if u'`' in line: print filename + " has " + u'`'
            #if u'´' in line: print filename + " has " + u'´'
            #if u'‘' in line: print filename + " has " + u'‘'

            line = line.replace(u'`', u"'")   # can't be (seen as an extra token)
            ##line = line.replace(u'’', u"'") # can be treated by frmg_lexer
            #line = line.replace(u'´', u"'")  # seems ok
            #line = line.replace(u'‘', u"'")   # seems ok

            # replace '…' as ' ... ' (with spaces)
            line = re.sub(ur'…', u' ... ', line)


            #if u"?" in line: print "possible phono", line.rstrip()
            '''
            searchpatterns = [
                        ur'(?<=\[)\s?(?:\S*\?\S*)+\s?(?=\])',
                        ur'(?<=/)\s?(?:\S*\?\S*)+\s?(?=/)',
                        ur'(?<=«)\s?(?:\S*\?\S*\s?)+(?=»)',
                        ur'(?<=\()\s?(?:\S*\?\S*)+\s?(?=\))',
                        ur'\?\?\?+',
                        ]
            searchpatterns = [   x +ur'\s?(?:\S*\?\S*)+\s?' + y
                                for x,y in ]
            print searchpatterns
            '''
            for x,y in [(ur'\[',ur'\]'), (ur'/',ur'/'), (ur'«',ur'»'), (ur'\(',ur'\)'), (ur'\?', ur'\?')]:
                # look for patterns within xy brackets, but no enchained/double bracketing
                searchpattern = x +ur'\s?(?:[^\s' + x + y + ur']*\?[^\s' + x + y + ur']*\s?)+\s?' + y
                unsearchedline = line
                searchedline = ""
                #print searchpattern
                while len(unsearchedline) > 0:
                    m = re.search(searchpattern, unsearchedline, flags=re.UNICODE)
                    if m is not None:
                        searchedline = searchedline +\
                                       proposeSubstitution(unsearchedline, m.start(), m.end(),
                                                           x.replace('\\', '').replace('?','') +
                                                           u" ɣ ɣ ɣ " + y.replace('\\', '').replace('?', ''),
                                                           do_all=True, debug=debug)
                        unsearchedline = unsearchedline[m.end():]
                    else:
                        searchedline += unsearchedline
                        unsearchedline = ""
                    #print "searched:  ", searchedline
                    #print "unsearched:", unsearchedline
                #print "orig line: ", line
                line = searchedline
                #print "final line:", line


            # look for unusual characters (that may indicate a bad encoding)
            for charac in line.lower():

                category = unicodedata.category(charac)
                # Ll = latin 1, Zs = Separator Space, Cc = other control characters
                # Nd = number etc. Po & Ps = Punctuation
                '''
                if category not in  ['Ll', 'Zs', 'Po', 'Nd'] \
                        and charac not in ["\n", '-', '(', ')', u'«', u'»', '[', ']', '\t', u'€', u'’', u'“', u'”']:
                    print "unexpected symbol detected in file", charac, category, ord(charac), unicodedata.name(charac),\
                        baseFilename
                    print line
                '''
                # we add our meta gamma character
                if charac not in u'abcdefghijklmnopqrstuvwxyz0123456789ùûüÿàâæçéèêëïîôœ_. \',\-!?:;[]"()/@\t\n%*€' + u'ɣ' \
                        and charac not in u'’´‘«»“”':
                    uniname = None
                    try:
                        uniname = unicodedata.name(charac)
                    except:
                        pass
                    print "unexpected symbol detected in file", charac, category, ord(charac), uniname ,\
                        baseFilename
                    print line

            # add all chars in the line to the set:
            allChars.update([x for x in line.lower()])

            '''
            # print lines with rare/unusual chars to check encoding is working ok:
            for x in [u"ã", u"ë", u"ó", u"ø", u"ü", u"…", u"õ", u"ú" ]:
                if x in line:
                    print x, line
            '''

            if re.search(ur'_', line.lower()):
            #    print "underscore:", line
                # here we make some ad hoc adjustments to avoid underscores in www links:
                line = re.sub(ur'permet_', 'permet,', line, flags=re.UNICODE)
                line = re.sub(ur'peut_', 'peut,', line, flags=re.UNICODE)
                line = re.sub(ur' _ ', ' , ', line, flags=re.UNICODE)
            #if re.search(ur'_', line.lower()):
            #    print "underscore check:", line

            # how should we treat xxx?
            if re.search(ur'xxx+', line.lower()):
                #print "xxx/XXX line:", line
                line = re.sub(ur'[xX][xX][xX]+', 'xxx', line, flags=re.UNICODE)
            #if re.search(ur'xx+', line.lower()):
            #    print "xxx/XXX line check:", line

            # if the file is one which starts with the activity number on the first line, remove it
            if removeActivityNumber and lineNumber == 0:
                if re.match(ur'\d+\.', line, flags=re.UNICODE):
                    # there is always a space after the . but just in case, we don't include it
                    if debug: printDebug(filename, line, "activity number at beginning", cut=True)
                    line = re.split(ur'\d+\.',line, maxsplit=1, flags=re.UNICODE)[1]


            # this section is often very ad hoc, removes header and footer meta-info included by the student
            if removeHeadTailSectionInfo:
                # put the line in lower case and remove accents:
                testline = line.lower()
                testline = unidecode.unidecode(testline)
                # test if the student's name is in the line, we use \b to make sure it's not by accident
                if firstname is not None and surname is not None:
                    if (re.search(ur'\b'+firstname+r'\b', testline, flags=re.UNICODE) is not None) and \
                            (re.search(ur'\b'+surname+r'\b', testline, flags=re.UNICODE) is not None):
                        if debug: printDebug(filename, line, "firstname and surname in line")
                        continue
                    if ((re.search(ur'\b'+firstname+r'\b', testline, flags=re.UNICODE) is not None) or
                        (re.search(ur'\b'+surname+r'\b', testline, flags=re.UNICODE) is not None)) and \
                        (re.search(ur'\b(pre)?nom\b', testline, flags=re.UNICODE) is not None):
                        if debug: printDebug(filename, line, 'firstname or surname + "nom" in line')
                        continue
                # look for (123 mots) with or without brackets
                if re.match(ur'^\(?\d+\s[mM]ots\)?', line, flags=re.UNICODE):
                    if debug: printDebug(filename, line, "word count in line")
                    continue
                # look for Mots : 123
                if re.match(ur'^[mM]ots\s*:\s*\d+', line, flags=re.UNICODE):
                    if debug: printDebug(filename, line, "word count in line")
                    continue
                # sometimes the question is restated:
                # it may be in quotes and may include apostrophes and accents or not
                # so we look for a section which should be relatively unique for the question:
                if lineNumber < 6 and (re.search(ur'[Jj]ustifiez vos choix', line, flags=re.UNICODE) is not None):
                    if debug: printDebug(filename, line, "exercise description in line")
                    continue
                # we require it to be at the start of the line:
                if lineNumber < 6 and (re.search(ur'^\s*([Gg]rille|[Rr]apport)\s+[Dd].[Oo]bservation', testline, flags=re.UNICODE) is not None):
                    if debug: printDebug(filename, line, "exercise description in line")
                    continue
                if lineNumber < 6 and (re.search(ur'valuation.+nregistrement.+[Uu]n [Ff]ait [Dd]ivers', line, flags=re.UNICODE) is not None):
                    if debug: printDebug(filename, line, "exercise description in line")
                    continue
                if lineNumber < 6 and (re.search(ur'[Aa]ctivit[ée]\s\d', line, flags=re.UNICODE) is not None):
                    if debug: printDebug(filename, line, "Activity description in line")
                    continue
                # the line might be just a student id at the beginning or a stray reference at the end:
                # we need up to 7 lines at the end
                #elif re.search(r'^\s*\d+\s*$', line, flags=re.UNICODE) is not None:
                #    print line
                #    print "maybe problem?"
                #    print lineNumber, totalLines
                if (lineNumber < 6 or (totalLines-lineNumber)<7) and (re.search(ur'^\s*\d+\s*$', line, flags=re.UNICODE) is not None):
                    if debug: printDebug(filename, line, "line is just a number")
                    continue
                # remove a date only line: (actually it is a bit more general)
                if (re.search(ur'^\s*(Date\s:)?\s*\d\d(\d\d)?\/\d\d(\d\d)?\/\d\d(\d\d)?\s*$', line, flags=re.UNICODE) is not None):
                    if debug: printDebug(filename, line, "line is just a date")
                    continue
                # remove any line containing the course name
                if ("GAL" in line or "Gal" in line) and "303" in line:
                    if debug: printDebug(filename, line, "line includes university subject")
                    continue
                # as a part of the header the student may put their year:
                if (re.search(ur'^\s*([Pp]remi[eè]re|(([Dd]eux|[Tt]rois|[Qq]uatr|[Cc]inq|[Ss]ix|[Ss]ept|[Hh]uit|[Nn]euv|[Dd]ix)i[èe]me))\s+[Aa]nn[ée]e\s*$',
                                line, flags=re.UNICODE) is not None):
                    if debug: printDebug(filename, line, "uni year in line")
                    continue
                # may contain teacher's name (use testline to be sure of case/accents):
                if 'freiderikos' in testline and  'valetopoulos' in testline:
                    if debug: printDebug(filename, line, "freiderikos valetopoulos (teacher) in line")
                    continue
                # reference to uni semester
                if (re.search(ur'semestre d[\w\s]+ 20\d\d', testline, flags=re.UNICODE) is not None):
                    if debug: printDebug(filename, line, "semester in line")
                    continue
                # reference to uni name:
                if (re.search(ur'^\s*universite de chypre\s*', testline, flags=re.UNICODE) is not None):
                    if debug: printDebug(filename, line, "uni name in line")
                    continue
                # remove references:
                # web:
                if (re.search(ur'^\d+\shttp\:\/\/', line, flags=re.UNICODE) is not None):
                    if debug: printDebug(filename, line, "web reference in line")
                    continue
                # book: (we say starts with a ref number and includes a year after 1800,
                # not great but hopefully strict enough ...
                if (re.search(ur'^\d+\s', line, flags=re.UNICODE) is not None) \
                    and (re.search(ur'((18|19)\d\d|20[01]\d)', line, flags=re.UNICODE) is not None):
                    if debug: printDebug(filename, line, "other reference in line")
                    continue
                # any line that is all punctuation: (\p doesn't seem to work)
                if (re.search(ur'^\s*[^\w\s]+\s*$', line, flags=re.UNICODE) is not None):
                    if debug: printDebug(filename, line, "line is just punctuation")
                    continue

            # check if this line should be concatenated with the previous one or not:
            # Sometimes paragraphs marked with a \n\n, sometimes with a space or tab at the beginning
            # Sometimes just a newline.
            # if a newline doesn't start with a space or a number and if the previous line doesn't end
            # with a punctuation, we'll join them, if there is no space at end of last line and
            #  todo Ideally : we make a word then ok, if we make a non-word then insert a space.
            #  todo         but this means dealing with - and '
            # if last line doesn't end in a .?! and next line

            # if not the first line, and this line starts with a letter (no spaces)
            if len(line) == 990: print "990 line in", filename
            if len(outlines) > 0 and re.match(ur'[^\W_\d]', line, flags=re.UNICODE):
                lastline = outlines[-1]
                # if the lastline ends in a letter (i.e. not a punctuation point, but maybe with spaces)
                # and the first letter of this line is lower case.
                # and the last line is long (> 120 chars)
                if re.search(ur'[^\W_\d]\s*$', lastline.strip(), flags=re.UNICODE) and \
                        re.match(ur'[^\W_\d]', line, flags=re.UNICODE).group().islower()\
                        and len(lastline) > 120:

                    # work out if we should add a space: (note regex includes _
                    # todo here we check if a word has been cut or not:
                    '''
                    endword = re.search(ur'(?:[^\W_\d]|\-|\')+$', lastline.strip(), flags=re.UNICODE)
                    beginword = re.match(ur'^(?:[^\W_\d]|\-|\')+', line, flags=re.UNICODE)
                    print len(lastline)
                    if endword and beginword:
                        print "end and begin"
                        print endword.group()
                        print beginword.group()
                        # need to check if together or separately they make words, maybe with sxpipe or lefff?
                    '''
                    # we don't add a space if the length of the last line = 990
                    #  (looks like some sort of email cutoff?)
                    if len(lastline) != 990:
                        # add a space
                        line = u" " + line

                    if debug: print "combining lines:"
                    if debug: print outlines[-1].strip()
                    if debug: print line
                    outlines[-1] = outlines[-1].strip() + line
                    if debug: print outlines[-1]

                else:
                    outlines.append(line)
            else:
                outlines.append(line)

            #outlines.append(line)
            lineNumber += 1

    #for i in range(len(outlines)):
    #    print "line,", str(i), outlines[i]
    # create an outfile in utf8 and open the infile with the encoding
    with codecs.open(outbasedir + "/" + filename, mode="w", encoding="utf-8") as outfile:
        for line in outlines:
            #print line
            outfile.write(line)



def analyseDirectory( inbasepath, outbasepath, relativepath ):
    outdir = outbasepath + "/" + relativepath
    # it's a directory:
    # make an output dir if necessary
    try:
        os.stat(outdir)
    except:
        os.mkdir(outdir)

    for element in os.listdir(inbasepath + "/" + relativepath):
        in_full_element = inbasepath + "/" + relativepath + "/" + element
        #out_full_element = outbasepath + "/" + relativepath + "/" + element
        if os.path.isfile(in_full_element):
            # only convert text files:
            if os.path.splitext(element)[1] == ".txt":
                #analyseFile(inbasepath + "/" + relativepath, outbasepath + "/" + relativepath, element )
                encoding = 'windows-1252'
                removeActivity = False
                removeHeaderETC = True
                #if element.startswith('hellasFLE'): encoding = 'MacRoman'
                if element.startswith('hellasFLE'): encoding = 'latin-1'
                if element.startswith('centreFLE'): removeActivity = True
                #if element.startswith('chyFLE') or element.startswith('centreFLE'): removeHeaderETC = True

                # exceptions:
                '''
                # known to be latin-1:
                # hellasFLE_2010_TL_KPG_B2_Activite1_candidat10.txt
                # hellasFLE_2010_TL_KPG_B2_Activite1_candidat13.txt
                # hellasFLE_2010_TL_KPG_B2_Activite1_candidat14.txt
                # hellasFLE_2010_TL_KPG_B2_Activite1_candidat15.txt
                # hellasFLE_2010_TL_KPG_B2_Activite1_candidat2.txt
                # hellasFLE_2010_TL_KPG_B2_Activite1_candidat3.txt
                # hellasFLE_2010_TL_KPG_B2_Activite1_candidat5.txt
                # hellasFLE_2010_TL_KPG_B2_Activite1_candidat6.txt
                # hellasFLE_2010_TL_KPG_B2_Activite1_candidat7.txt
                # hellasFLE_2010_TL_KPG_B2_Activite1_candidat9.txt
                # hellasFLE_2010_TL_KPG_B2_Activite2_candidat9.txt
                #'hellasFLE_2010_TL_KPG_B2_Activite1_candidat1.txt',
                #'hellasFLE_2010_TL_KPG_B2_Activite1_candidat11.txt',
                #'hellasFLE_2010_TL_KPG_B2_Activite2_candidat4.txt',
                #'hellasFLE_2010_TL_KPG_B2_Activite2_candidat6.txt',
                #'hellasFLE_2010_TL_KPG_B2_Activite2_candidat8.txt',
                #'hellasFLE_2010_TL_KPG_B2_Activite2_candidat13.txt',
                #'hellasFLE_2010_TL_KPG_B2_Activite2_candidat15.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite1_candidat9.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite1_candidat11.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite1_candidat13.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite1_candidat14.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite1_candidat16.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite1_candidat19.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite1_candidat22.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite1_candidat23.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite1_candidat29.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite1_candidat3.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite1_candidat6.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite1_candidat7.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite2_candidat1.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite2_candidat6.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite2_candidat9.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite2_candidat12.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite2_candidat14.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite2_candidat17.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite2_candidat21.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite2_candidat23.txt',
                #'hellasFLE_2010_TL_KPG_C1_Activite2_candidat29.txt',
                '''

                # macRoman:
                if element in [
                    'hellasFLE_2010_TL_KPG_C1_Activite2_candidat15.txt',
                    'hellasFLE_2010_TL_KPG_C1_Activite1_candidat15.txt',
                    ]:
                    encoding = 'macRoman'
                # utf-8:
                elif element in [
                    'hellasFLE_2010_TL_KPG_B2_Activite1_candidat16.txt',
                    'hellasFLE_2010_TL_KPG_B2_Activite1_candidat18.txt',
                    'hellasFLE_2010_TL_KPG_B2_Activite2_candidat12.txt',
                    'hellasFLE_2010_TL_KPG_B2_Activite2_candidat17.txt',
                    'hellasFLE_2010_TL_KPG_B2_Activite2_candidat16.txt',
                    'hellasFLE_2010_TL_KPG_C1_Activite1_candidat20.txt',
                    'hellasFLE_2010_TL_KPG_C1_Activite2_candidat20.txt',
                    ]:
                    encoding = 'utf-8'
                # utf-16le:
                elif element in [
                    'hellasFLE_2010_TL_KPG_C1_Activite1_candidat26.txt',
                    'hellasFLE_2010_TL_KPG_B2_Activite1_candidat19.txt',
                    'hellasFLE_2010_TL_KPG_C1_Activite1_candidat27.txt',
                    ]:
                    encoding = 'utf-16le'
                # unknown, treat as utf-8:
                elif element in [
                    'hellasFLE_2010_TL_KPG_B2_Activite1_candidat17.txt',
                    'hellasFLE_2010_TL_KPG_B2_Activite1_candidat12.txt',
                    ]:
                    encoding = 'utf-8'
                # unknown, treat as latin-1 (as latin-1 is correct for all but 2 chars)
                elif element in [
                    'hellasFLE_2010_TL_KPG_C1_Activite2_candidat16.txt',
                    ]:
                    encoding = 'latin-1'

                reEncodeFile( inbasepath + "/" + relativepath, outbasepath + "/" + relativepath, element,
                              encoding,
                              removeActivityNumber=removeActivity,
                              removeHeadTailSectionInfo=removeHeaderETC,
                              debug=True)
            else:
                # if it's not a .txt file just copy it:
                shutil.copyfile(inbasepath + "/" + relativepath + "/" + element,
                                outbasepath + "/" + relativepath + "/" + element)
        else:
            # it's not a file, so it's a directory, recurse into it:
            print "analysing directory: ", relativepath + "/" + element
            analyseDirectory(inbasepath, outbasepath, relativepath + "/" + element )


#basedir = "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_ECRIT_VALETOPOULOS/CORPUS_CHY-FLE/"
#outbasedir = "/home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS/CORPUS_CHY-FLE/"
basedir = "/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS_ECRIT_VALETOPOULOS/"
outbasedir = "/home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS/"

analyseDirectory(basedir, outbasedir, ".")

print "all chars found:"
print allChars # unicode so it doesn't work this way
for char in sorted(allChars):
    print char


