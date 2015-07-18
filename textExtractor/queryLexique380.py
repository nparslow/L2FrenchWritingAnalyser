__author__ = 'nparslow'

import codecs
import json

def loadLexiqueToDict( lexiquefilename, lexdict ):
    #lexdict = {}
    with codecs.open(lexiquefilename, mode="rb", encoding='latin1') as lexfile: #
        firstLine = True
        strangelinecount = 0

        for line in lexfile:
            if not firstLine:
                # 33 lines seem to behave strangely so:
                try:
                    #print len(line.strip('\r\n').split('\t'))
                    ortho, phon, lemme, cgram, genre, nombre, freqlemfilms, freqlemlivres, freqfilms2, \
                    freqlivres, infover, nbhomogr, nbhomoph, islem, nblettres, nbphons, cvcv, p_cvcv, \
                    voisorth, voisphon, puorth, puphon, syll, nbsyll, cv_cv, orthrenv, phonrenv, \
                    orthosyll, cgramortho, deflem, defobs, old20, pld20, morphoder, nbmorph = \
                    line.strip('\r\n').split('\t')

                    if ortho in lexdict:
                        lexdict[ortho].append([(lemme, int(nbsyll))])
                    else:
                        lexdict[ortho] = [(lemme, int(nbsyll))]
                except:
                    #print "strange line:", line
                    strangelinecount += 1
                    #break
            else:
                firstLine = False

    print "loaded Lexique:", len(lexdict), strangelinecount, sum([len(x) for x in lexdict.values()])

#lex = {}
#loadLexiqueToDict(u"/home/nparslow/Documents/AutoCorrige/tools/Lexique380/Bases+Scripts/Lexique380.txt", lex)

#with codecs.open('blah.txt', 'w', encoding='utf8') as fp:
#    json.dump(lex, fp)