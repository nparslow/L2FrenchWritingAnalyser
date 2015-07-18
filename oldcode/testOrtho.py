# coding=utf-8
__author__ = 'nparslow'


from bs4 import BeautifulSoup
import codecs

corpushtmlfile = "/home/nparslow/Documents/AutoCorrige/SpellChecker/errorsCorpusCorrected.html"

'''
with codecs.open(corpushtmlfile, mode='r', encoding='latin1') as htmlcorpus:
    htmlcorpusAsUnicode = htmlcorpus.read().encode('latin1').decode('latin-1').encode('utf8')
    #soup = BeautifulSoup(htmlcorpus)
    soup = BeautifulSoup(htmlcorpusAsUnicode)

    table = soup.find('table')

    rowcount = 0
    for row in table.findAll('tr'):
        print "analysing", row
        cols = row.findAll('td')
        if len(cols) > 0:
            entryNumber = int(cols[0].text.strip())  # note some entry numbers do not exist
            #if entryNumber in  [48,106, 155, 270, 274, 334]: continue
            # the view corpus all together option has some only partial original texts so we don't use those
            # and sometimes the corrected sentence includes
            #  both the original words and their replacements (e.g. no. 225)

            # if cols[1].findAll('td'):
            print type(cols[1].text)
            #print (cols[1].text).encode('utf8')
            #print (cols[1].text).encode('utf8').decode('utf8').strip()
            origtextmainpage = cols[1].text.strip() + u"bléh"
            #correctedtextmainpage = cols[3].text.encode('utf8').decode('utf8').strip()
            correctedtextmainpage = cols[3].text.strip()
            corr2 = correctedtextmainpage.encode('utf8').decode('utf8')

            print type((cols[1].text).encode('utf8').decode('utf8').strip())
            altcorr = correctedtextmainpage + u""

            blah = u"blah"
            blah2 = blah + u""
            print altcorr == correctedtextmainpage
            print corr2 == correctedtextmainpage
            print blah2 == blah
            print origtextmainpage

            break

'''
origout = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellChecker/entry"
corrout = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellCheckerCorrected/entrycorrected"
entrynumber = 337
outtextfilename = origout + "_" + str(entrynumber) + ".txt"
correctedouttextfilename = corrout + "_" + str(entrynumber) + ".txt"
with codecs.open(outtextfilename, mode='r', encoding='utf8') as outtextfile:
    with codecs.open(correctedouttextfilename, mode='r', encoding='utf8') as correctedouttextfile:
        for line1, line2 in zip(outtextfile, correctedouttextfile):
            print line1
            print line2
            for c1, c2 in zip(line1, line2):
                print c1==c2