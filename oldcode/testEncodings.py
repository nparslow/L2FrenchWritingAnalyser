# coding=utf-8
import re

__author__ = 'nparslow'

import codecs
import io
import charade

#dir = '/home/nparslow/Documents/AutoCorrige/Corpora/CORPUS ECRIT VALETOPOULOS/CORPUS HELLAS-FLE/'
#dir = '/home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS/CORPUS_CENTRE-FLE/'
dir = '/home/nparslow/Documents/AutoCorrige/Corpora/converted/CORPUS_ECRIT_VALETOPOULOS/CORPUS_CHY-FLE/'
'''
file = u'hellasFLE_2010_TL_KPG_B2_Activité1_candidat12.txt'

file = u'hellasFLE_2010_TL_KPG_B2_Activité2_candidat6.txt' # needs latin-1
file = u'hellasFLE_2010_TL_KPG_C1_Activité1_candidat29.txt' # needs latin-1
file = u'hellasFLE_2010_TL_KPG_C1_Activité2_candidat17.txt' # needs latin-1
file = u'hellasFLE_2010_TL_KPG_B2_Activité2_candidat6.txt' # needs latin-1
file = u'hellasFLE_2010_TL_KPG_C1_Activité1_candidat11.txt' # needs latin-1

# utf-8 ?
file = u"hellasFLE_2010_TL_KPG_B2_Activité2_candidat17.txt"
file = u"hellasFLE_2010_TL_KPG_C1_Activité2_candidat20.txt"
file = u"hellasFLE_2010_TL_KPG_B2_Activité1_candidat16.txt"
file = u"hellasFLE_2010_TL_KPG_B2_Activité1_candidat12.txt"
file = u"hellasFLE_2010_TL_KPG_B2_Activité2_candidat16.txt"
file = u"hellasFLE_2010_TL_KPG_C1_Activité1_candidat20.txt"

# unknown:
file = u"hellasFLE_2010_TL_KPG_C1_Activité2_candidat26.txt"
file = u'hellasFLE_2010_TL_KPG_B2_Activité1_candidat12.txt'
file = u'hellasFLE_2010_TL_KPG_C1_Activité1_candidat26.txt'

file = u"hellasFLE_2010_TL_KPG_C1_Activité2_candidat16.txt" # latin1 and latin3 work for all but "matire" (è)
                                                            # windows-1253 etc. also, same problem
'''

'''
file = u"centreFLE_2006_TL_CFLETP_6_Activite1_ZABALA_Leonardo.txt"
file = u"chyFLE_2010_TL_UCY_1A_Autoobservation_Rafaella_Sofroniou.txt"
file = u'chyFLE_2011_TI_UCY_4_Autoobservation_Aphrodite_Papaioannou.txt'
file = u"chyFLE_2010_TL_UCY_1A_Strategies_Rafaella_Georgiou.txt"
'''

