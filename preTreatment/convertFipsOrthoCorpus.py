# -*- coding=utf-8 -*-

import codecs
import sys
#import locale
__author__ = 'nparslow'
#sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
# to avoid screwed up ascii in the terminal/console (doesn't seem to work here)
#UTF8Writer = codecs.getwriter('utf8')
#sys.stdout = UTF8Writer(sys.stdout)
#sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) # no luck
#sys.setdefaultencoding("utf-8")
# export PYTHONIOENCODING=utf-8 doesn't work
from bs4 import BeautifulSoup
import re


import json

#import locale

class Entry:
    def __init__(self, entrynumber, origtext, correctedtext, worderrorlist):
        self.entrynumber = entrynumber
        self.origtext = origtext
        self.correctedtext = correctedtext
        self.worderrorlist = worderrorlist


def readCorpus(corpushtmlfile):
    corpus = []
    with codecs.open(corpushtmlfile, mode='r', encoding='latin1') as htmlcorpus:
        htmlcorpusAsUnicode = htmlcorpus.read().encode('latin1')
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
                #if entryNumber != 337: continue
                # the view corpus all together option has some only partial original texts so we don't use those
                # and sometimes the corrected sentence includes
                #  both the original words and their replacements (e.g. no. 225)

                # if cols[1].findAll('td'):
                origtextmainpage = cols[1].text.strip() #.encode('utf8').decode('utf8')
                correctedtextmainpage = cols[3].text.strip() #.encode('utf8').decode('utf8')
                #print type(origtextmainpage)
                #print type(correctedtextmainpage)

                # normalisations to make life easier:
                origtextmainpage = re.sub(ur'\s+', u' ', origtextmainpage, flags=re.UNICODE)
                origtextmainpage = re.sub(ur' !', u'!', origtextmainpage, flags=re.UNICODE)
                origtextmainpage = re.sub(ur' \?', u'?', origtextmainpage, flags=re.UNICODE)
                origtextmainpage = re.sub(ur' ,', u',', origtextmainpage, flags=re.UNICODE)
                origtextmainpage = re.sub(ur' ;', u';', origtextmainpage, flags=re.UNICODE)

                if entryNumber == 15:
                    correctedtextmainpage = re.sub(ur' en ', u' de la ', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'le Terre-Neuve', u'Terre-Neuve', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 29:
                    correctedtextmainpage = re.sub(ur'des problèmes', u'de problèmes', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 31:
                    # origtextmainpage = re.sub(ur' France', u'France', origtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'la France', u'France', correctedtextmainpage, flags=re.UNICODE)
                # elif entryNumber == 38:
                #    origtextmainpage = re.sub(ur'\s+La curé', u' La curé', origtextmainpage, flags=re.UNICODE)
                # elif entryNumber == 40:
                #    origtextmainpage = re.sub(ur'\s+par', u' par', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 43:
                    correctedtextmainpage = re.sub(ur'content,', u'content;', correctedtextmainpage,
                                                   flags=re.UNICODE)  # I could be wrong here
                elif entryNumber == 48:
                    correctedtextmainpage = re.sub(ur'là', u'-là', correctedtextmainpage, flags=re.UNICODE)
                    # origtextmainpage = re.sub(ur'\)\?', u') ?', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 49:
                    correctedtextmainpage = re.sub(ur'faim', u'faim,', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 53:
                    origtextmainpage = re.sub(ur'peintures,', u'peintures', origtextmainpage,
                                              flags=re.UNICODE)  # an error was highlighted, so I assume it was there
                elif entryNumber == 61:
                    origtextmainpage = re.sub(ur':«', u':« ', origtextmainpage, flags=re.UNICODE)
                    origtextmainpage = re.sub(ur'\.\.\. »', u'...»', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 65:
                    correctedtextmainpage = re.sub(ur'rois inca', u'rois incas', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 69:
                    origtextmainpage = re.sub(ur'...Une', u'... Une', origtextmainpage, flags=re.UNICODE)
                    origtextmainpage = re.sub(ur'» \(', u'»(', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 70 or entryNumber == 84:
                    origtextmainpage = re.sub(ur'\? »', u'?»', origtextmainpage, flags=re.UNICODE)
                    pass
                elif entryNumber == 71:
                    origtextmainpage = re.sub(ur'...alors', u'... alors', origtextmainpage, flags=re.UNICODE)
                    origtextmainpage = re.sub(ur'»Prépondérant', u'» Prépondérant', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 74 or entryNumber == 75:
                    origtextmainpage = re.sub(ur' , ', u', ', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 81:
                    correctedtextmainpage = re.sub(ur'épisode\(«Les', u'épisode ( « Les', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    origtextmainpage = re.sub(ur'» \)', u'»)', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 82:
                    origtextmainpage = re.sub(ur'président...', u'président ...', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 92:
                    origtextmainpage = re.sub(ur'autre "\.', u'autre ».', origtextmainpage, flags=re.UNICODE) # standardise punct, benefit of the doubt to student
                    correctedtextmainpage = re.sub(ur'autre "\.', u'autre ».', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 93:
                    origtextmainpage = re.sub(ur':«Un', u':« Un', origtextmainpage, flags=re.UNICODE)
                    origtextmainpage = re.sub(ur'\.\.\. »', u'...»', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 94:
                    origtextmainpage = re.sub(ur'» :', u'»:', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 96:
                    origtextmainpage = re.sub(ur'\. \( = C', u'.( = C', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 107 or entryNumber == 119:
                    origtextmainpage = re.sub(ur' \!', u'!', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 109:
                    correctedtextmainpage = re.sub(ur'père', u'Père', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 110:
                    correctedtextmainpage = re.sub(ur'dans ce temps-ci', u'à cette époque', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'pleuvait', u'pleut', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'faisait vent', u'fait du vent', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'il est en général', u'il fait en général', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 113:
                    origtextmainpage = re.sub(ur'\' ', u'\'', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 114:
                    correctedtextmainpage = re.sub(ur' ne ', u' ', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 116:
                    origtextmainpage = re.sub(ur',Comment', u', Comment', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 122:
                    correctedtextmainpage = re.sub(ur' est ', u' ', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 124:
                    correctedtextmainpage = re.sub(ur'cours du surf', u'cours de surf', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 126:
                    correctedtextmainpage = re.sub(ur'Australiens', u'Australiens. Je plaisante', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 131:
                    correctedtextmainpage = re.sub(ur'l\'aimeras', u'aimeras', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 139:
                    origtextmainpage = re.sub(ur'\.\.\.A', u'... A', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 140:
                    correctedtextmainpage = re.sub(ur'va\-tu', u'vas-tu', correctedtextmainpage, flags=re.UNICODE)
                    origtextmainpage = re.sub(ur' \?', u'?', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 155:
                    correctedtextmainpage = re.sub(ur'de', u'', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 160:
                    correctedtextmainpage = re.sub(ur'en la ville', u'en ville', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 164:
                    correctedtextmainpage = re.sub(ur'grosse que', u'grosse que quand', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 162:
                    correctedtextmainpage = re.sub(ur'à tous', u'dans tous', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'\-\s', u'', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 173:
                    correctedtextmainpage = re.sub(ur'\.,', u'.', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 177:
                    origtextmainpage = re.sub(ur'e\.\.\.', u'e ...', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 179:
                    correctedtextmainpage = re.sub(ur'Mountain', u'Mountains', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 184:
                    correctedtextmainpage = re.sub(ur'es arrives', u'arrives', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 185:
                    correctedtextmainpage = re.sub(ur'\?,', u'?', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 186:
                    correctedtextmainpage = re.sub(ur' ais ', u' aies ', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 187:
                    correctedtextmainpage = re.sub(ur'excitée', u'enthousiaste', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 189:
                    correctedtextmainpage = re.sub(ur'mois prochains', u'prochains mois', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 195:
                    origtextmainpage = re.sub(ur'Donc,', u'Donc', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 200:
                    origtextmainpage = re.sub(ur'»,', u'» ,', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 202:
                    correctedtextmainpage = re.sub(ur'modestes', u'modeste', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 203 or entryNumber == 204:
                    origtextmainpage = re.sub(ur'\. »', u'.»', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 210:
                    correctedtextmainpage = re.sub(ur'goût', u'ton', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 214:
                    correctedtextmainpage = re.sub(ur'\- meilleurs', u'meilleurs', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'Absolument à voir', u'À voir absolument', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 215:
                    # print "yo", correctedtextmainpage
                    correctedtextmainpage = re.sub(ur'global réchauffement', u'réchauffement global',
                                                   correctedtextmainpage,
                                                   flags=re.UNICODE)  # missing word in corrected text
                elif entryNumber == 218:
                    correctedtextmainpage = re.sub(ur'baisse', u'une baisse', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'grand simutanés ouragans', u'grands ouragans simultanés',
                                                   correctedtextmainpage, flags=re.UNICODE) # note the spelling correction!
                elif entryNumber == 223:
                    correctedtextmainpage = re.sub(ur'baisse', u'une baisse', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 225:
                    correctedtextmainpage = re.sub(ur'hier', u'', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'Le cadre a', u'Le cadre', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'J\'ai j\'y suis', u'J\'y suis',
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 226:
                    correctedtextmainpage = re.sub(ur'au une au miel sauce', u'au miel', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'poulet en', u'poulet à la', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 227:
                    correctedtextmainpage = re.sub(ur'mourir pour', u'mourir', correctedtextmainpage, flags=re.UNICODE)
                    origtextmainpage = re.sub(ur'»,', u' »,', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 233:
                    correctedtextmainpage = re.sub(ur'avec une saveur', u'en ajoutant une touche',
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 240:
                    origtextmainpage = re.sub(ur'fruits,pain', u'fruits, pain', origtextmainpage, flags=re.UNICODE)
                elif entryNumber == 241:
                    correctedtextmainpage = re.sub(ur'favorite plats', u'plats favoris', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'les salsa', u'le salsa', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur' pain ', u' le pain ', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 242:
                    correctedtextmainpage = re.sub(ur'yaatties', u'yatties', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 243:
                    correctedtextmainpage = re.sub(ur'La Bamba restaurant', u'Le restaurant La Bamba',
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 245:
                    correctedtextmainpage = re.sub(ur'bar petit', u'petit bar', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'assiette est', u'plat', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 251:
                    correctedtextmainpage = re.sub(ur'complètent\s+l\'une\s+l\'autre', u'complète celui des autres',
                                                                        correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 255:
                    correctedtextmainpage = re.sub(ur'intime ambiance', u'ambiance intime', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 257:
                    correctedtextmainpage = re.sub(ur'génial', u'géniaux', correctedtextmainpage,
                                                   flags = re.UNICODE)
                elif entryNumber == 261:
                    correctedtextmainpage = re.sub(ur'Soverign', u'Sovereign', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 268:
                    correctedtextmainpage = re.sub(ur"L'' ambiance", u"L'ambiance",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 272:
                    correctedtextmainpage = re.sub(ur",\s+par\s+contre\s+", u", par contre, ",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 274:
                    correctedtextmainpage = re.sub(ur"principal", u"principal,",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 275:
                    correctedtextmainpage = re.sub(ur"commencé je", u"commencé, je",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 277:
                    correctedtextmainpage = re.sub(ur"révélé", u"révélée",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 278:
                    correctedtextmainpage = re.sub(ur"[Ll]a cours", u"le cours",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"[Ll]a cours", u"le cours",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"offrent", u"s'accompagnent",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 281:
                    correctedtextmainpage = re.sub(ur"quel sorte", u"quelle sorte",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 287:
                    correctedtextmainpage = re.sub(ur'porteur', u'porteurs', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 293:
                    correctedtextmainpage = re.sub(ur'leur chansons', u'leurs chansons', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 296:
                    correctedtextmainpage = re.sub(ur'le koulak', u'les koulaks', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 332:
                    correctedtextmainpage = re.sub(ur'aimais beaucoup aimé', u'aimais beaucoup', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'ai mange la', u'ai mangé une', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'petite j\'ai', u'petite, j\'ai', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 334:
                    correctedtextmainpage = re.sub(ur'petite j\'\s*aimais', u'petite, j\'aimais', correctedtextmainpage,
                                                   flags=re.UNICODE)

                # start of missing info:
                elif entryNumber == 335:
                    origtextmainpage += u"a trop grand!"
                    correctedtextmainpage = re.sub(ur'petite j\'ai', u'petite, j\'ai', correctedtextmainpage,
                                                   flags = re.UNICODE)

                elif entryNumber == 336:
                    origtextmainpage += u" hommes. C'est une petite guerre civile entre le Gouvernement et" \
                                        u" la\" Guerilla\"." \
                                        u" Une Guerilla qui est née come conséquence des mouvements socialistes" \
                                        u" en Amérique" \
                                        u" du Sud au même temp que la Révolution Cubaine, mais qu'aujourd'hui n'a pas" \
                                        u" des ideales ( Elle se finance avec le trafic de drogue)" \
                                        u" . Un Gouvernement\" " \
                                        u"démocratique\" qui change chaque quatre ans de mains, sans avoir une vrais" \
                                        u" volonté pour arriver a vivre en paix. Et comme le Gouvernement( les" \
                                        u" militaires) n est pas capable de garantir la sécurité des entrepreneurs" \
                                        u" et des grands producteurs agricole, ceux-ci ont formé sa propre armée" \
                                        u" pour se défandre de la Guerilla, les\" Para Militaires\"." \
                                        u" Entre les combats" \
                                        u" de la Guerilla, des Militaires et des Para Militaires, c'est la population" \
                                        u" qui souffre les conséquence de la guerre. C'est normale de lire tous" \
                                        u" les jours dans les journaux colombien des articles sur la dernière masacre" \
                                        u" dans une zone rurale. Ce sont des paysan qui ils n'ont rien avoir avec" \
                                        u" le conflit qui sont torture et tue, parce que selon le groupe qui" \
                                        u" masacre, ils aidaient l'autre groupe armé. Alors ils perdent leur vie" \
                                        u" simplement pour être entre le conflit armé. J'espère que le jour arrivera," \
                                        u" où qu'en Colombie on pourras vivre en paix."
                    correctedtextmainpage = re.sub(ur'Guerilla', u"Guérilla", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'se finance avec', u"est financée par", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'défendre de la Guérilla', u"défendre contre la Guérilla",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'qui ils n\'ont', u"qui n'ont", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'entre le conflit', u"au milieu du conflit", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'arrivera, où', u"arrivera où", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'qu\'en Colombie', u"en Colombie", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"on pourras", u"on pourra", correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 337:
                    #print origtextmainpage
                    #print origtextmainpage + u"" == origtextmainpage
                    #origtextmainpage = re.sub(ur"é", u"é", origtextmainpage, flags=re.UNICODE)
                    #origtextmainpage  = unicode(origtextmainpage)

                    origtextmainpage += u" grandes conséquences pour les entreprises belges. Si elles veulent occuper" \
                                        u" leur position sur le marché intérieure, elles doivent faire face à la" \
                                        u" concurrence élargissante de l'étranger. Mais réaliser cet objectif est" \
                                        u" impossible de notre entreprise parce que notre entreprise est une PME" \
                                        u" et elle ne peut pas concurrencez les grandes entreprises de l'étranger." \
                                        u" Notre entreprise a donc dû partir à la recherche de nouveaux marchés par" \
                                        u" exemple le marché de l'Europe occidental où notre entreprise pourrait" \
                                        u" être rentable. A fin de lancer notre produit sur ce marché, nous devons " \
                                        u"promouvoir notre produit dans cette région."
                    # sxpipe will stop segmenting if it encounters a single ', so we have to manually cut the sentence:
                    origtextmainpage = re.sub(ur"des services et des capitaux\.", u"des services et des capitaux.\n",
                                              origtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"commençait", u"commençaient", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    #print type(origtextmainpage)
                    #print type(correctedtextmainpage)
                                                    # example of a new mistake inserted in the correct version!
                elif entryNumber == 338:
                    origtextmainpage += u"eau, pour que nous pouvons augmenter notre chiffre d'affaires. Notre" \
                                        u" entreprise a donc dû partir à la recherche de nouveau marchés. En faisant" \
                                        u" des innovations de l'un part investir dans les unité de production et" \
                                        u" de l'autre part dans la recherche et developpement. Pour atteindre ce but" \
                                        u" nous devons utiliser la publicité et élargir" \
                                        u" notre siseaux de point de vents."
                    correctedtextmainpage = re.sub(ur"ciblé", u"ciblé:", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"donc répond", u"donc il répond", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'conséquent est-il', u'conséquent, il est', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    #correctedtextmainpage = re.sub(ur'à des nouveaux cerveaux', u'a de nouveaux cerveaux',
                    #                               correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'd\'une l\'un', u'd\'une', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'd\' l\'autre part', u'd\'autre part', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'point de vente', u'points de vente', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'des nouveaux', u'de nouveaux', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 339:
                    origtextmainpage += u" dû partir à la recherche de nouveaux marchés. C'est pourquoi nous avons" \
                                        u" investit beaucoup dans la recherche et le développement de notre produit." \
                                        u" Afin d'améliorer la mise en disposition, nous avons multiplié les point" \
                                        u" de vente. Nous avons aussi contracté un agence publicitaire qui, grâce à" \
                                        u" une campagne publicitaire, a pû créer une image de marque pour notre" \
                                        u" produit. Diminuer le prix nous ne semble pas nécessaire, puisque notre" \
                                        u" produit est un produit de haute gamme."
                    correctedtextmainpage = re.sub(ur'contracté', u'engagé', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'nous ne semble', u'ne nous semble', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 340:
                    origtextmainpage += u"as en Belgique un créneaux. Mais les entreprises qu veulent rester ouvert," \
                                        u" doit être competitif. Les conditions pour être competitif sont la" \
                                        u" performance, la rentabilité, la productivité et l'innovation. Une" \
                                        u" entreprise est performante s'elle gagne des parts de marché Elle est" \
                                        u" rentabilité s'elle produit que le public demande. Elle est productive si" \
                                        u" les coûts relatif sont faibles et elle est innovatrice si elle investit" \
                                        u" dans le recherche et le developpement. Les entreprises n'ont pas de" \
                                        u" choix. Elles doivent chercher des nouveaux marchés pour rester vivant" \
                                        u" et d'entrer en concurrence avec d'autres entreprises."
                    correctedtextmainpage = re.sub(ur'exporzer', u'exporter', correctedtextmainpage,
                                                   flags=re.UNICODE)  # wtf lol
                    correctedtextmainpage = re.sub(ur'créneaux', u'créneau', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'rester\s+ouvert,\s+doit\s+être\s+compétitif',
                                                   u'rester ouvertes, doivent être compétitives', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur's\'elle', u'si elle', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'Elle est rentabilité', u'Elle est rentable',
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'produit que', u'produit ce que', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'coûts relatif', u'coûts relatifs', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'le recherche', u'la recherche', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'rester vivant', u'rester vivantes', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 341:
                    origtextmainpage += u" répondre à la demande d'un public déterminé. Ensuite pour le lancer sur le" \
                                        u" marché notre entreprise va faire en promotion. Elle donne des" \
                                        u" exemplaires gratuites et elle organise un tombola. Mais contrairement aux" \
                                        u" autres produits, le producteur veut opter" \
                                        u" pour un produit\" haut de gamme\"" \
                                        u" et puis le prix ne doit pas être bas. Enfin nous allons aussi multiplier" \
                                        u" les points de vente pour élargir le réseau de distribution."
                    correctedtextmainpage = re.sub(ur's\' il s\' agit', u's\' il s\' agit de', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'haut de gamme', u'haut-de-gamme', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 342:  # missing word line two after 'des' was indicated with ****
                    origtextmainpage += u"se, OCOB, avait trouvé de nouveaux débouchés, grâce à l'investissement et" \
                                        u" en faisant beaucoup d'études de marché par des sondages et des ." \
                                        u" Notre entreprise a donc dû partir à la recherche de nouveaux marchés," \
                                        u" parce que si on ne le faisait pas, ou resterait beaucoup derrière et la" \
                                        u" chance de faire faillite serait trop grand. En recherchant de nouveaux" \
                                        u" marchés, notre entreprise a vu ce qu'on devait faire. Nos yeux étaient" \
                                        u" ouverts et nous étions sur que dans quelque temps, nous nous trouverons" \
                                        u" de même sur le même niveau de OCOB."
                    correctedtextmainpage = re.sub(ur'desordinateurs', u'des ordinateurs', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'\* \* \* \*', u' enquêtes', correctedtextmainpage,
                                                   flags=re.UNICODE) # REPLACE **** by a substitute word!!!! todo (put in rapport)
                elif entryNumber == 343:
                    origtextmainpage += u" avait des autres firmes sur le marché et qui voulaient faire concurrence à" \
                                        u" DECA car leurs produits avaient comme cible" \
                                        u" le même public. Cettes firmes ont" \
                                        u" bien suivi les règles du marketing, c'est à dire\" les quatre p' s\"." \
                                        u" Le prix moins élevée car leurs production étaient plus élevée, leurs" \
                                        u" produits réspondaient plus à la demande du public car les produits de DECA" \
                                        u" avaient vieilli et elles faisaient beaucoup de promotion. A cause de tout" \
                                        u" cela DECA a perdu beaucoup de segments du marché et et maintenant elle a" \
                                        u" donc dû partir à la recherche de nouveaux marchés."
                    correctedtextmainpage = re.sub(ur'vingt ans', u'vingt ans,', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"c'est à dire", u"c'est-à-dire", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"tout cela", u"tout cela,", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur" et et ", u" et ", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"les quatre p' s", u"les quatre p", correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 344:
                    origtextmainpage += u"té pendant 5 ans. En dépit que les chiffres d'affaires baissaient, Belga" \
                                        u" restait le plus grand. VDB: \" Nous avions quelques problèmes avec la" \
                                        u" vente, mais ces problèmes sont passés maintenant\". La crise avait à voir" \
                                        u" avec la saturation du marché. \" Notre entreprise a donc dû partir à" \
                                        u" la recherche de nouveaux marchés\" il dit, et ils ont trouvé un: les" \
                                        u" jeunes. Eslabalement, leur clientèle existait des fumeurs agés. En" \
                                        u" developpant une nouvelle image de marque, les jeunes commençaient à" \
                                        u" fumer le Belga. Ainsi nous avons gagné une très grande part du" \
                                        u" marché. \" Maintenant je suis un homme heureux\" étaient ses mots finals."
                    correctedtextmainpage = re.sub(ur"président du Belga", u"président de Belga", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"ils ont trouvé", u"ils en ont trouvé", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Eslabalement", u"Auparavant", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"existait des", u"était constituée de", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"jeunes commençaient à", u"jeunes ont commencé à",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"le Belga", u"des Belga", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"il dit", u"dit-il", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"part du marché", u"part de marché",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"heureux\" étaient", u"heureux\", étaient",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 345:
                    origtextmainpage += u"on M. Declerck, on ne va plus pouvoir parler d'une peine sans coupable" \
                                        u" ou\" la négation de la presomption d'innocense. \" Au futur on aura" \
                                        u" besoin plus de preuves pour détenir quelqu'un. Certaines députés" \
                                        u" disent que ce projet de loi à comme seule but de résoudre le problème" \
                                        u" des prisons. En plus, disent-ils, seront les nouveaux organes des" \
                                        u" instruments du Ministère. Néanmoins, la Chambre a adopté le projet" \
                                        u" majorité contre minorité. Néanmoins quelques député de la majorité"
                    correctedtextmainpage = re.sub(ur"les idées des juristes éminents",
                                                   u"l'avis de juristes éminents", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"le Ministre de Justice", u"le Ministre de la Justice",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Ministère de Justice", u"Ministère de la Justice",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"a construit", u"a élaboré", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"va des", u"va créer des", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Au futur", u"Dans le futur", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"seule but", u"seul but", correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 346:
                    origtextmainpage += u"a donc les doses imortels vont réduire. Quelques députés de la majorité" \
                                        u" ont toutefois voté cotre ce projet de loi. Ce vote de méfiance"
                    correctedtextmainpage = re.sub(ur"état contrôle", u"État contrôle", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"d'opinion que", u"d'avis que", correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 347:
                    origtextmainpage += u"a majorité du chambre à voter pour le projet de loi mais quelques " \
                                        u"députés de la majorité ont voté contre ce projet de loi. La Chambre donne" \
                                        u" ce projet de loi à la sénat qui indiqué 15 sénateurs pour une recherche" \
                                        u" ou commission"
                    origtextmainpage = re.sub(ur"P\.H\.", u"", origtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"une recherche par", u"un examen par", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"La Chambre donne", u"La Chambre a transmis",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"au\s+la", u"au", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"indiqué", u"a désigné", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"une recherche ou", u"un examen en", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    #print "weird:", re.search(ur"examen",correctedtextmainpage, flags=re.UNICODE )

                elif entryNumber == 348:
                    origtextmainpage += u"nt d'accord, monsieur Maystadt sera très content. Le projet de loi du" \
                                        u" ministre de Finances s'exprime par une augmentation des impôts indirects," \
                                        u" c'est-à-dire une croissance de TVA. Ainsi, le ministre veut augmenter" \
                                        u" les recettes. Heureusement pour la population de la Belgique, quelques" \
                                        u" députés de la majorité ont voté contre ce projet de loi Et pas seulement" \
                                        u" des députés de la majorité, mais également ceux de la minorité. Alors le" \
                                        u" parlement a pu prevenir une nouvelle augmentation des impôts."

                    correctedtextmainpage = re.sub(ur"monsieur", u"Monsieur", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Pour ceci", u"Pour qu'il", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"deviendrait", u"devienne", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"se manifester", u"être présenté", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"s'exprime par", u"porte sur", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"croissance", u"augmentation", correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 349:
                    origtextmainpage += u"i La Haute Assemblée, à savoir le Sénat, a seulement une fonction de" \
                                        u" réffection. L'abolition de la peine de mort était un sujet d'un projet" \
                                        u" de loi, mais les partis politiques avaient des opinions différentes" \
                                        u" sur ce sujet. Quelques députés de la majorité ont toutefois vote" \
                                        u" contre ce projet de loi. Ces députés avaient l'opinion de garder" \
                                        u" la peine de mort pour des cas de guerre( par exemple: désertion) " \
                                        u"et des cas très sévères. Non seulement l'opposition voulait l'abolir" \
                                        u" parce que la peine de mort est trop cruelle et immense. Mais la peine" \
                                        u" de mort est probablement aussi un mort plus douce que le mort des victimes."
                    correctedtextmainpage = re.sub(ur"un sujet d'un", u"le sujet d'un", correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 350:
                    origtextmainpage += u"a soumis à la commission. Après le projet a fait plusieurs fois la navette" \
                                        u" entre la chambre des représentant et le sénat. Chaque chambre peut amender" \
                                        u" des partie du projet. Ainsi les partie amender sont corriger par" \
                                        u" l'autre chambre. La décision finale se trouve chez la chambre des" \
                                        u" représentant ( ceci depuis la dernière réforme) . Hier quelques députés" \
                                        u" de la majorité ont voté contre ce projet de loi, ce qui signifie que" \
                                        u" le projet ne continue pas son chemin, et ne sera donc jamais soumis" \
                                        u" à la sanction du Roi, et donc ni promulger ni publié dans le moniteur belge."
                    correctedtextmainpage = re.sub(ur"la chambre", u"la Chambre", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Chaque chambre", u"Chaque Chambre", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"autre chambre", u"autre Chambre", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"le sénat", u"le Sénat", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"la commission Après", u"la commission. Après",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"promulguer", u"promulgué",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Hier", u"Hier,",
                                                   correctedtextmainpage, flags=re.UNICODE)

                elif entryNumber == 351:
                    origtextmainpage += u"ouvernement a pris quelques messures c'est-à-dire, a la fin de l'année" \
                                        u" passée le gouvernement a proposé un nouveau loi: augmenter" \
                                        u" les impôts sur cigarettes, augmenter des coûts pour un " \
                                        u"rendez-vous au médecin. Mais cette proposition a connu des obstacles." \
                                        u" des plusieurs partis. Quelques députés de la majorité ont" \
                                        u" toutefois voté contre ce projet de loi C'est pourquoi cette proposition" \
                                        u" a été rejetée."
                    correctedtextmainpage = re.sub(ur"est crée par", u"est causé par",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"aux recettes", u"par rapport aux recettes",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"un nouveau loi", u"une nouvelle loi",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"au médecin", u"chez le médecin",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"de loi C'est", u"de loi. C'est",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"les coûts pour", u"le coût d'",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    origtextmainpage = re.sub(ur"de loi C'est", u"de loi. C'est",
                                                   origtextmainpage, flags=re.UNICODE) # benefit of doubt to student
                    correctedtextmainpage = re.sub(ur"c'est-à-dire,\s+à", u", en effet, à",
                                                   correctedtextmainpage, flags=re.UNICODE)

                elif entryNumber == 352:
                    origtextmainpage += u"onde politique a même peur pour une situation comme le projet de loi" \
                                        u" concernant l'avortement, c'est-à-dire que le Roi y est contre aussi." \
                                        u" Néanmoins, il y a aussi des Représentants et des sénateurs qui sont" \
                                        u" optimiste, mais ça ne veut pas dire que le projet de loi sera accepté," \
                                        u" évidemment. Si le Roi ne veut pas désigner, la Chambre des Représentants," \
                                        u" le Parlement et le Sénat avaient beaucoup de problèmes. Peut-être que la" \
                                        u" Cour d'Arbitrage doit s'y mêler. La seule chose qui manque encore pour" \
                                        u" que la situation serait typiquement belge, c'est une grande confrontation" \
                                        u" entre la Communauté française et la Communauté flamande."
                    correctedtextmainpage = re.sub(ur" trouvent pas à", u" trouve pas sur",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"pendant que", u"tandis que",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"ferme disant\" la", u"s'oppose \"en",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"avaient beaucoup", u"auront beaucoup",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"serait typiquement", u"soit typiquement",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 353:
                    origtextmainpage += u"t d'exclure les partis extrème-droite, les membres du Front National" \
                                        u" quittaient l'Assemblée fou de rage disantes qu'ils n'avaient rien à faire" \
                                        u" avec les incidents de la semaine passée. Enfin le scrutin pouvait avoir" \
                                        u" lieu après que la séance avait été interrompu de cette façon, pensantes" \
                                        u" à des situations japonaises. Le projet voté d'une manière renforcé" \
                                        u" et spéciale était accepté par la Chambre malgré que quelques députés" \
                                        u" de la majorité ont toutefois voté contre ce projet de loi. Ils disaient" \
                                        u" après dans leur explication du vote: \" qu'il faut tolléré la voix de" \
                                        u" chacun et chacune dans une démocratie moderne\". Probablement eux" \
                                        u" n'ont pas encore sentis la poignée."
                    correctedtextmainpage = re.sub(ur"La rue de la Loi succède l'", u"Le parcours de la Loi rencontre ",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    origtextmainpage = re.sub(ur"en otage", u"en hautage", origtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"uneambiance", u"une ambiance",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 354:
                    origtextmainpage += u"es de capital et attribuer par conséquence à la suppression de la dette" \
                                        u" publique. La Chambre a accepté mais ensuite après les députés ont" \
                                        u" voté, la Chambre a rejetté le projet de loi, parce que l'effet négative" \
                                        u" serez plus élevée que l'effet positive. Avec l'effet négative, elle" \
                                        u" veut dire par exemple une augmentation des accidents autoroutes." \
                                        u" Ensuite le ministre l'a changé en vue de l'acceptation de la Chambre" \
                                        u" mais malheureusement les députés de la majorité ont toutefois voté" \
                                        u" contre ce projet de loi."
                    correctedtextmainpage = re.sub(ur"la vie politique\.", u"la vie politique",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"\[ \? \]", u"",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"plus élevée", u"plus élevé",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"accidents sur l'autoroute", u"accidents sur les autoroutes",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 355:
                    origtextmainpage += u"oté contre. Ministre Peers était surpris car ceci est plusieurs" \
                                        u" exceptionnelle. En outre, le parlement a utilisé son pouvoir pour faire" \
                                        u" chuter le gouvernement Elle doit donc indiquer un nouveau Premier ministre" \
                                        u" et ceci pendant les trois jours. La décision a causé beaucoup de réactions" \
                                        u" mais le parlement a fait une choix qui le semble la meilleure."
                    correctedtextmainpage = re.sub(ur"chuter le gouvernement", u"chuter le gouvernement.",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Elle doit", u"Il doit",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"\.\s+le", u". Le",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 356:
                    origtextmainpage += u" transmis le texte au Sénat. Mais le sénat a amendé le texte de sorte" \
                                        u" qu'il soit revenu à la Chambre. La Chambre a la décision finale et" \
                                        u" il doit voter le texte. L'opinion publique supposait que ce projet" \
                                        u" soit accepté, quelque députés de la majorité ont toutefois voter" \
                                        u" contre ce projet de loi de sorte que le texte soit rejeté. Les députés" \
                                        u" ont modivé leur décision et ils ont dit qu'ils pensent qu'une" \
                                        u" legalisation des drogues augmentera la criminalité et incitera les" \
                                        u" jeunes à utiliser des drogues."
                    correctedtextmainpage = re.sub(ur"soit revenu", u"est revenu",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"soit rejeté", u"a été rejeté",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"quelque députés", u"quelques députés",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 357:
                    origtextmainpage += u" beaucoup de confiance avec ma capacité de parler français. En réalité," \
                                        u" je parle français comme une vache espagnole!" \
                                        u" Je sais qu'un séjour en France" \
                                        u" ou dans un pays où les gens parlent en français serait un avantage." \
                                        u" Je voudrais participer au cours de langue français en France ou l'ideal" \
                                        u" serait aller au Quebec. Je voudrais aussi voir la civilisation" \
                                        u" de Canada et la pays aussi. J'ai l'occasion de voir la France dans" \
                                        u" ma troisieme année et cette chance n'arrive qu'une fois dans" \
                                        u" ma vie. Mais, avec réalisme et avec les limites d'argent, je pense" \
                                        u" qu'un cours en France serait la meilleure occasion pour moi. C'est pour" \
                                        u" ceux raisons là que je demande une allocation. Veuillez agréer Madame," \
                                        u" l'expression de mes sentiments distingués."
                    correctedtextmainpage = re.sub(ur"s'offre trop", u"est trop",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"ne pas la savoir", u"ne pas la saisir",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"en français", u"français",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"dans ma troisième", u"lors de ma troisième",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"raisons là", u"raisons-là",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 358:
                    origtextmainpage += u"ays. J'attends avec impatience de voyager à l'étranger, parce que je" \
                                        u" n'ai jamais aller tout seul vers un pays étrange. Il y aura une" \
                                        u" expérience inestimable que me préparera pour l'année prochaine. Quand" \
                                        u" je suis étudier dans les leçon et participer aux activités, en plus " \
                                        u"d'améliorer ma connaissance de la langue français, j'espère qu'il est" \
                                        u" aussi une possibilité d'améliorer moi-même. Le voyage m'aidera" \
                                        u" se développer plus d'amour-propre avec des gens et exprimer des choses" \
                                        u" en français plus assurées. En fin de compte, il est une bonne occasion" \
                                        u" pour moi de faire des progrès ainsi quand je rentre, je serai prêt" \
                                        u" pour l'annee prochaine."
                    correctedtextmainpage = re.sub(ur"voudrais de passer", u"voudrais passer",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"parle le français", u"parle français",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"je n'suis jamais", u"je ne suis jamais",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"je ai étudié dans", u"j'ai étudié",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"améliorer moi-même", u"améliorer",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"confiance quand je parle", u"confiance en moi quand je parlerai",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 359:
                    origtextmainpage += u"enir. Je crois que la meilleure façon en quelle je peux apprendre" \
                                        u" le français le plus est travaillèrent avec une famille française, comme" \
                                        u" une au pair, ou peut-être dans un café où la langue française est" \
                                        u" utilisé toujours et on n'a pas la chance de parler dans une autre" \
                                        u" langue. Avec une famille française, qui utilise la langue française" \
                                        u" seulement, je n'aurai pas l'occasion de parler en anglais, seulement" \
                                        u" s'ils veulent apprendre un peu d'anglais qui je peux les enseigner." \
                                        u" J'aurai aussi la chance d'éprouver la vie d'une famille française" \
                                        u" et apprendre sur la culture et les coutumes françaises. Avant" \
                                        u" travaillèrent en France, je veux faire du travail bénévole pour trois" \
                                        u" semaines dans un autre pays francophone. Je préférais aller au Canada" \
                                        u" ou en Afrique pour une autre expérience de la vie, la langue et la" \
                                        u" culture française en dehors de France. Si ce ne sera pas possible pour moi" \
                                        u" à travailler dans un autre pays francophone, je peux faire du travail" \
                                        u" bénévole en France ou en Belgique. Je voudrais faire du travail bénévole" \
                                        u" parce qu'il peut me donner une occasion de travailler avec les" \
                                        u" francophones sans pression et ce sera une expérience très différente" \
                                        u" où je peux aider les autres. Bien que je ne sois pas étudier le français" \
                                        u" pendant les vacances, je crois que ce que je peux faire me donnera une" \
                                        u" meilleure occasion d'apprendre la langue. Une bourse m'aidera payer" \
                                        u" pour mes coûts de voyage et ainsi me donne la chance de vivre en France" \
                                        u" et avec espoirs, dans un autre pays francophone et apprendre sur les" \
                                        u" autres cultures françaises différents dans le monde et les comparent."
                    correctedtextmainpage = re.sub(ur"la chance de parler", u"l'occasion de parler",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"est travailler", u"est de travailler",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"une au pair", u"une jeune fille au pair",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"et apprendre sur la culture", u"et d'apprendre la culture",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    #correctedtextmainpage = re.sub(ur"et apprendre sur l", u"et apprendre",
                    #                               correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur" ne est", u" n'est", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"coûts de voyage", u"dépenses de voyage",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"et avec espoirs", u"et si possible",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"et les comparent\.", u"et les comparer.",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"je ne aie pas", u"je n'aie pas",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"quel sorte", u"quelle sorte",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 361:
                    origtextmainpage += u"pe dans le Vatican, la fontaine de trevi et la chapelle de Michaelangelo," \
                                        u" très beau. Nous avons voulu aller à Naples mais nous avons appris qu'il" \
                                        u" y avait beaucoup de crimes. Au lieu de Naples nous sommes allés au" \
                                        u" Venise. Ironiquement un voleur italien a pris nos sacs sur le train" \
                                        u" quand nous dormions. Mais c'est la vie. Marseille était déplaisante." \
                                        u" Un mois avant nos vacances, pendant la Coupe du monde, des voyous anglais" \
                                        u" ont saccagé la ville. Les habitants de cette ville n'avaient pas oublier." \
                                        u" A Barcelone, nous étions fatigués et nous nous sommes" \
                                        u" détendus. C'est tout." \
                                        u" J'ai fini. Est-ce qu'il y a des questions? Jon? Vous avez une question" \
                                        u" pour moi n' est-ce pas?"
                    correctedtextmainpage = re.sub(ur"la mosquée bleue", u"la Mosquée Bleue",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Rome était très intéressant", u"Rome était très intéressante",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"colluseum", u"Collisée",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"le pape dans le", u"le pape au",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"de trevi", u"de Trevi",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"très beau\.", u"très belle.",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"au Venise\.", u"à Venise.",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"sur le train", u"dans le train",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"pas oublier", u"pas oublié",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"question pour moi", u"question pour moi,",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Michaelangelo", u"Michelangelo",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 362:
                    origtextmainpage += u"i et aujourd'hui le groupe jouait un très grand concert à Manchester, la" \
                                        u" ville où tout le groupe habite, alors ils sont restés chez Noël( l'homme" \
                                        u" qui joue la guitare ici) . Ils n'ont pas pu quitter la maison parce qu'à" \
                                        u" l'extérieur il y avait deux ou trois cent fanatiques qui ont voulu voir" \
                                        u" leur héros. Ils ont dû rester et attendre la police et la limousine. Il" \
                                        u" y avait rien d'intérressant à la télévision et ils étaient tout anxieux," \
                                        u" donc Noël a dit\" qui veut un peu de vin? J'ai une bouteille ou cinq" \
                                        u" dans la cuisine! C'est un Côtes du Rhone" \
                                        u" mille neuf cent quatre-vingt treize de Tesco." \
                                        u" C'était une très bonne année! \" Tout le monde a dit\" oui\" et alors" \
                                        u" pendant deux heures ils ont bu beaucoup de vin pour se détendre." \
                                        u" Soudainement le temps a passé plus vite, la télévision était plus" \
                                        u" intéressante et Noël a joué des chansons. Malheureusement personne" \
                                        u" n'a vu que Liam buvait plus que les autres... .en fait il n'a pas" \
                                        u" pu marcher ou parler. C'était un grand problème parce qu'il est le" \
                                        u" chanteur! Les autres dans la bande ont porté Liam à la chambre de" \
                                        u" Noël où il existe un mur avec une puissance mystérieuse qui s'appelle" \
                                        u" Wonderwall. C'est aussi le sujet d'une des chansons du groupe." \
                                        u" C'était désespéré mais c'était la seule chance pour sauver le concert." \
                                        u" Ils sont retourné après deux heures et étonnament Liam était en bonne" \
                                        u" santé! Noël a déclaré que c'était un miracle. Le mur a évité le" \
                                        u" concert. Le concert était la plus grande épreuve musicale de l'année," \
                                        u" avec vingt-cinq mille personnes dans le stade. Ils ne pouvaient pas" \
                                        u" connaître les difficultés de la bande pendant l'après-midi."
                    correctedtextmainpage = re.sub(ur"et aujourd'hui", u"et ce jour-là",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"joue la guitare", u"joue de la guitare",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"de la groupe", u"du groupe",
                                                   correctedtextmainpage, flags=re.UNICODE) # this fixes 2 occurences
                    correctedtextmainpage = re.sub(ur"la groupe", u"le groupe",
                                                   correctedtextmainpage, flags=re.UNICODE) # this fixes 2 occurences
                elif entryNumber == 363:
                    origtextmainpage += u"oses qui se sont passées pendant mes vacances en Kenya. Surtout, Je me" \
                                        u" souviens du match de rugby contre l'école pas loin de la location de" \
                                        u" mon travail. Nous avons voyagé en bus à l'école, mais après environ" \
                                        u" une heure le bus s'est arrêté soudainement. Il y avait beaucoup de" \
                                        u" bruit, y compris des coups de feu. A ce moment là, trois hommes de" \
                                        u" pauvre apparence, armés j'usq' aux dents sont embarqué dans le bus." \
                                        u" Ils ont ordonné que tout le monde descendre. Nous avons été ligotés," \
                                        u" et ils nous avons renversé sur la terre. C'était une situation" \
                                        u" inquiétante! Nous avions la terreur d'être assassine! Bientôt," \
                                        u" les eleves étaient libérés, mais nous nous restions où nous étions." \
                                        u" Ils nous ont mis en camionette, et ils ont conduit, je ne sais où," \
                                        u" quelque part. La nuit tombait. Il faissait froid et nous avions faim." \
                                        u" Après plusieurs heures de bavardage en Swahili, nous les avons persuadé" \
                                        u" que nous étions bénévoles et que nous n'avions pas d'argent. Jusqu'à" \
                                        u" une heure avancée de la nuit nous étions déposé au faubourg d'Eldoret." \
                                        u" Nous sommes resté plus long-temps dans le commissariat de police que" \
                                        u" les bandits! Inutile de dire qu'ils n'ont jamais étaient capturé, et nous" \
                                        u" ne sommes joué pas au rugby ce jour!"
                    origtextmainpage = re.sub(ur"Kapsabet\' \.", u"Kapsabet\'.", origtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"L autre", u"L'autre", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"qui avant mon arrivée", u"que avant mon arrivée",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"de la location de mon", u"du lieu de mon",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"en bus à l'école", u"en bus vers l'école",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"j'jusqu", u"jusqu", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"ils nous ont renversé sur la terre", u"ils nous ont jeté à terre",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"en camionette", u"en camionnette",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"où,\s+quelque part", u"où", correctedtextmainpage, flags=re.UNICODE)
                    #print "weird", u"où,\s+quelque part" in correctedtextmainpage
                    correctedtextmainpage = re.sub(ur"ne avons joué pas", u"n'avons pas joué", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"rugby ce jour", u"rugby ce jour-là",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"étions déposé", u"étions déposés",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 364:
                    origtextmainpage += u"us sommes catholiques. Le deux jour suivant, il y a des danceurs qui" \
                                        u" dancent pour las rues avec des groups de musiciens pendant la" \
                                        u" journée. Tout les groupes des danceurs sont organizees de façon qui" \
                                        u" ils peuvent dancer sans problèmes. Cette célébration a trois raisons:" \
                                        u" la fête de la ville, la fête d'une virgen et la fête du roi du minas." \
                                        u" Tout les gens parcitipent et pendant cet jours. la ville être vivre et" \
                                        u" ou peut voir des gens qui jamais on a vu et tous sont heureux d'être" \
                                        u" de la ville et de participier de la fête."
                    correctedtextmainpage = re.sub(ur"la fête de la ville est", u"La fête de la ville est",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"\.\s+de\s+façon\s+qui", u" de façon qu'",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"être vit", u"vit", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"jour suivant", u"jour", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"du mines", u"des mines", correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 365:
                    origtextmainpage += u" ils crient, ils rient en jettant les oranges."
                elif entryNumber == 366:
                    origtextmainpage += u"ille pendant des fêtes dans des petits villes an Italie. Une fanfare" \
                                        u" la jouait. Tout le monde tapent les mains avec le rythme."
                    correctedtextmainpage = re.sub(ur"tape des mains avec le rythme", u"tape des mains en rythme",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 367:
                    origtextmainpage += u" oublier leure impatience et leures inquiétudes. Les armes brillent dans" \
                                        u" le soleil levant, les uniformes ofrent une mélange des couleurs" \
                                        u" inimaginable. Et malgré tout, dans quelques heures seulement, les" \
                                        u" mêmes armes seront cassés, les mêmes uniformes pleines de poussière" \
                                        u" et de sang."
                    correctedtextmainpage = re.sub(ur"les faire oublier", u"oublier",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"inimaginable", u"inimaginables",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 368:
                    origtextmainpage += u"onsommateurs et patrons. D'abord, il y a des arguments économiques" \
                                        u" qu'avec l'ouverture dominicale le chiffre d'affaires augmenterait" \
                                        u" jusqu'au ciel. Mais l'argent pour cet augmentation, d'ou vient-il?" \
                                        u" Les gens n' acheteront plus parce qu'il y aura un autre jour pour" \
                                        u" acheter, mais pas un autre pour consommer. Bien sûr, il faut respecter" \
                                        u" les exceptions pour les droits élémentaires: les hopitaux, les moyens" \
                                        u" de transport etc. Mais ce sont des exceptions, ce n'est pas la règle" \
                                        u" parce que aussi les salariés, ils ont le droit de liberté, la liberté" \
                                        u" d'un jour de repos familial. même pour les autres, le dimanche doit" \
                                        u" rester un jour de récréation sous la pression de la vie quotidienne." \
                                        u" La liberté, c'est aussi la liberté des autres. Ma liberté de faire" \
                                        u" les courses quand je veux se termine où a liberté des salariés commence:" \
                                        u" le dimanche."
                    correctedtextmainpage = re.sub(ur"la demande de la déréglementation",
                                                   u"la demande de déréglementation",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"et patrons", u"et les patrons", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"salariés,\s+ils", u"salariés", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"termine où a liberté", u"termine là où la liberté",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 369:
                    origtextmainpage += u" serieux. Dans les jours d'après tous les ètudiants portait la radio" \
                                        u" avec eux pour écouter les dernières nouvelles. Tout le monde parlait" \
                                        u" de la 3ème guerre mondial, comme maintenant à Kosovo. Les gens avaient" \
                                        u" peur des bombes nucleaires et biologiques. Les disputes pour ou contre" \
                                        u" l'OTAN etaient toujour les mêmes. Moi aussi j'ai commencé à donner mon" \
                                        u" opinion: ça va ou ne va pas arriver, etc.. sans savoir vraimente la" \
                                        u" verité C'est pour ça que maintenant je ne crois pas tout que les" \
                                        u" journals dissent. avec Kosovo. J'ai été choqué, bien sur, mais" \
                                        u" la panique et e peur pour la 3e eme guerre Mondial ou la guerre" \
                                        u" atomique a disparu. Ca ne veut pas de tout dire que on se sent pas" \
                                        u" triste et solidaire avec les gens qui suffrent en place."
                    correctedtextmainpage = re.sub(ur"dans la pause", u"pendant la pause",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"écouté à", u"écouté", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"de parler sur", u"de parler de",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"tout que", u"tout ce que",
                               correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"ent\. à propos du Kosovo", u"ent à propos du Kosovo",
                               correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"J'ai été choqué", u"J'ai été choquée",
                               correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"étudiant portaient", u"étudiants portaient",
                               correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'vérité C\'est', u'vérité. C\'est',
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'3e eme', u'3e',
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 370:
                    origtextmainpage += u", comment ils s'appellent et surtout savoir si mon frère avait été" \
                                        u" blessé pour l'impact de la bombe. Tout d'abord j'ai changé le channel" \
                                        u" de la radio pour vérifier la nouvel. Après je parlait à mes parents" \
                                        u" sur les faits et je leur expliquais qu'il avait" \
                                        u" malheureusement un mort, c'était un militaire. La nouvel avait" \
                                        u" été très discuté et toute la ville ne parlait que des assassins" \
                                        u" d'ETA. C'est difficile à croire comment ils peuvent demander" \
                                        u" un droit, le droit d'être independantes de l'Espagne, en attentant" \
                                        u" contre des autres droits humains et se faisant prévaloir d'un systéme" \
                                        u" democratique. Je crois qu'il y a plusieurs manières de demander" \
                                        u"- les choses mais ce qu'il n'est pas acceptable c'est le fait de" \
                                        u" tuer des personnes pour ideologies."
                    correctedtextmainpage = re.sub(ur"jea l'ai", u"je l'ai",
                               correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Je l'avait appris", u"Je l'avais appris",
                               correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"au sujet des les", u"au sujet des",
                               correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'ce quiil', u'ce qui', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'C\'est difficile à croire', u'Il est difficile de croire',
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'des autres droits', u'd\'autres droits',
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 371:
                    origtextmainpage += u" volonté de crier au monde notre desapprovetion devait dévénir réelle et" \
                                        u" éfficace. Le matin suivent beaucoup d'étudiants avaient eu la même" \
                                        u" idée et un cortège spontané allait se former dans la ville pour" \
                                        u" manifester notre indignation. On ne pouvait pas tues les étudiants" \
                                        u" universitaires qui se croiait la vrai expression de la culture," \
                                        u" comme des petites bêtes sans valeur."
                    correctedtextmainpage = re.sub(ur"ami dans un", u"ami un", correctedtextmainpage, flags=re.UNICODE)
                # back to nomral:
                elif entryNumber == 372:
                    correctedtextmainpage = re.sub(ur"ceci", u"Ceci", correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 373:
                    correctedtextmainpage = re.sub(ur"troux", u"trou", correctedtextmainpage, flags=re.UNICODE)

                elif entryNumber == 377:
                    correctedtextmainpage = re.sub(ur"qui a eu une fille", u"qui avait une fille",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"rester chez moi", u"chez moi",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"soulagées", u"rassurées",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur",\s+souci,\s+et", u" et",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"n'a\s+pas servi à rien", u"n'a servi à rien",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"tous recueilli", u"tous recueillis",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"il ont", u"ils ont",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 378:
                    correctedtextmainpage = re.sub(ur"envers l'", u"envers ",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Je suis une espagnole", u"Je suis une Espagnole",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"en derrière", u"derrière",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"co\-koteurs\"\s+on", u"co-koteurs\", on",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 379:
                    correctedtextmainpage = re.sub(ur"qui ils", u"qu'ils",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"partout elle", u"partout et elle",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 380:
                    correctedtextmainpage = re.sub(ur"dans mes mains", u"aux mains",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"quelquefois", u"quelque fois",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"des les choses", u"des choses",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"le corps Comme", u"le corps. Comme",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    origtextmainpage = re.sub(ur"le corps Comme", u"le corps. Comme",
                                                   origtextmainpage, flags=re.UNICODE) # benefit of the doubt to the student with a missing .
                    correctedtextmainpage = re.sub(ur"aux mains ça", u"aux mains, ça",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 381:
                    correctedtextmainpage = re.sub(ur"porte clef", u"porte-clefs",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"cadeaux", u"cadeau",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"que j'ai acheté", u"que j'ai achetés",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"pour quoi", u"pourquoi",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"deux chose ", u"deux choses ",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"je jamais n'ai utilisé un",
                                                   u"je n'en ai jamais utilisé",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"des petites folies", u"petites feuilles",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"codes,\s+numéros", u"numéros",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"portefeuille qui avec", u"portefeuille, qui avec",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 382:
                    correctedtextmainpage = re.sub(ur"que il y a pas", u"qu'il n' y a pas",
                                                   correctedtextmainpage, flags=re.UNICODE) # strange spacing
                    correctedtextmainpage = re.sub(ur"la Amérique", u"Amérique",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"tout les", u"tous les",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"qu'a le", u"qui ont le",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"la intégration", u"l'intégration",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"de une", u"d'un",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"il n'a pas possible", u"ce n'est pas possible",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"cette développement", u"ce développement",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"discrimination,\s+cette", u"discrimination. Cette",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 383:
                    correctedtextmainpage = re.sub(ur"Thème", u"thème",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"ma pays", u"mon pays",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"s'appelle Bolivie", u"s'appelle la Bollivie",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"un épouse", u"un époux",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"et Travaillent", u"et travaillent",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"une pays développement", u"un pays développé",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"une 30\%", u"30%",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"rien Elles sont", u"rien. Elles sont",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    origtextmainpage = re.sub(ur"rien Elles sont", u"rien. Elles sont",
                                                   origtextmainpage, flags=re.UNICODE) # benefit of doubt to student
                elif entryNumber == 384:
                    correctedtextmainpage = re.sub(ur"dans nouvelle", u"dans une nouvelle",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"pour veille", u"pour veiller",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"a la femme", u"à la femme",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"important pour", u"importante pour",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"c'estune", u"c'est une",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 385:
                    correctedtextmainpage = re.sub(ur"la évolution", u"l'évolution",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"à ces lieux", u"dans ces lieux",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"certains choses que ce n'", u"certaines choses qui ne ",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"faciles de trouver", u"faciles à trouver",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"en autre pays", u"dans d'autres pays",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"je adore", u"j'adore",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"du couleur", u"de la couleur",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"en leur travail artisanale", u"dans leur travail artisanal",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Je enjoi de", u"J'apprécie",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"de les gens", u"des gens",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"mon sprit", u"mon esprit",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"ce richesse culturel", u"cette richesse culturelle",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"des vacances je", u"des vacances, je",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 386:
                    correctedtextmainpage = re.sub(ur"la place très important", u"une place très importante",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Le différentes cultures et religions",
                                                   u"Les différences culturelles et religieuses",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"sont très important", u"sont très importantes",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"de\s+femme\,\s+c\'est\s+clair", u"de la femme, il est clair",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"occupe des affaires", u"s'occupe des affaires",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"tout jour", u"toujours",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"pour mange pour tout le", u"à manger pour toute la",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"le majorité de femme", u"la majorité des femmes",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Le\s+rôle\s+de\s+femme c'est beaucoup comment",
                                                   u"Le rôle de la femme est grand si",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"ne pas occupe", u"n'occupe pas",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"la problème de l'émancipation de",
                                                   u"du problème de l'émancipation de la",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 387:
                    correctedtextmainpage = re.sub(ur"qui elles ne", u"qu'elles ne",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"que après elle fait", u"qui fait après",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"que après elle fait", u"qui fait après",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"elle a plusieurs", u"a plusieurs",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"majorité de femmes", u"majorité des femmes",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"moins posibilités", u"moins de possibilités",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"n'ont fait pas", u"n'ont pas fait",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"desenfants", u"des enfants",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 388:
                    correctedtextmainpage = re.sub(ur"Je crois toutes", u"Je crois que toutes",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur" ne utilisent", u" qui n'utilisent",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"nationales et régionales langues",
                                                   u"langues nationales et régionales",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"e\.  x\.  Maroc c'est", u"par ex. le Maroc est",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"une arabe pays", u"un pays arabe",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"cette pays", u"ce pays",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"le Français", u"le français",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"l'université,  Algérie", u"à l'université algérienne a",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"la même problème", u"le même problème",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"obliger la", u"rendre obligatoires les",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"a l'école", u"à l'école",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"a partir", u"à partir",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"l'arabe il", u"l'arabe",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"dans l'université", u"à l'université",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"université,\s+à\s+l'école", u"université et à l'école",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"ensemble", u"",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"français pour", u"français et ce pour",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"dans l'école", u"à l'école",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 389:
                    correctedtextmainpage = re.sub(ur"la femme toujours a", u"la femme a toujours",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"en occuper", u"en occupant",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"travers de plusieurs", u"travers plusieurs",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"par partie des femmes", u"par des mouvements des femmes",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"participer dans", u"participer à",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Actuellement,\s+au Panama", u"Actuellement au Panama,",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 390:
                    correctedtextmainpage = re.sub(ur"été plus pire", u"était pire",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"le vol de", u"la place de",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"femme en la société", u"femme dans la société",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"beaucoup mieux parce que", u"bien meilleure parce qu'",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"occupant charges", u"occupant des charges",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"plus meilleurs qui", u"meilleures qu'",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"aident a la", u"aident la",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 391:
                    correctedtextmainpage = re.sub(ur"Régionales", u"régionales",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"plus importants", u"importants",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"petits groupes des", u"des petits groupes d'",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"etc...", u"etc.",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 392:
                    correctedtextmainpage = re.sub(ur"certains droit", u"certains droits",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"tous niveaux", u"tous les niveaux",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"en rapport", u"par rapport",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"qui encore existe", u"qui existe encore",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"pour réussir", u"pour obtenir",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"quelques choses", u"choses",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 393:
                    correctedtextmainpage = re.sub(ur"D'e abord", u"D'abord",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"que envisage", u"qui envisagent",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"que sont mises", u"qui sont mises",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"des femmes qui se trouvent", u"des femmes qui sont",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"été Président", u"été présidentes",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 394:
                    correctedtextmainpage = re.sub(ur"tous le monde", u"tout le monde",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"traditions sociale", u"traditions sociales",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"engurance", u"spoliation",
                                                   correctedtextmainpage, flags=re.UNICODE)

                print "orig:", origtextmainpage
                print "corrected:", correctedtextmainpage
                reducedcorrected = correctedtextmainpage
                reducedoriginal = origtextmainpage

                origtext = u""
                correctedText = u""

                outhtmlfilename = "/home/nparslow/Documents/AutoCorrige/SpellChecker/entryhtml/entry_" + str(
                    entryNumber) + ".html"
                '''
                # download the html from web mode:
                detailslink = "http://www.lhaire.org/corpus/compact.php?id=" + str(entryNumber)
                response = urllib2.urlopen(detailslink)
                html = response.read()
                '''

                with codecs.open(outhtmlfilename, mode='r') as htmlfile:
                    html = htmlfile.read()

                '''
                # download the html mode:
                with codecs.open(outhtmlfilename, mode="w") as outhtmlfile:
                    outhtmlfile.write(html) # will be in latin1

                '''

                subsoup = BeautifulSoup(html)

                worderrors = []
                subtable = subsoup.find('table')
                lastwordsearch = None  # will be stocked in case of failure
                lastword = None  # to check for repeated ***

                for subrow in subtable.findAll('tr'):
                    subcols = subrow.findAll('td')
                    if len(subcols) > 0:
                        # we want the first 2 strings of first column
                        counter = 0
                        word = None
                        cat = None
                        wordlabel = None
                        # *** = end of phrase?
                        for string in subcols[0].stripped_strings:
                            if counter == 0: word = string
                            if counter == 1: cat = string
                            if counter == 2: wordlabel = string
                            counter += 1
                        # print word, cat

                        # we only want the first string of the second column, the tag
                        # the second string describes the tag and starts with "-"
                        # if it's 'Aucune valeur', we ignore it.
                        errors = []
                        if len(subcols) > 1:
                            for string in subcols[1].stripped_strings:
                                if string != "Aucune valeur" and not string[0] == "-":
                                    errors.append(string)

                        # the 3rd column has fipsortho proposed corrections, we don't want them
                        # for the 4th column, we want the replacement text (note '-' = remove)
                        correctedWord = None
                        if len(subcols) > 3:
                            for string in subcols[3].stripped_strings:
                                # print "col 3:", string
                                correctedWord = string

                        #print "error:", word, cat, errors, correctedWord

                        # reconstruct with ambiguous punctuation,
                        #  double *** = end of sentence (single *** for the last sentence though)
                        # *** is sometimes replaced by nothing though ...
                        '''
                        nextwordsearch = correctedWord
                        if correctedWord == "-": nextwordsearch = ""
                        if correctedWord is None:
                            if word != "***":
                                nextwordsearch = word
                            else:
                                nextwordsearch = ur"" # as a punct mark can be forgotten, already included in search
                        '''
                        # in corrected version can have:
                        # - corrected word
                        # - original word (seriously!)
                        # - both original word and corrected word
                        nextwordsearch = ur""

                        # Errors in the corpus, words to remove not noted with '-'
                        if entryNumber == 11:
                            if wordlabel == "i00016":
                                word = u"soldats,"
                                # correctedWord = "soldats,"
                            if wordlabel == "i00022":
                                word = u"roi,"
                                # correctedWord = "roi,"
                                # probably shouldn't be with comma, but it's acceptable for emphasis on the last element
                        elif entryNumber == 16:
                            if wordlabel == "i00014": word = u"Ouest,"
                            if wordlabel == "i00017": word = u"fourrures,"
                            if wordlabel == "i00007": word = u"multiples;"
                            if wordlabel == "i00020": word = u"Amérindiens,"
                        elif entryNumber == 18:
                            if wordlabel == "i00010":
                                word = u"anglais,"
                                correctedWord = u"anglaise,"
                            if wordlabel == "i00011": word = u"hollandais,"
                        elif entryNumber == 27:
                            if wordlabel == "i00004": word = u"métier,"
                            if wordlabel == "i00006": word = u"religieux,"
                            if wordlabel == "i00008": word = u"soldats,"
                            if wordlabel == "i00012": word = u"roi,"
                        elif entryNumber == 29:
                            if wordlabel == "i00006":
                                word = "problemes,"
                                correctedWord = u"problèmes,"
                            if wordlabel == "i00009": word = u"maladies,"
                            if wordlabel == "i00012": word = u"corsaires,"
                        elif entryNumber == 39:
                            if wordlabel == "i00003": word = u"cérémonie,"
                        elif entryNumber == 41:
                            if wordlabel == "i00022": word = u"cérémonie,"
                        elif entryNumber == 43:
                            if wordlabel == "i00022":
                                word = u"content,"
                                correctedWord = u"content;"  # or perhaps should be . ????? (no correction given)
                        elif entryNumber == 45:
                            if wordlabel == "i00013": word = u"parents,"
                        elif entryNumber == 55:
                            if wordlabel == "i00015": word = u"heures,"
                            if wordlabel == "i00018": word = u"soirs."
                        elif entryNumber == 60:
                            if wordlabel == "i00030": word = u"'Europe"
                        elif entryNumber == 83:
                            if wordlabel == "i00024": correctedWord = u"veut"
                            if wordlabel == "i00025": correctedWord = u"ainsi"  # word order swap
                            if wordlabel == "i00026": word = u"-elle"
                        elif entryNumber == 106:
                            if wordlabel == "i00014": word = u"'s"
                        elif entryNumber == 111:
                            if wordlabel == "i00004": word = u"Mai,"
                        elif entryNumber == 117:
                            if wordlabel == "i00004": word = u"-ils"
                        elif entryNumber == 121:
                            if wordlabel == "i00008": word = u"-vous"
                        elif entryNumber == 126:
                            if wordlabel == "i00016": correctedWord = None
                            if wordlabel == "i00010": correctedWord = u"le"
                            if wordlabel == "i00012": correctedWord = u"préféré"
                        elif entryNumber == 127:
                            if wordlabel == "i00004": correctedWord = u"vous"
                        elif entryNumber == 128:
                            if wordlabel == "i00002": word = u"-vous"
                        elif entryNumber == 133:
                            if word == "J'": correctedWord = u"Je"
                            if word == "ai": correctedWord = u"-"
                            if wordlabel == "i00027": correctedWord = u"me réjouis"
                        elif entryNumber == 138:
                            if wordlabel == "i00019": word = u"Asie,"
                        elif entryNumber == 139:
                            if wordlabel == "i00006": word = u"Alors..."  # no *** for the ... :/
                        elif entryNumber == 140:
                            if wordlabel == "i00010": word = u"-tu"
                            if wordlabel == "i00016": word = u"-ils"
                        elif entryNumber == 143:
                            if wordlabel == "i00023": word = u"-toi"
                        elif entryNumber == 157:
                            if wordlabel == "i00020": word = u"-tu?"
                            if wordlabel == "i00015": word = u"souvenis,"
                        elif entryNumber == 163:
                            if wordlabel == "i00001": word = u"Puis,"
                        elif entryNumber == 164:
                            if wordlabel == "i00018":
                                correctedWord = u"que quand" # todo added error
                                errors = ["MAN"]
                        elif entryNumber == 171:
                            if wordlabel == "i00004": word = u"pas,"
                        elif entryNumber == 176:
                            if wordlabel == "i00020": correctedWord = u"bons"
                            if wordlabel == "i00021": correctedWord = u"petits"
                        elif entryNumber == 179:  # no *** for "
                            if wordlabel == "i00008":
                                word = u'"Blue'
                                correctedWord = u'"Blue'
                            if wordlabel == "i00009":
                                word = u'Mountain"'
                                correctedWord = u'Mountains"'
                        elif entryNumber == 185:
                            if wordlabel == "i00005":
                                word = u"-tu"
                                correctedWord = u"-tu?"
                        elif entryNumber == 186:
                            if wordlabel == "i00027":
                                word = u"-tu"
                            if wordlabel == "i00015": correctedWord = u"aies" # typo in corrected version
                        elif entryNumber == 187:
                            if wordlabel == 'i00007':
                                word = u"excitée,"
                        elif entryNumber == 189:
                            if wordlabel == "i00014":
                                correctedWord = u"prochains"
                            if wordlabel == "i00015":
                                correctedWord = u"mois"
                            if wordlabel == "i00004": correctedWord = None
                            if wordlabel == "i00005": correctedWord = None
                            if wordlabel == "i00006": correctedWord = u"-à"
                            if wordlabel == "i00007": correctedWord = u"-dire"
                        elif entryNumber == 191:
                            if wordlabel == "i00002": word = u"-moi"
                            if wordlabel == "i00014": word = u"voyage,"
                            if wordlabel == "i00015": correctedWord = u"Et"
                        elif entryNumber == 195:
                            # if word == "Je": correctedWord = "-"
                            #  keep Je as it is the same in both orig and corr versions
                            if word == "suis": correctedWord = u"-"
                            if word == u"très": correctedWord = u"-"
                            if word == u"exalté": correctedWord = u"me réjouis"
                        elif entryNumber == 208:
                            if word == "ma": correctedWord = u"mon"
                        elif entryNumber == 213:
                            if wordlabel == "i00012": correctedWord = u"chef"
                            # TODO this was 'uncorrectable', _UNKNOWN???
                        elif entryNumber == 214:
                            if wordlabel == "i00014": correctedWord = u"À"
                            # A is ok, but to be consistent with the other form
                        elif entryNumber == 218:
                            if wordlabel == "i00010":
                                correctedWord = u"grands"
                                errors = ["AGR"]
                            if wordlabel == "i00011": correctedWord = u"ouragans"
                            if wordlabel == "i00012": correctedWord = u"simultanés" # word order and spelling!
                        elif entryNumber ==  225:
                            if wordlabel == "i00002": correctedWord = u"y suis"
                            if wordlabel == "i00003": correctedWord = u"allé"
                        elif entryNumber == 226:
                            if word == "avec" and wordlabel == "i00015": correctedWord = u"-"
                            if word == "un" and wordlabel == "i00016": correctedWord = u"-"
                            if word == "sauce" and wordlabel == "i00018": correctedWord = u"-"
                            # print "corr word", correctedWord
                        elif entryNumber == 233:
                            if wordlabel == "i00008":
                                correctedWord = u"en ajoutant"
                                errors = ["LEX"]
                            if wordlabel == "i00010":
                                correctedWord = u"touche"
                                errors = ["LEX"]
                        elif entryNumber == 240:
                            if wordlabel == "i00032": word = u"[much"
                            if wordlabel == "i00033": word = u"more]"
                        elif entryNumber == 241:
                            if wordlabel == "i00008":
                                correctedWord = u"plats"
                            if wordlabel == "i00009":
                                correctedWord = u"favoris"
                            if wordlabel == "i00011":
                                correctedWord = u"le salsa"
                            if wordlabel == "i00014":
                                correctedWord = u"le pain"
                                errors = ["MAN"]
                        elif entryNumber == 247:
                            if wordlabel == "i00014": word = u"C,"
                        elif entryNumber == 251:
                            if wordlabel == "i00027":
                                correctedWord = u"se complète"
                                errors.append("AGR")
                            if wordlabel == "i00028":
                                correctedWord = u"celui"
                                errors = ["LEX"]
                            if wordlabel == "i00029":
                                correctedWord = u"des autres"
                                errors = ["AGR"]
                        elif entryNumber == 257:
                            if wordlabel == "i00008":
                                correctedWord = u"géniaux" # todo new error addded here
                        elif entryNumber == 268: # here we have an error that crosses a sentence bound so we split it (as otherwise alignment is too hard)
                            if wordlabel == "i00019":
                                word = u"violet."
                                correctedWord = "violettes."
                            if wordlabel == "i00020":
                                word = u"L'ambiance"
                                correctedWord = "L'ambiance est"
                        elif entryNumber == 269: # here we have an error that crosses a sentence bound so we split it (as otherwise alignment is too hard)
                            if wordlabel == "i00005":
                                word = "soir."
                                correctedWord = "soir."
                            if wordlabel == "i00006":
                                word = "Cette restaurante"
                                correctedWord = "Ce restaurant"
                        elif entryNumber == 271:
                            if wordlabel == "i00005": word = u"rapide,"
                        elif entryNumber == 272:
                            if wordlabel == "i00008":
                                correctedWord = u"par contre,"
                                errors = ["PNC"] # todo new error added

                        elif entryNumber == 275:
                            if wordlabel == "i00018": word = u"rapidement,"
                            if wordlabel == "i00005":
                                correctedWord = u"commencé,"
                                errors.append("PNC")
                        elif entryNumber == 277:
                            if wordlabel == "i00021": correctedWord = u"révélée"
                        elif entryNumber == 278:
                            if wordlabel == "i00035": correctedWord = u"le" # to agree with other correction
                            if wordlabel == "i00021":
                                correctedWord = u"s'accompagnent"
                                errors = ["LEX"]
                        elif entryNumber == 281:
                            if wordlabel == "i00018": correctedWord = u"quelle" # to match agreeement
                        elif entryNumber == 332:
                            if wordlabel == "i00008": correctedWord = u"-"
                            if wordlabel == "i00004":
                                correctedWord = u"petite,"
                                errors = ["PNC"] # Punctuation : todo new error added here
                        elif entryNumber == 334:
                            if wordlabel == "i00004":
                                correctedWord = u"petite,"
                                errors = ["PNC"] # Punctuation : todo new error added here
                        elif entryNumber == 335:
                            if wordlabel == "i00004":
                                correctedWord = u"petite,"
                                errors = ["PNC"] # Punctuation : todo new error added here

                        elif entryNumber == 336:
                            if wordlabel == "i00060": correctedWord = u"Guérilla"
                        elif entryNumber == 337:
                            if wordlabel == "i00122": correctedWord = u"Afin"
                        elif entryNumber == 338:
                            #if wordlabel == "i00039":
                            #    correctedWord = u"a"
                            #    errors = [u"DIA"]
                            if wordlabel == "i00031":
                                correctedWord = u"Par conséquent,"
                                errors = ["PNC"]
                        elif entryNumber == 342:
                            if wordlabel == "i00062":
                                word = u"des" # remove extra  *
                                correctedWord = u"des enquêtes"
                        elif entryNumber == 344:
                            if wordlabel == "i00012":
                                correctedWord = u"SA."
                        elif entryNumber == 346:
                            if wordlabel == "i00022":
                                correctedWord = u"État"
                        elif entryNumber == 347:
                            if wordlabel == "i00017":
                                correctedWord = u"un"  # not a mistake but needed for the change in noun
                            if wordlabel == "i00075": correctedWord = u"un"  # ditto
                        elif entryNumber == 349:
                            if wordlabel == "i00027": correctedWord = u"suspendu"
                            # this is same as original word but doesn't
                            #  fit the context, not obvious what to replace it with
                            # but the same is better than ? as in the corpus
                        elif entryNumber == 350:
                            if wordlabel == "i00136":
                                correctedWord = u"promulgué"
                            if wordlabel == "i00100":
                                correctedWord = u"Hier,"
                                errors = ["PNC"]
                        elif entryNumber == 351:
                            if wordlabel == "i00069": correctedWord = u"le"
                            if wordlabel == "i00070":
                                correctedWord = u"coût"
                                errors = ["AGR"]
                            if wordlabel == "i00071":
                                correctedWord = u"d'"
                                errors = ["LEX"]
                            if wordlabel == "i00048":
                                correctedWord = u", en effet,"
                                errors = ["LEX"]
                        elif entryNumber == 353:
                            if wordlabel == "i00001": correctedWord = u"Le" # needed for agreement with changed word
                            if wordlabel == "i00094": correctedWord = u"pensant" # corrected by spellchecker incorrectly
                        elif entryNumber == 356:
                            if wordlabel == "i00082":
                                correctedWord = u"quelques"
                                errors = ["AGR"]
                        elif entryNumber == 358:
                            if wordlabel == "i00055": correctedWord = u"ne" # correct n',
                            #  but change in aux requires change here
                            if wordlabel == "i00079": correctedWord = u"j'" # ditto
                            if wordlabel == "i00020":
                                correctedWord = u"confiance en moi"
                                errors = ["MAN"] # todo added error
                            if wordlabel == "i00023":
                                correctedWord = u"parlerai"
                                errors = ["TMP"]
                        elif entryNumber == 359:
                            if wordlabel == "i00196": correctedWord = u"n'" # ditto
                            if wordlabel == "i00255": correctedWord = u"n'" # ditto
                            if wordlabel == "i00089": correctedWord = u"l'" # ditto
                            if wordlabel == "i00033": correctedWord = u"quelle" # ditto (agreement)
                        elif entryNumber == 362:
                            if wordlabel == "i00225": correctedWord = u"le" # ditto (agreement)
                            if wordlabel == "i00323": correctedWord = u"du" # ditto
                            if wordlabel == "i00324": correctedWord = "-"
                        elif entryNumber == 363:
                            if wordlabel == "i00074": correctedWord = u"du" # ditto
                            if wordlabel == "i00075": correctedWord = u"-" # ditto
                            if wordlabel == "i00176": correctedWord = u"camionnette" # same typo in corrected form lol
                            if wordlabel == "i00259": correctedWord = u"n'" # ditto style
                            if wordlabel == "i00229":
                                correctedWord = u"déposés" # todo found by frmg
                                errors = ["AGR"]
                        elif entryNumber == 364:
                            if wordlabel == "i00001": correctedWord = u"La"
                            if wordlabel == "i00014": correctedWord = u"mois" # mix up mois and jours
                            if wordlabel == "i00108": correctedWord = u"des" # matching correction
                        #elif entryNumber == 368:
                        #    if wordlabel == "i00177":
                        #        correctedWord = u"terminer" # missed correction <- nope it's not!!!!
                        #        errors = ["TPS"] # TPS = tense
                        elif entryNumber == 369:
                            if wordlabel == "i00063": correctedWord = u"étudiants"
                            if wordlabel == "i00158": correctedWord = u"-"
                        elif entryNumber == 370:
                            if wordlabel == "i00035": correctedWord = u"étais"
                            if wordlabel == "i00123":
                                correctedWord = u"Il"
                                errors = ["LEX"] # todo not really a good case for this label -> report
                            if wordlabel == "i00126":
                                correctedWord = u"de"
                                errors = ["LEX"] # todo not really a good case for this label -> report
                            if wordlabel == "i00145":
                                correctedWord = u"d'"
                                errors = ["AGR"] # todo not really a good case for this label -> report
                        elif entryNumber == 377:
                            if wordlabel == "i00261":
                                correctedWord = u"ils"
                                errors = ["AGR"] # AGR = agreement # todo : added error
                        elif entryNumber == 373:
                            if wordlabel == "i00001": correctedWord = u"Le"
                            if wordlabel == "i00002": correctedWord = u"trou" # uncorrected word was put as corrected


                        elif entryNumber == 378:
                            if wordlabel == "i00261": correctedWord = u"cohabitation"
                        elif entryNumber == 379:
                            if wordlabel == "i00057": correctedWord = u"qu'"
                            if wordlabel == "i00074":
                                correctedWord = u"et elle"
                                errors = ["MAN"] # todo new error, missing word
                        elif entryNumber == 380:
                            if wordlabel == "i00109":
                                correctedWord = u"mains,"
                                errors = ["PNC"]
                        elif entryNumber == 381:
                            if wordlabel == "i00068":
                                correctedWord = u"clefs,"
                                errors.append("PNC")
                        elif entryNumber == 382:
                            if wordlabel == "i00096": correctedWord = u"ce" # to match gender change of a correction
                            if wordlabel == "i00018":
                                correctedWord = u"qu'"
                                errors = ["HPO"] # not really appropriate todo (homophone existing)
                            if wordlabel == "i00024":
                                correctedWord = u"discrimination."
                                errors = ["PNC"]
                            if wordlabel == "i00025":
                                correctedWord = u"Cette"
                        elif entryNumber == 383:
                            if wordlabel == "i00041":
                                correctedWord = "-"
                                errors = ["SUP"] # superfluous word # todo new error
                        elif entryNumber == 385:
                            if wordlabel == "i00055": correctedWord = u"intéressants"
                            if wordlabel == "i00082": correctedWord = u"J'"
                            if wordlabel == "i00004":
                                correctedWord = u"des vacances,"
                                errors.append("PNC") # # todo : added error
                        elif entryNumber == 386:
                            if wordlabel == "i00032": correctedWord = u"affaires"
                        elif entryNumber == 387:
                            if wordlabel == "i00078": correctedWord = u"possibilités"
                        elif entryNumber == 388:
                            if wordlabel == "i00036":
                                correctedWord = "-"
                                errors = ["SUP"] # todo added error
                            if wordlabel == "i00050":
                                correctedWord = "-"
                                errors = ["SUP"]
                            if wordlabel == "i00070":
                                correctedWord = u"à"
                                errors = ["LEX"] # not really lex todo new error
                            if wordlabel == "i00057":
                                correctedWord = u"à l'"
                                errors = ["MAN"]
                            if wordlabel == "i00054":
                                correctedWord = u"à"
                                errors = ["LEX"] # not really lex todo new error
                            if wordlabel == "i00073":
                                correctedWord = u"et à"
                                errors.append("MAN")
                            if wordlabel == "i00076":
                                correctedWord = "-"
                                errors = ["SUP"]
                            if wordlabel == "i00083":
                                correctedWord = u"et ce pour"
                                errors = ["MAN"]
                        elif entryNumber == 389:
                            if wordlabel == "i00033":
                                correctedWord = u"Panama,"
                                errors = ["PNC"]
                        elif entryNumber == 391:
                            if wordlabel == "i00020":
                                correctedWord = u"etc."
                                errors = ["PNC"]
                        elif entryNumber == 394:
                            if wordlabel == "i00102": correctedWord = u"sociétés"

                        worderrors.append((word, errors, cat, correctedWord))

                        # escape all regex special chars :
                        # escape is maybe too strong as it does everything \W (inc unicode chars :/)
                        wordtouse = re.escape(word)
                        correctedwordtouse = wordtouse

                        nextwordsearch = ur""
                        nextorigwordsearch = wordtouse
                        # re.sub(r'([\.\\\+\*\?\[\^\]\$\(\)\{\}\!\<\>\|\:\-])', r'\\\1', "example string.")
                        if correctedWord is not None:
                            correctedwordtouse = re.escape(correctedWord)

                            if correctedWord == u"-":
                                # dash means 'should be dropped' but it isn't always dropped :/
                                nextwordsearch = ur""
                            else:
                                nextwordsearch = correctedwordtouse
                        else:
                            if word == "***":
                                # this is usually some form of punctuation but sometimes it's nothing
                                nextwordsearch = ur"\s*(?P<punct>[^\w\s])?(?P=punct)?(?P=punct)?"
                                nextorigwordsearch = ur"\s*(?P<punct>[^\w\s])?(?P=punct)?(?P=punct)?"
                                # a punct or the same punct  2 or 3 times or a space (re. #5)
                            else:
                                nextwordsearch = wordtouse  # as a punct mark can be forgotten,
                                #  already included in search, see below


                        found_next_word = re.match(ur"^[\W\s]*(" + nextwordsearch + ur")", reducedcorrected, flags=re.UNICODE)
                        found_next_origword = re.match(ur"^[\W\s]*(" + nextorigwordsearch + ur")", reducedoriginal, flags=re.UNICODE)
                        if word == "***":
                            # we don't want the punct stuff at the start:
                            found_next_word = re.match(ur"^\s*(" + nextwordsearch + ur")", reducedcorrected, flags=re.UNICODE)
                            found_next_origword = re.match(ur"^\s*(" + nextorigwordsearch + ur")", reducedoriginal, flags=re.UNICODE)


                        #print word, correctedWord
                        #print "searching", nextwordsearch, "|", reducedcorrected[:min(30, len(reducedcorrected))]
                        #print "searchingorig", nextorigwordsearch,"|", reducedoriginal[:min(30, len(reducedoriginal))]
                        if not found_next_word:
                            print "PROBLEM", word, correctedWord, reducedcorrected[:min(30, len(reducedcorrected))]
                            #exit(2)
                            #print reducedcorrected
                        else:
                            if word == "***":
                                reducedcorrected = re.sub(ur"^\s*(" + nextwordsearch + ur")", "", reducedcorrected, flags=re.UNICODE)

                            else:
                                reducedcorrected = re.sub(ur"^[\W\s]*(" + nextwordsearch + ur")", "", reducedcorrected, flags=re.UNICODE)

                        if not found_next_origword:
                            print "ORIG PROBLEM", word, correctedWord, reducedoriginal[:min(30, len(reducedoriginal))]
                            #exit(1)

                            #print reducedoriginal
                        else:
                            if word == "***":
                                reducedoriginal = re.sub(ur"^\s*(" + nextorigwordsearch + ur")", "", reducedoriginal, flags=re.UNICODE)
                            else:
                                reducedoriginal = re.sub(ur"^[\W\s]*(" + nextorigwordsearch + ur")", "", reducedoriginal, flags=re.UNICODE)


                #print
                #print origtextmainpage
                #print correctedtextmainpage
                #print type(origtextmainpage)
                #print type(correctedtextmainpage)
                print "-------------------------------------------"


                corpus.append(Entry(entryNumber, origtextmainpage, correctedtextmainpage, worderrors))

            rowcount += 1
            # if rowcount > 300: break
    return corpus


# base file name will have _ + entry number + .txt added to it
# and ".json" for the whole corpus
def save_corpus(corpus, baseFilename, correctedBaseFileName, outjsonfilename):
    # save one text file per entry and a .json for the whole
    for entry in corpus:
        outtextfilename = baseFilename + "_" + str(entry.entrynumber) + ".txt"
        with codecs.open(outtextfilename, mode='wb', encoding='utf8') as outtextfile:
            outtextfile.write(entry.origtext)
        correctedouttextfilename = correctedBaseFileName + "_" + str(entry.entrynumber) + ".txt"
        with codecs.open(correctedouttextfilename, mode='wb', encoding='utf8') as correctedouttextfile:
            correctedouttextfile.write(entry.correctedtext)

    # outjsonfilename = baseFilename + ".json"
    jsoncorpus = [(entry.entrynumber, entry.origtext, entry.correctedtext, entry.worderrorlist) for entry in corpus]
    with codecs.open(outjsonfilename, mode='w', encoding='utf8') as outjsonfile:
        json.dump(jsoncorpus, outjsonfile)


corpushtmlfile = "/home/nparslow/Documents/AutoCorrige/SpellChecker/errorsCorpusCorrected.html"

corpus = readCorpus(corpushtmlfile)
outjsonfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellCheckerJson/entry.json"

origout = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellChecker/entry"
corrout = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellCheckerCorrected/entrycorrected"
save_corpus(corpus, origout, corrout, outjsonfilename)