# looking for strange phonetic symbols:
file = u"chyFLE_2010_TL_UCY_1A_Autoobservation_Agathe_Chrysse.txt" # ''???''
file = u"chyFLE_2010_TL_UCY_1A_Autoobservation_Andria_Zavrou.txt" # ok
file = u"chyFLE_2010_TL_UCY_1A_Autoobservation_Anna_Sakka.txt" # line broken in middle of 'des' i.e. 'd \n es'
'''
file = u"chyFLE_2010_TL_UCY_1A_Autoobservation_Maria_Hadjigeorgiou.txt"
file = u"chyFLE_2010_TL_UCY_1A_Autoobservation_Michalis_Christodoulou.txt"
file = u"chyFLE_2010_TL_UCY_1A_Autoobservation_Panagiotou_Efi.txt"
file = u"chyFLE_2010_TL_UCY_1A_Autoobservation_Rafaella_Georgiou.txt"si tu
file = u"chyFLE_2010_TL_UCY_1A_Autoobservation_Rafaella_Sofroniou.txt"
file = u"chyFLE_2010_TL_UCY_1A_Strategies_Agathe_Chrysse.txt"
file = u"chyFLE_2010_TL_UCY_1A_Strategies_Agathi_Hadjicosti.txt"
file = u"chyFLE_2010_TL_UCY_1A_Strategies_Andria_Zavrou.txt"
file = u"chyFLE_2010_TL_UCY_1A_Strategies_Anna_Sakka.txt"
file = u"chyFLE_2010_TL_UCY_1A_Strategies_Michalis_Christodoulou.txt"
file = u"chyFLE_2010_TL_UCY_1A_Strategies_Rafaella_Georgiou.txt"
file = u"chyFLE_2010_TL_UCY_1A_Strategies_Yiannis_Panayides.txt"
file = u"chyFLE_2011_TI_UCY_4_Autoobservation_Andria_PANTELI.txt"
file = u"chyFLE_2011_TI_UCY_4_Autoobservation_Aphrodite_Papaioannou.txt"
file = u"chyFLE_2011_TI_UCY_4_Autoobservation_Elia_Aza.txt"
file = u"chyFLE_2011_TI_UCY_4_Autoobservation_Evdokia_Sofokleous.txt"
file = u"chyFLE_2011_TI_UCY_4_Autoobservation_Helene_Christoforou.txt"
file = u"chyFLE_2011_TI_UCY_4_Autoobservation_Margarita_Epiphaniou.txt"
file = u"chyFLE_2011_TI_UCY_4_Autoobservation_Maria_Eleftheriou.txt"
file = u"chyFLE_2011_TI_UCY_4_Autoobservation_Maria_Odysseos.txt"
file = u"chyFLE_2011_TI_UCY_4_Autoobservation_Neofytos_Antoniou.txt"
file = u"chyFLE_2011_TI_UCY_4_Autoobservation_Panagiota_Ioannou.txt"
file = u"chyFLE_2011_TI_UCY_4_Autoobservation_Savvia_Leonidou.txt"
file = u"chyFLE_2011_TI_UCY_4_Autoobservation_Susanna_Georgiou.txt"
'''

# re https://docs.python.org/2/library/codecs.html
# tested utf-8 utf-7 utf_8_sig
# tested windows-1250 to windows-1258 (1259 doesn't exist)
# utf-16 gives error: UnicodeError: UTF-16 stream does not start with BOM
# macRoman macGreek macturkish maclatin2
# latin-1 latin2 - latin10   nb  iso-8859-1 == latin-1  iso-8859-5 to 8
# UTF-16LE UTF-16BE utf_32_le utf_32_be
# ISO-8859-7
# cp500 cp737 cp850 cp852 cp855 cp857 cp858 cp869 cp875 cp1026 cp1140
# greek == iso-8859-7
# ascii (lol)
#

import ftfy


rawdata = open(dir + file, 'rb').read()
result = charade.detect(rawdata)
print ftfy.guess_bytes(rawdata)[0]
print rawdata
print result
'''


with codecs.open(dir + file, mode='r', encoding='utf-8') as infile:
#with io.open(dir + file, mode='rb') as infile:
#    data = infile.read().encode('windows-1250')
        #.decode('latin1')

    #print data
    for line in infile:

        #line = line.replace(u'ˆ', u'à')
        #line = line.replace(u'Õ', u"'")
        #line = line.replace(u'Ž', u'é')
        print line
        print ftfy.fix_encoding(line)



blah = ftfy.fix_file(dir + file)

'''
import ftfy.bad_codecs


import repairFunction

with codecs.open(dir + file, mode='r', encoding='utf8') as infile:
    for line in infile:
        print "newline:", line.strip()
        print line.strip().split(' ')
        print

        #print line.replace(u"matiڈre", u"matière")

        '''
        #print line.encode('utf-8')
        #print '\x00' in line
        #print re.sub(ur'\x00', 'è', line)
        line.encode('utf-8')
        line = line.replace(u'\x00', u"è")
        line = line.replace(u'Õ', u"'")
        line = line.replace(u'ˆ', u"à")
        line = line.replace(u'Ž', u"é")
        print line.rstrip()
        #print line.encode('utf-8').decode('latin-1')
        #print line.encode('macgreek')
        #print repairFunction.fix_bad_unicode(line)
        '''
    #text = infile.read()
    #print text
    ##text = u"Je tÕecris pour rŽpondre ˆ son faux decision de quitter le lycŽe. Tu es dans une difficulte situation."
    #print ftfy.fix_encoding(text)
    ##print ftfy.explain_unicode(text)


#for line in ftfy.fix_file(dir + file):
#    print line

