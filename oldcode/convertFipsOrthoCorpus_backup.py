# coding=utf-8
import re
#import urllib2

__author__ = 'nparslow'

from bs4 import BeautifulSoup
import codecs
import json


class Entry:
    def __init__(self, entrynumber, origtext, correctedtext, worderrorlist):
        self.entrynumber = entrynumber
        self.origtext = origtext
        self.correctedtext = correctedtext
        self.worderrorlist = worderrorlist


def readCorpus(corpushtmlfile):
    corpus = []
    with codecs.open(corpushtmlfile, mode='r', encoding='latin1') as htmlcorpus:
        soup = BeautifulSoup(htmlcorpus)

        table = soup.find('table')

        rowcount = 0
        for row in table.findAll('tr'):
            print "analysing", row
            cols = row.findAll('td')
            if len(cols) > 0:
                entryNumber = int(cols[0].text.strip())  # note some entry numbers do not exist
                if entryNumber < 372: continue
                # the view corpus all together option has some only partial original texts so we don't use those
                # and sometimes the corrected sentence includes
                #  both the original words and their replacements (e.g. no. 225)

                # if cols[1].findAll('td'):
                origTextMainPage = cols[1].text.strip()
                correctedtextmainpage = cols[3].text.strip()

                # normalisations to make life easier:
                origTextMainPage = re.sub(ur'\s+', u' ', origTextMainPage, flags=re.UNICODE)
                origTextMainPage = re.sub(ur' !', u'!', origTextMainPage, flags=re.UNICODE)
                origTextMainPage = re.sub(ur' \?', u'?', origTextMainPage, flags=re.UNICODE)
                origTextMainPage = re.sub(ur' ,', u',', origTextMainPage, flags=re.UNICODE)
                origTextMainPage = re.sub(ur' ;', u';', origTextMainPage, flags=re.UNICODE)

                if entryNumber == 15:
                    correctedtextmainpage = re.sub(ur' en ', u' de la ', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'le Terre-Neuve', u'Terre-Neuve', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 29:
                    correctedtextmainpage = re.sub(ur'des problèmes', u'de problèmes', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 31:
                    # origTextMainPage = re.sub(ur' France', u'France', origTextMainPage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'la France', u'France', correctedtextmainpage, flags=re.UNICODE)
                # elif entryNumber == 38:
                #    origTextMainPage = re.sub(ur'\s+La curé', u' La curé', origTextMainPage, flags=re.UNICODE)
                # elif entryNumber == 40:
                #    origTextMainPage = re.sub(ur'\s+par', u' par', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 43:
                    correctedtextmainpage = re.sub(ur'content,', u'content;', correctedtextmainpage,
                                                   flags=re.UNICODE)  # I could be wrong here
                elif entryNumber == 48:
                    correctedtextmainpage = re.sub(ur'là', u'-là', correctedtextmainpage, flags=re.UNICODE)
                    # origTextMainPage = re.sub(ur'\)\?', u') ?', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 49:
                    correctedtextmainpage = re.sub(ur'faim', u'faim,', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 53:
                    origTextMainPage = re.sub(ur'peintures,', u'peintures', origTextMainPage,
                                              flags=re.UNICODE)  # an error was highlighted, so I assume it was there
                elif entryNumber == 61:
                    origTextMainPage = re.sub(ur':«', u':« ', origTextMainPage, flags=re.UNICODE)
                    origTextMainPage = re.sub(ur'\.\.\. »', u'...»', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 65:
                    correctedtextmainpage = re.sub(ur'rois inca', u'rois incas', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 69:
                    origTextMainPage = re.sub(ur'...Une', u'... Une', origTextMainPage, flags=re.UNICODE)
                    origTextMainPage = re.sub(ur'» \(', u'»(', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 70 or entryNumber == 84:
                    origTextMainPage = re.sub(ur'\? »', u'?»', origTextMainPage, flags=re.UNICODE)
                    pass
                elif entryNumber == 71:
                    origTextMainPage = re.sub(ur'...alors', u'... alors', origTextMainPage, flags=re.UNICODE)
                    origTextMainPage = re.sub(ur'»Prépondérant', u'» Prépondérant', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 74 or entryNumber == 75:
                    origTextMainPage = re.sub(ur' , ', u', ', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 81:
                    correctedtextmainpage = re.sub(ur'épisode\(«Les', u'épisode ( « Les', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    origTextMainPage = re.sub(ur'» \)', u'»)', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 82:
                    origTextMainPage = re.sub(ur'président...', u'président ...', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 92:
                    origTextMainPage = re.sub(ur'autre "\.', u'autre".', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 93:
                    origTextMainPage = re.sub(ur':«Un', u':« Un', origTextMainPage, flags=re.UNICODE)
                    origTextMainPage = re.sub(ur'\.\.\. »', u'...»', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 94:
                    origTextMainPage = re.sub(ur'» :', u'»:', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 96:
                    origTextMainPage = re.sub(ur'\. \( = C', u'.( = C', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 107 or entryNumber == 119:
                    origTextMainPage = re.sub(ur' \!', u'!', origTextMainPage, flags=re.UNICODE)
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
                    origTextMainPage = re.sub(ur'\' ', u'\'', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 114:
                    correctedtextmainpage = re.sub(ur' ne ', u' ', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 116:
                    origTextMainPage = re.sub(ur',Comment', u', Comment', origTextMainPage, flags=re.UNICODE)
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
                    origTextMainPage = re.sub(ur'\.\.\.A', u'... A', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 140:
                    correctedtextmainpage = re.sub(ur'va\-tu', u'vas-tu', correctedtextmainpage, flags=re.UNICODE)
                    origTextMainPage = re.sub(ur' \?', u'?', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 160:
                    correctedtextmainpage = re.sub(ur'en la ville', u'en ville', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 162:
                    correctedtextmainpage = re.sub(ur'à tous', u'dans tous', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'\- ', u'', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 177:
                    origTextMainPage = re.sub(ur'e\.\.\.', u'e ...', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 179:
                    correctedtextmainpage = re.sub(ur'Mountain', u'Mountains', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 184:
                    correctedtextmainpage = re.sub(ur'es arrives', u'arrives', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 187:
                    correctedtextmainpage = re.sub(ur'excitée', u'enthousiaste', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 189:
                    correctedtextmainpage = re.sub(ur'mois prochains', u'prochains mois', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 195:
                    origTextMainPage = re.sub(ur'Donc,', u'Donc', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 200:
                    origTextMainPage = re.sub(ur'»,', u'» ,', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 202:
                    correctedtextmainpage = re.sub(ur'modestes', u'modeste', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 203 or entryNumber == 204:
                    origTextMainPage = re.sub(ur'\. »', u'.»', origTextMainPage, flags=re.UNICODE)
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
                elif entryNumber == 223:
                    correctedtextmainpage = re.sub(ur'baisse', u'une baisse', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 225:
                    correctedtextmainpage = re.sub(ur'hier', u'', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'Le cadre a', u'Le cadre', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 226:
                    correctedtextmainpage = re.sub(ur'au une au miel sauce', u'au miel', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'poulet en', u'poulet à la', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 227:
                    correctedtextmainpage = re.sub(ur'mourir pour', u'mourir', correctedtextmainpage, flags=re.UNICODE)
                    origTextMainPage = re.sub(ur'»,', u' »,', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 240:
                    origTextMainPage = re.sub(ur'fruits,pain', u'fruits, pain', origTextMainPage, flags=re.UNICODE)
                elif entryNumber == 242:
                    correctedtextmainpage = re.sub(ur'yaatties', u'yatties', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 243:
                    correctedtextmainpage = re.sub(ur'La Bamba restaurant', u'Le restaurant La Bamba',
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 245:
                    correctedtextmainpage = re.sub(ur'bar petit', u'petit bar', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'assiette est', u'plat', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 255:
                    correctedtextmainpage = re.sub(ur'intime ambiance', u'ambiance intime', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 261:
                    correctedtextmainpage = re.sub(ur'Soverign', u'Sovereign', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 287:
                    correctedtextmainpage = re.sub(ur'porteur', u'porteurs', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 293:
                    correctedtextmainpage = re.sub(ur'leur chansons', u'leurs chansons', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 296:
                    correctedtextmainpage = re.sub(ur'le koulak', u'les koulaks', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 332:
                    correctedtextmainpage = re.sub(ur'ai mange la', u'ai mangé une', correctedtextmainpage,
                                                   flags=re.UNICODE)

                # start of missing info:
                elif entryNumber == 335:
                    origTextMainPage += u"a trop grand!"
                elif entryNumber == 336:
                    origTextMainPage += u"hommes. C'est une petite guerre civile entre le Gouvernement et" \
                                        u" la\" Guerilla\"." \
                                        u" Une Guérilla qui est née come conséquence des mouvements socialistes" \
                                        u" en Amérique" \
                                        u" du Sud au même temp que la Révolution Cubaine, mais qu'aujourd'hui n'a pas" \
                                        u" des idéales ( Elle se finance avec le trafic de drogue)" \
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
                    correctedtextmainpage = re.sub(ur'se finance avec', u"est financé par", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'défendre de la Guérilla', u"défendre contre la Guérilla",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'qui ils n\'ont', u"qui n'ont", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'entre le conflit', u"au milieu du", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'arrivera, où', u"arrivera où", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'qu\'en Colombie', u"en Colombie", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"on pourras", u"on pourra", correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 337:
                    origTextMainPage += u" grandes conséquences pour les entreprises belges. Si elles veulent occuper" \
                                        u" leur position sur le marché interieure, elles doivent faire face à la" \
                                        u" concurrence élargissante de l'étranger. Mais réaliser cet objectif est" \
                                        u" impossible de notre entreprise parce que notre entreprise est une PME" \
                                        u" et elle ne peut pas concurrencez les grandes entreprises de l'étranger." \
                                        u" Notre entreprise a donc dû partir à la recherche de nouveaux marchés par" \
                                        u" exemple le marché de l'Europe occidental où notre entreprise pourrait" \
                                        u" être rentable. A fin de lancer notre produit sur ce marché, nous devons " \
                                        u"promouvoir notre produit dans cette région."
                    correctedtextmainpage = re.sub(ur"commençait", u"commençaient", correctedtextmainpage,
                                                   flags=re.UNICODE)
                                                    # example of a new mistake inserted in the correct version!
                elif entryNumber == 338:
                    origTextMainPage += u"eau, pour que nous pouvons augmenter notre chiffre d'affaires. Notre" \
                                        u" entreprise a donc dû partir à la recherche de nouveau marchés. En faisant" \
                                        u" des innovations de l'un part investir dans les unité de production et" \
                                        u" de l'autre part dans la recherche et developpement. Pour atteindre ce but" \
                                        u" nous devons utiliser la publicité et élargir" \
                                        u" notre siseaux de point de vente."
                    correctedtextmainpage = re.sub(ur"ciblé", u"ciblé:", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"donc répond", u"donc il répond", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'conséquent est-il', u'conséquent il est', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'à des nouveaux cerveaux', u'a de nouveaux cerveaux',
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'd\'une l\'un', u'd\'une', correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'd\' l\'autre part', u'd\'autre part', correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'point de vente', u'points de vente', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 339:
                    origTextMainPage += u" dû partir à la recherche de nouveaux marchés. C'est pourquoi nous avons" \
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
                    origTextMainPage += u"as en Belgique un créneaux. Mais les entreprises qu veulent rester ouvert," \
                                        u" doit être compétitif. Les conditions pour être competitif sont la" \
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
                    correctedtextmainpage = re.sub(ur'rester ouvert doit être compétitif',
                                                   u'rester ouvertes doivent être compétitives', correctedtextmainpage,
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
                    origTextMainPage += u" répondre à la demande d'un public déterminé. Ensuite pour le lancer sur le" \
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
                    origTextMainPage += u"se, OCOB, avait trouvé de nouveaux débouchés, grâce à l'investissement et" \
                                        u" en faisant beaucoup d'études de marché par des sondages et des ." \
                                        u" Notre entreprise a donc dû partir à la recherche de nouveaux marchés," \
                                        u" parce que si on ne le faisait pas, ou resterait beaucoup derrière et la" \
                                        u" chance de faire faillite serait trop grand. En recherchant de nouveaux" \
                                        u" marchés, notre entreprise a vu ce qu'on devait faire. Nos yeux étaient" \
                                        u" ouverts et nous étions sur que dans quelque temps, nous nous trouverons" \
                                        u" de même sur le même niveau de OCOB."
                    correctedtextmainpage = re.sub(ur'desordinateurs', u'des ordinateurs', correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 343:
                    origTextMainPage += u" avait des autres firmes sur le marché et qui voulaient faire concurrence à" \
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
                elif entryNumber == 344:
                    origTextMainPage += u"té pendant 5 ans. En dépit que les chiffres d'affaires baissaient, Belga" \
                                        u" restait le plus grand. VDB: \" Nous avions quelques problèmes avec la" \
                                        u" vente, mais ces problèmes sont passés maintenant\". La crise avait à voir" \
                                        u" avec la saturation du marché. \" Notre entreprise a donc dû partir à" \
                                        u" la recherche de nouveaux marchés\" dit-il, et ils ont trouvé un: les" \
                                        u" jeunes. Eslabalement, leur clientèle existait des fumeurs agés. En" \
                                        u" developpant une nouvelle image de marque, les jeunes commençaient à" \
                                        u" fumer le Belga. Ainsi nous avons gagné une très grande part du" \
                                        u" marché. \" Maintenant je suis un homme heureux\" étaient ses mots finals."
                    correctedtextmainpage = re.sub(ur"président du Belga", u"président de Belga", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"ils ont trouvé", u"ils en ont troué", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Eslabalement", u"Auparavant", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"existait des", u"était constituée de", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"jeunes commençaient à", u"jeunes ont commencé à",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"le Belga", u"des Belga", correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 345:
                    origTextMainPage += u"on M. Declerck, on ne va plus pouvoir parler d'une peine sans coupable" \
                                        u" ou\" la négation de la presomption d'innocense. \" Au futur on aura" \
                                        u" besoin plus de preuves pour détenir quelqu'un. Certaines députés" \
                                        u" disent que ce projet de loi à comme seule but de résoudre le problème" \
                                        u" des prisons. En plus, disent-ils, seront les nouveaux organes des" \
                                        u" instruments du Ministère. Néanmoins, la Chambre a adopté le projet" \
                                        u" majorité contre minorité. Néanmoins quelques député de la majorité"
                    correctedtextmainpage = re.sub(ur"les idées des juristes éminents",
                                                   u"l'avis de jusristes éminents", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"le Ministère de Justice", u"Ministère de la Justice",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"a construit", u"a élaboré", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"va des", u"va créer des", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Au futur", u"Dans le futur", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"seule but", u"seul but", correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 346:
                    origTextMainPage += u"a donc les doses imorteles vont réduire. Quelques députés de la majorité" \
                                        u" ont toutefois voté cotre ce projet de loi. Ce vote de méfiance"
                    correctedtextmainpage = re.sub(ur"état contrôle", u"État contrôle", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"d'opinion que", u"d'avis que", correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 347:
                    origTextMainPage += u"a majorité du chambre à voter pour le projet de loi mais quelques " \
                                        u"députés de la majorité ont voté contre ce projet de loi. La Chambre donne" \
                                        u" ce projet de loi à la sénat qui indiqué 15 sénateurs pour une recherche" \
                                        u" ou commission"
                    correctedtextmainpage = re.sub(ur"une recherche", u"un examen", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"La Chambre donne", u"La Chambre a transmis",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"au la", u"à la", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"indiqué", u"a désigné", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"une recherche ou", u"un examen en", correctedtextmainpage,
                                                   flags=re.UNICODE)
                elif entryNumber == 348:
                    origTextMainPage += u"nt d'accord, monsieur Maystadt sera très content. Le projet de loi du" \
                                        u" ministre de Finances s'exprime par une augmentation des impôts indirects," \
                                        u" c'est-à-dire une croissance de TVA. Ainsi, le ministre veut augmenter" \
                                        u" les recettes. Heureusement pour la population de la Belgique, quelques" \
                                        u" députés de la majorité ont voté contre ce projet de loi Et pas seulement" \
                                        u" des députés de la majorité, mais également ceux de la minorité. Alors le" \
                                        u" parlement a pu prevenir une nouvelle augmentation des impôts."

                    correctedtextmainpage = re.sub(ur"monsieur", u"Monsieur", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"pour ceci", u"pour qu'il", correctedtextmainpage,
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
                    origTextMainPage += u"i La Haute Assemblée, à savoir le Sénat, a seulement une fonction de" \
                                        u" réffection. L'abolition de la peine de mort était le sujet d'un projet" \
                                        u" de loi, mais les partis politiques avaient des opinions différentes" \
                                        u" sur ce sujet. Quelques députés de la majorité ont toutefois vote" \
                                        u" contre ce projet de loi. Ces députés avaient l'opinion de garder" \
                                        u" la peine de mort pour des cas de guerre( par exemple: désertion) " \
                                        u"et des cas très sévères. Non seulement l'opposition voulait l'abolir" \
                                        u" parce que la peine de mort est trop cruelle et immense. Mais la peine" \
                                        u" de mort est probablement aussi un mort plus douce que le mort des victimes."
                elif entryNumber == 350:
                    origTextMainPage += u"a soumis à la commission Après le projet a fait plusieurs fois la navette" \
                                        u" entre la chambre des représentant et le sénat. Chaque chambre peut amender" \
                                        u" des partie du projet. Ainsi les partie amender sont corriger par" \
                                        u" l'autre chambre. La décision finale se trouve chez la chambre des" \
                                        u" représentant ( ceci depuis la dernière réforme) . Hier quelques députés" \
                                        u" de la majorité ont voté contre ce projet de loi, ce qui signifie que" \
                                        u" le projet ne continue pas son chemin, et ne sera donc jamais soumis" \
                                        u" à la sanction du Roi, et donc ni promulger ni publié dans le moniteur belge."
                    correctedtextmainpage = re.sub(ur"la chambre", u"la Chambre", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"le sénat", u"le Sénat", correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 351:
                    origTextMainPage += u"ouvernement a pris quelques messures c'est-à-dire, a la fin de l'année" \
                                        u" passée le gouvernement a proposé une nouvelle loi: augmenter" \
                                        u" les impôts sur cigarettes, augmenter des coûts pour un " \
                                        u"rendez-vous au médecin. Mais cette proposition a connu des obstacles." \
                                        u" ded plusieurs partis. Quelques députés de la majorité ont" \
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
                elif entryNumber == 352:
                    origTextMainPage += u"onde politique a même peur pour une situation comme le projet de loi" \
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
                    correctedtextmainpage = re.sub(ur"ferme disant la", u"s'oppose en force",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"avaient beaucoup", u"auront beaucoup",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"serait typiquement", u"soit typiquement",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 353:
                    origTextMainPage += u"t d'exclure les partis d'extrème-droite, les membres du Front National" \
                                        u" quittaient l'Assemblée fou de rage disantes qu'ils n'avaient rien à faire" \
                                        u" avec les incidents de la semaine passée. Enfin le scrutin pouvait avoir" \
                                        u" lieu après que la séance avait été interrompu de cette façon, pensant" \
                                        u" à des situations japonaises. Le projet voté d'une manière renforcé" \
                                        u" et spéciale était accepté par la Chambre malgré que quelques députés" \
                                        u" de la majorité ont toutefois voté contre ce projet de loi. Ils disaient" \
                                        u" après dans leur explication du vote: \" qu'il faut tollére la voix de" \
                                        u" chacun et chacune dans une démocratie moderne\". Probablement eux" \
                                        u" n'ont pas encore sentis la poignée."
                    correctedtextmainpage = re.sub(ur"la rue de la Loi succède l'", u"le parcours de la loi rencontre ",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    origTextMainPage = re.sub(ur"en otage", u"en hautage", origTextMainPage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"uneambiance", u"une ambiance",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 354:
                    origTextMainPage += u"es de capital et attribuer par conséquence à la suppression de la dette" \
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
                elif entryNumber == 355:
                    origTextMainPage += u"oté contre. Ministre Peers était surpris car ceci est plusieurs" \
                                        u" exceptionnelle. En outre, le parlement a utilisé son pouvoir pour faire" \
                                        u" chuter le gouvernement Elle doit donc indiquer un nouveau Premier ministre" \
                                        u" et ceci pendant les trois jours. La décision a causé beaucoup de réactions" \
                                        u" mais le parlement a fait une choix qui le semble la meilleure."
                    correctedtextmainpage = re.sub(ur"chuter le gouvernement", u"chuter le gouvernement.",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Elle doit", u"Il doit",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 356:
                    origTextMainPage += u" transmis le texte au Sénat. Mais le sénat a amendé le texte de sorte" \
                                        u" qu'il soit revenu à la Chambre. La Chambre a la décision finale et" \
                                        u" il doit voter le texte. L'opinion publique supposait que ce projet" \
                                        u" soit accepté, quelque députés de la majorité ont toutefois voter" \
                                        u" contre ce projet de loi de sorte que le texte soit rejeté. Les députés" \
                                        u" ont modivé leur décision et ils ont dit qu'ils pensent qu'une" \
                                        u" legalisation des drogues augmentera la criminalité et incitera les" \
                                        u" jeunes à utiliser des drogues."
                    correctedtextmainpage = re.sub(ur"soit revenu", u"est revenu",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"soit rejeté", u"a été",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 357:
                    origTextMainPage += u" beaucoup de confiance avec ma capacité de parler français. En réalité," \
                                        u" je parle français comme une vache espagnole!" \
                                        u" Je sais qu'un séjour en France" \
                                        u" ou dans un pays où les gens parlent français serait un avantage." \
                                        u" Je voudrais participer au cours de langue français en France ou l'ideal" \
                                        u" serait aller au Québec. Je voudrais aussi voir la civilisation" \
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
                    origTextMainPage += u"ays. J'attends avec impatience de voyager à l'étranger, parce que je" \
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
                elif entryNumber == 359:
                    origTextMainPage += u"enir. Je crois que la meilleure façon en quelle je peux apprendre" \
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
                    correctedtextmainpage = re.sub(ur"est travailler", u"est de travailler",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"une au pair", u"une jeune fille au pair",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"et apprendre sur", u"et d'apprendre",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur" ne est", u" n'est", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"coûts de voyage", u"dépenses de voyage",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"et avec espoirs", u"et si possible",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"et les comparent\.", u"et les comparer.",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 361:
                    origTextMainPage += u"pe dans le Vatican, la fontaine de trevi et la chapelle de Michaelangelo," \
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
                elif entryNumber == 362:
                    origTextMainPage += u"i et aujourd'hui le groupe jouait un très grand concert à Manchester, la" \
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
                                        u" n'a vu que Liam buvait plus que les autres... . en fait il n'a pas" \
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
                    correctedtextmainpage = re.sub(ur"joue la guitare", u"jouer de la guitare",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 363:
                    origTextMainPage += u"oses qui se sont passées pendant mes vacances en Kenya. Surtout, Je me" \
                                        u" souviens du match de rugby contre l'école pas loin de la location de" \
                                        u" mon travail. Nous avons voyagé en bus à l'école, mais après environ" \
                                        u" une heure le bus s'est arrêté soudainement. Il y avait beaucoup de" \
                                        u" bruit, y compris des coups de feu. A ce moment là, trois hommes de" \
                                        u" pauvre apparence, armés j'jusq' aux dents sont embarqué dans le bus." \
                                        u" Ils ont ordonné que tout le monde descendre. Nous avons été ligotés," \
                                        u" et ils nous ont renversé sur la terre. C'était une situation" \
                                        u" inquiétante! Nous avions la terreur d'être assassiné! Bientôt," \
                                        u" les eleves étaient libérés, mais nous nous restions où nous étions." \
                                        u" Ils nous ont mis en camionette, et ils ont conduit, je ne sais où," \
                                        u" quelque part. La nuit tombait. Il faissait froid et nous avions faim." \
                                        u" Après plusieurs heures de bavardage en Swahili, nous les avons persuadé" \
                                        u" que nous étions bénévoles et que nous n'avions pas d'argent. Jusqu'à" \
                                        u" une heure avancée de la nuit nous étions déposé au faubourg d'Eldoret." \
                                        u" Nous sommes resté plus long-temps dans le commissariat de police que" \
                                        u" les bandits! Inutile de dire qu'ils n'ont jamais étaient capturé, et nous" \
                                        u" ne sommes joué pas au rugby ce jour!"
                    origTextMainPage = re.sub(ur"Kapsabet\' \.", u"Kapsabet\'.", origTextMainPage, flags=re.UNICODE)
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
                    correctedtextmainpage = re.sub(ur"où quelque part", u"où", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"ne avons", u"n'avons", correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"rugby ce jour", u"rugby ce jour-là",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 364:
                    origTextMainPage += u"us sommes catholiques. Le deux jour suivant, il y a des danceurs qui" \
                                        u" dancent pour las rues avec des groups de musiciens pendant la" \
                                        u" journée. Tout les groupes des danceurs sont organizees de façon qui" \
                                        u" ils peuvent dancer sans problèmes. Cette célébration a trois raisons:" \
                                        u" la fête de la ville, la fête d'une virgen et la fête du roi du minas." \
                                        u" Tout les gens parcitipent et pendant cet jours. la ville être vit et" \
                                        u" ou peut voir des gens qui jamais on a vu et tous sont heureux d'être" \
                                        u" de la ville et de participier de la fête."
                    correctedtextmainpage = re.sub(ur"la fête de la ville est", u"La fête de la ville est",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"\. de façon qui", u" de façon qu'",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"être vit", u"vit", correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 365:
                    origTextMainPage += u" ils crient, ils rient en jettant les oranges."
                elif entryNumber == 366:
                    origTextMainPage += u"ille pendant des fêtes dans des petits villes an Italie. Une fanfare" \
                                        u" la jouait. Tout le monde tape des mains avec le rythme."
                    correctedtextmainpage = re.sub(ur"tapent les mains avec le rythme", u"tape des mains en rythme",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 367:
                    origTextMainPage += u" oublier leure impatience et leures inquiétudes. Les armes brillent dans" \
                                        u" le soleil levant, les uniformes ofrent une mélange des couleurs" \
                                        u" inimaginable. Et malgré tout, dans quelques heures seulement, les" \
                                        u" mêmes armes seront cassés, les mêmes uniformes pleines de poussière" \
                                        u" et de sang."
                    correctedtextmainpage = re.sub(ur"les faire oublier", u"oublier",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"inimaginable", u"inimaginables",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 368:
                    origTextMainPage += u"onsommateurs et patrons. D'abord, il y a des arguments économiques" \
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
                    correctedtextmainpage = re.sub(ur"la demande de la déréglementation", u"demande de déréglemenation",
                                                   correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"et patrons", u"et les patrons", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"salariés, ils", u"salariés", correctedtextmainpage,
                                                   flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"termine où a liberté", u"terminer là où la liberté",
                                                   correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 369:
                    origTextMainPage += " serieux. Dans les jours d'après tous les ètudiants portait la radio" \
                                        " avec eux pour écouter les dernières nouvelles. Tout le monde parlait" \
                                        " de la 3ème guerre mondial, comme maintenant à Kosovo. Les gens avaient" \
                                        " peur des bombes nucleaires et biologiques. Les disputes pour ou contre" \
                                        " l'OTAN etaient toujour les mêmes. Moi aussi j'ai commencé à donner mon" \
                                        " opinion: ça va ou ne va pas arriver, etc.. sans savoir vraimente la" \
                                        " verité C'est pour ça que maintenant je ne crois pas tout que les" \
                                        " journals dissent. avec Kosovo. J'ai été choqué, bien sur, mais" \
                                        " la panique et e peur pour la 3e eme guerre Mondiale ou la guerre" \
                                        " atomique a disparu. Ca ne veut pas de tout dire que on se sent pas" \
                                        " triste et solidaire avec les gens qui suffrent en place."
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
                elif entryNumber == 370:
                    origTextMainPage += u", comment ils s'appellent et surtout savoir si mon frère avait été" \
                                        u" blessé pour l'impact de la bombe. Tout d'abord j'ai changé le channel" \
                                        u" de la radio pour vérifier la nouvel. Après je parlait à mes parents" \
                                        u" sur les faits et je leur expliquais qu'il avait" \
                                        u" malheureusement un mort, c'était un militaire. La nouvel avait" \
                                        u" été très discuté et toute la ville ne parlait que des assassins" \
                                        u" d'ETA. C'est difficile à croire comment ils peuvent demander" \
                                        u" un droit, le droit d'être independantes de l'Espagne, en attentant" \
                                        u" contre des autres droits humains et se faisant prévaloir d'un systéme" \
                                        u" democratique. Je crois qu'il y a plusieurs manières de demander" \
                                        u" les choses mais ce qu'il n'est pas acceptable c'est le fait de" \
                                        u" tuer des personnes pour ideologies."
                    correctedtextmainpage = re.sub(ur"jea l'ai", u"je l'ai",
                               correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"Je l'avait appris", u"Je l'avais appris",
                               correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur"au sujet des les", u"au sujet des",
                               correctedtextmainpage, flags=re.UNICODE)
                    correctedtextmainpage = re.sub(ur'ce quiil', u'ce qui', correctedtextmainpage, flags=re.UNICODE)
                elif entryNumber == 371:
                    origTextMainPage += u" volonté de crier au monde notre desapprovetion devait dévénir réelle et" \
                                        u" éfficace. Le matin suivent beaucoup d'étudiants avaient eu la même" \
                                        u" idée et un cortège spontané allait se former dans la ville pour" \
                                        u" manifester notre indignation. On ne pouvait pas tues les étudiants" \
                                        u" universitaires qui se croiait la vrai expression de la culture," \
                                        u" comme des petites bêtes sans valeur."
                    correctedtextmainpage = re.sub(ur"ami dans un", u"ami un", correctedtextmainpage, flags=re.UNICODE)
                # back to nomral:
                elif entryNumber == 372:
                    correctedtextmainpage = re.sub(ur"ceci", u"Ceci", correctedtextmainpage, flags=re.UNICODE)

                print "orig:", origTextMainPage
                print "corrected:", correctedtextmainpage
                reducedcorrected = correctedtextmainpage

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

                        print "error:", word, cat, errors, correctedWord

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
                                word = "soldats,"
                                # correctedWord = "soldats,"
                            if wordlabel == "i00022":
                                word = "roi,"
                                # correctedWord = "roi,"
                                # probably shouldn't be with comma, but it's acceptable for emphasis on the last element
                        elif entryNumber == 16:
                            if wordlabel == "i00014": word = "Ouest,"
                            if wordlabel == "i00017": word = "fourrures,"
                            if wordlabel == "i00007": word = "multiples;"
                            if wordlabel == "i00020": word = u"Amérindiens,"
                        elif entryNumber == 18:
                            if wordlabel == "i00010":
                                word = "anglais,"
                                correctedWord = "anglaise,"
                            if wordlabel == "i00011": word = "hollandais,"
                        elif entryNumber == 27:
                            if wordlabel == "i00004": word = u"métier,"
                            if wordlabel == "i00006": word = u"religieux,"
                            if wordlabel == "i00008": word = u"soldats,"
                            if wordlabel == "i00012": word = u"roi,"
                        elif entryNumber == 29:
                            if wordlabel == "i00006":
                                word = "problemes,"
                                correctedWord = u"problèmes,"
                            if wordlabel == "i00009": word = "maladies,"
                            if wordlabel == "i00012": word = "corsaires,"
                        elif entryNumber == 39:
                            if wordlabel == "i00003": word = u"cérémonie,"
                        elif entryNumber == 41:
                            if wordlabel == "i00022": word = u"cérémonie,"
                        elif entryNumber == 43:
                            if wordlabel == "i00022":
                                word = u"content,"
                                correctedWord = u"content;"  # or perhaps should be . ????? (no correction given)
                        elif entryNumber == 45:
                            if wordlabel == "i00013": word = "parents,"
                        elif entryNumber == 55:
                            if wordlabel == "i00015": word = "heures,"
                            if wordlabel == "i00018": word = "soirs."
                        elif entryNumber == 60:
                            if wordlabel == "i00030": word = "'Europe"
                        elif entryNumber == 83:
                            if wordlabel == "i00024": correctedWord = "veut"
                            if wordlabel == "i00025": correctedWord = "ainsi"  # word order swap
                            if wordlabel == "i00026": word = "-elle"
                        elif entryNumber == 106:
                            if wordlabel == "i00014": word = "'s"
                        elif entryNumber == 111:
                            if wordlabel == "i00004": word = "Mai,"
                        elif entryNumber == 117:
                            if wordlabel == "i00004": word = "-ils"
                        elif entryNumber == 121:
                            if wordlabel == "i00008": word = "-vous"
                        elif entryNumber == 126:
                            if wordlabel == "i00016": correctedWord = None
                            if wordlabel == "i00010": correctedWord = "le"
                            if wordlabel == "i00012": correctedWord = u"préféré"
                        elif entryNumber == 127:
                            if wordlabel == "i00004": correctedWord = "vous"
                        elif entryNumber == 128:
                            if wordlabel == "i00002": word = "-vous"
                        elif entryNumber == 133:
                            if word == "J'": correctedWord = "Je"
                            if word == "ai": correctedWord = "-"
                            if wordlabel == "i00027": correctedWord = u"me réjouis"
                        elif entryNumber == 138:
                            if wordlabel == "i00019": word = u"Asie,"
                        elif entryNumber == 139:
                            if wordlabel == "i00006": word = "Alors..."  # no *** for the ... :/
                        elif entryNumber == 140:
                            if wordlabel == "i00010": word = "-tu"
                            if wordlabel == "i00016": word = "-ils"
                        elif entryNumber == 143:
                            if wordlabel == "i00023": word = "-toi"
                        elif entryNumber == 157:
                            if wordlabel == "i00020": word = "-tu?"
                            if wordlabel == "i00015": word = "souvenis,"
                        elif entryNumber == 163:
                            if wordlabel == "i00001": word = "Puis,"
                        elif entryNumber == 171:
                            if wordlabel == "i00004": word = "pas,"
                        elif entryNumber == 176:
                            if wordlabel == "i00020": correctedWord = "bons"
                            if wordlabel == "i00021": correctedWord = "petits"
                        elif entryNumber == 179:  # no *** for "
                            if wordlabel == "i00008":
                                word = '"Blue'
                                correctedWord = '"Blue'
                            if wordlabel == "i00009":
                                word = 'Mountain"'
                                correctedWord = 'Mountains"'
                        elif entryNumber == 185:
                            if wordlabel == "i00005":
                                word = "-tu"
                                correctedWord = "-tu?"
                        elif entryNumber == 186:
                            if wordlabel == "i00027":
                                word = "-tu"
                        elif entryNumber == 187:
                            if wordlabel == 'i00007':
                                word = u"excitée,"
                        elif entryNumber == 189:
                            if wordlabel == "i00014":
                                correctedWord = "prochains"
                            if wordlabel == "i00015":
                                correctedWord = "mois"
                            if wordlabel == "i00004": correctedWord = None
                            if wordlabel == "i00005": correctedWord = None
                            if wordlabel == "i00006": correctedWord = u"-à"
                            if wordlabel == "i00007": correctedWord = u"-dire"
                        elif entryNumber == 191:
                            if wordlabel == "i00002": word = "-moi"
                            if wordlabel == "i00014": word = "voyage,"
                            if wordlabel == "i00015": correctedWord = "Et"
                        elif entryNumber == 195:
                            # if word == "Je": correctedWord = "-"
                            #  keep Je as it is the same in both orig and corr versions
                            if word == "suis": correctedWord = "-"
                            if word == u"très": correctedWord = "-"
                            if word == u"exalté": correctedWord = u"me réjouis"
                        elif entryNumber == 208:
                            if word == "ma": correctedWord = "mon"
                        elif entryNumber == 213:
                            if wordlabel == "i00012": correctedWord = "chef"
                            # TODO this was 'uncorrectable', _UNKNOWN???
                        elif entryNumber == 214:
                            if wordlabel == "i00014": correctedWord = u"À"
                            # A is ok, but to be consistent with the other form

                        elif entryNumber == 226:
                            if word == "avec" and wordlabel == "i00015": correctedWord = "-"
                            if word == "un" and wordlabel == "i00016": correctedWord = "-"
                            if word == "sauce" and wordlabel == "i00018": correctedWord = "-"
                            # print "corr word", correctedWord
                        elif entryNumber == 240:
                            if wordlabel == "i00032": word = "[much"
                            if wordlabel == "i00033": word = "more]"
                        elif entryNumber == 247:
                            if wordlabel == "i00014": word = "C,"
                        elif entryNumber == 271:
                            if wordlabel == "i00005": word = "rapide,"
                        elif entryNumber == 275:
                            if wordlabel == "i00018": word = "rapidement,"
                        elif entryNumber == 336:
                            if wordlabel == "i00060": correctedWord = u"Guérilla"
                        elif entryNumber == 337:
                            if wordlabel == "i00122": correctedWord = "Afin"
                        elif entryNumber == 338:
                            if wordlabel == "i00039":
                                correctedWord = "a"
                                errors = ["DIA"]
                        elif entryNumber == 347:
                            if wordlabel == "i00017":
                                correctedWord = "un"  # not a mistake but needed for the change in noun
                            if wordlabel == "i00075": correctedWord = "un"  # ditto
                        elif entryNumber == 349:
                            if wordlabel == "i00027": correctedWord = "suspendu"
                            # this is same as original word but doesn't
                            #  fit the context, not obvious what to replace it with
                            # but the same is better than ? as in the corpus
                        elif entryNumber == 353:
                            if wordlabel == "i00094": correctedWord = None # corrected by spellchecker incorrectly
                        elif entryNumber == 358:
                            if wordlabel == "i00055": correctedWord = "ne" # correct n',
                            #  but change in aux requires change here
                            if wordlabel == "i00079": correctedWord = "j'" # ditto
                        elif entryNumber == 359:
                            if wordlabel == "i00196": correctedWord = "n'" # ditto
                            if wordlabel == "i00255": correctedWord = "n'" # ditto
                        elif entryNumber == 363:
                            if wordlabel == "i00074": correctedWord = "du" # ditto
                            if wordlabel == "i00075": correctedWord = "-" # ditto
                            if wordlabel == "i00176": correctedWord = "camionnette" # same typo in corrected form lol
                            if wordlabel == "i00259": correctedWord = "n'" # ditto style
                        elif entryNumber == 364:
                            if wordlabel == "i00001": correctedWord = "La"
                            if wordlabel == "i00014": correctedWord = "mois" # mix up mois and jours
                        elif entryNumber == 368:
                            if wordlabel == "i00177":
                                correctedWord = "terminer" # missed correction
                                errors = ["TPS"] # TPS = tense
                        elif entryNumber == 369:
                            if wordlabel == "i00063": correctedWord = u"étudiants"
                            if wordlabel == "i00158": correctedWord = "-"
                        elif entryNumber == 373:
                            if wordlabel == "i00001": correctedWord = u"Le"

                        worderrors.append((word, errors, correctedWord))

                        # escape all regex special chars :
                        # escape is maybe too strong as it does everything \W (inc unicode chars :/)
                        wordtouse = re.escape(word)
                        correctedwordtouse = wordtouse

                        # re.sub(r'([\.\\\+\*\?\[\^\]\$\(\)\{\}\!\<\>\|\:\-])', r'\\\1', "example string.")
                        if correctedWord is not None:
                            correctedwordtouse = re.escape(correctedWord)

                            if correctedWord == "-":
                                # dash means 'should be dropped' but it isn't always dropped :/
                                nextwordsearch = ur""
                            else:
                                nextwordsearch = correctedwordtouse
                        else:
                            if word == "***":
                                # this is usually some form of punctuation but sometimes it's nothing
                                nextwordsearch = ur"\s*(?P<punct>[^\w\s])?(?P=punct)?(?P=punct)?"
                                # a punct or the same punct  2 or 3 times or a space (re. #5)
                            else:
                                nextwordsearch = wordtouse  # as a punct mark can be forgotten,
                                #  already included in search, see below

                        print "searching", nextwordsearch, word, wordtouse
                        print reducedcorrected
                        found_next_word = re.match(ur"[\W\s]*(" + nextwordsearch + ur")", reducedcorrected, flags=re.UNICODE)

                        if not found_next_word:
                            print "PROBLEM"

                        
                        punct_replacement = ""
                        need_comma = False
                        if (not (lastword == "***" and word == "***")) and found_next_word is None:
                            print "Potential PROBLEM", correctedWord, nextwordsearch, reducedcorrected

                            # try to solve it by adding a comma if one in the orig text:
                            # splits = origTextMainPage.split(word)
                            # splits = re.split(wordtouse, origTextMainPage, flags=re.UNICODE )
                            # splits = correctedtextmainpage.split(word)
                            #splits = []
                            if correctedwordtouse is not None:
                                splits = re.split(correctedwordtouse, correctedtextmainpage, flags=re.UNICODE)
                            else:
                                splits = re.split(wordtouse, origTextMainPage, flags=re.UNICODE)
                            print "splits", splits
                            for cut in splits[:-1]:
                                # print cut, re.match(ur'\s*,', cut, flags=re.UNICODE)
                                if re.search(ur'\s*(?:[,\(\)«»=/:\'\"]\s*)+$', cut, flags=re.UNICODE):
                                    nextwordsearch = ur"((?:[,\(\)«»=/\:\'\"]\s*)+)\s*" + nextwordsearch
                                    # may have missed a comma from the last word
                                    print "second try:", nextwordsearch
                                    found_next_word = re.match(ur"\s*" + nextwordsearch, reducedcorrected,
                                                             flags=re.UNICODE)
                                    if found_next_word is None:
                                        print "DOUBLE PROBLEM"

                                        if re.search(ur'\s*(?:[\-]\s*)+$', cut, flags=re.UNICODE):
                                            nextwordsearch = ur"((?:[\-]\s*)+)\s*" + nextwordsearch
                                            # may have missed a comma from the last word
                                            print "third try:", nextwordsearch
                                            found_next_word = re.match(ur"\s*" + nextwordsearch, reducedcorrected,
                                                                     flags=re.UNICODE)
                                            if found_next_word is None:
                                                print "TRIPLE PROBLEM"

                                                # print correctedText
                                                # we may have a change in word order, so stocke
                                                # the last one and look for it again after:
                                                lastwordsearch = nextwordsearch
                                    else:
                                        print "NO PROB!"
                                        need_comma = True
                                        break  # need as can be splitting by 'le' and thus have many splits,
                                        # so it won't work perfectly
                        if found_next_word is not None:

                            print "groups:", found_next_word.groups()
                            punct_replacement = found_next_word.groups()[0]
                            # print "repl:", punct_replacement

                            if entryNumber == 334 and punct_replacement == u"-":
                                print punct_replacement, punct_replacement == u'-'
                                punct_replacement = ""  # as punct is corrected but also indicated with ***
                            else:

                                # reducedcorrected = re.sub( ur"^(\s*\W*\s*" + nextwordsearch + ur")", "",
                                #   reducedcorrected, flags=re.UNICODE | re.IGNORECASE)
                                reducedcorrected = re.sub(ur"^\s*(" + nextwordsearch + ur")", "", reducedcorrected,
                                                          flags=re.UNICODE)

                                if lastwordsearch:  # i.e. only search a second time if we have shortened the string
                                    # try to find it first:
                                    # print "old search repeated:", correctedWord, lastwordsearch, reducedcorrected
                                    # found_next_word = re.match( ur"(\s*\W*\s*" + lastwordsearch + ur")",
                                    #   reducedcorrected, flags=re.UNICODE | re.IGNORECASE)
                                    found_next_word = re.match(ur"\s*(" + lastwordsearch + ur")", reducedcorrected,
                                                             flags=re.UNICODE)
                                    if found_next_word:
                                        # reducedcorrected = re.sub( ur"^(\s*\W*\s*" + lastwordsearch + ur")", "",
                                        #   reducedcorrected, flags=re.UNICODE | re.IGNORECASE)
                                        reducedcorrected = re.sub(ur"^\s*(" + lastwordsearch + ur")", "",
                                                                  reducedcorrected, flags=re.UNICODE)
                                    else:
                                        print "double prob?"
                                        exit(1)
                                    lastwordsearch = None  # update i.e. we only search for a swap of one word
                        # print reducedcorrected + "|" + word + "|" + punct_replacement + "|"

                        if entryNumber == 69 or entryNumber == 71:
                            if punct_replacement == u"«":
                                punct_replacement = u"« ..."  # ad hoc for # 69
                                reducedcorrected = re.sub(ur"^\s*...", "", reducedcorrected, flags=re.UNICODE)

                        if word != "***":
                            if need_comma:  # could be comma or other form of missed punct

                                # somehow we get an extra space so remove it:
                                punct_replacement = re.sub(ur'\s+', ' ', punct_replacement, flags=re.UNICODE)
                                print "punct repl", punct_replacement + "|"
                                if len(origtext) > 0:
                                    if origtext[-1] != " " and not re.match(ur'[ ,]', punct_replacement,
                                                                            flags=re.UNICODE):
                                        origtext += " "
                                origtext += punct_replacement.strip() + " " + word
                            else:
                                if word == "'Europe":  # specific case
                                    origtext += " "
                                elif origtext != "":
                                    if not re.search(ur'[\' ]$', origtext, flags=re.UNICODE) and not re.match(
                                            ur"[\-'][^\W\d]+", word, flags=re.UNICODE):
                                        # print "adding space"
                                        origtext += " "
                                # print origtext + "|"
                                origtext += word
                                # print origtext + "|"
                        else:
                            if word == "***" and lastword == "***":  # i.e. ignore a second consecutive ***
                                pass
                            elif len(origtext) > 0:
                                if "(" in punct_replacement or ")" in punct_replacement:
                                    origtext += " "  # for no. 48
                                # if entryNumber == 49 : #and "," in punct_replacement: # specific problem for 49
                                if ":" in punct_replacement or u"»" in punct_replacement or "..." in punct_replacement:
                                    origtext += " "  # for 61
                                elif punct_replacement in ['?', "!"] and re.search(ur'\w$', origtext, flags=re.UNICODE):
                                    pass
                                # elif ";" in punct_replacement: pass
                                elif len(punct_replacement) == 1 and (
                                        u"«" in punct_replacement or "?" in punct_replacement) and origtext[-1] != ":":
                                    origtext += " "  # for 70
                                    #    print "prepl", punct_replacement
                                    #    pass
                                    # else:
                            origtext += punct_replacement
                        print "punct replacement", punct_replacement

                        if correctedWord is not None:
                            if correctedWord != "-":
                                if correctedText != "": correctedText += " "
                                correctedText += correctedWord
                        else:
                            if word != "***":
                                if correctedText != "": correctedText += " "
                                correctedText += word
                            else:
                                if lastword != "***":
                                    correctedText += punct_replacement
                        print "recon origtext:", origtext
                        lastword = word
                        #lastcorrectword = correctedWord

                if entryNumber == 144:  # problem with ',' after a deleted word, ambiguous if before or after
                    origtext = u"Alors, me dire, à quel jour arriverais toi exactement? Parce que la semaine" \
                               u" prochaine je vais aller à Brisbane pendant deux semaines."
                elif entryNumber == 155:
                    origtext = u"À bientôt, de ton meilleur copain"  # same problem with de
                elif entryNumber == 162:  # same prob
                    origtext = u"Nous mangerons à tout les restaurants des quartiers d'est, dans la premiére semaine."
                elif entryNumber == 221:
                    origtext = u'Bon appétit au « Dragon Court Restaurant »!'  # 2 punct and one *** at the end
                elif entryNumber == 223:  # . ambiguous after deleted word
                    origtext = u"Il est le mieux garde secret au « Kingston ». Il l'emplacement est" \
                               u" « Dragon Court Mall » en « Ligueanea »."
                elif entryNumber == 226:  # ditto
                    origtext = u"C'été a délicieux, j'aime vraiment beaucoup. Nous avons fait rôti du" \
                               u" canard avec un miel sauce ( j'aime bien, il goûte différent ) et un" \
                               u" poulet en sauce de limon avec riz blanc pour de plat de principal."
                elif entryNumber == 230:  # ' problems:
                    origtext = u"Hier Soir j'ai dîné chez 'Guilt Trip.' Il était plus que fantastique." \
                               u" Il faut absolument y aller."
                elif entryNumber == 231:  # ditto
                    origtext = u"Guilt trip est situé dans la nouvelle 'Orchid Plaza' un cadre assez" \
                               u" enchanté. L'ambiance est chaleureuse et intime."
                elif entryNumber == 236:  # " probs
                    origtext = u'Les déserts peut les quelles le "Guilt Trip" est le plus conçu ne deceve.'
                elif entryNumber == 247:  # , probs
                    origtext = u"Clienteles sont bourgeoise et jeune. La cuisine essentiellement" \
                               u" de les mer de sea. C,est beau a voir les repas."
                elif entryNumber == 255:  # double punct at end
                    origtext = u"Le décor est très simple et traditionnel. Il a une intime ambiance." \
                               u" Les tables et les chaises sont basses ( ils sont peu pouces de le sol )."
                elif entryNumber == 270:  # double $ problem
                    origtext = u"Il y'a italienne japonaise, caraïbes,et la cuisine de américaine." \
                               u" N'attendrè pas à la prix modeste. Un plat coute $JA 500 - $JA2650."
                elif entryNumber == 273:  # punct at end
                    origtext = u'Le film le plus reussi que j\'ai vu cette annee c\'est la seance' \
                               u' d\'"Une Pure Formalite".'
                elif entryNumber == 274:  # . at end
                    origtext = u"Ce film, très bizarre, avait la puissance qu'on ne trouverait" \
                               u" pas dans un film ordinaire. Gérard Depardieu, en tant que" \
                               u" caractère principal était excellente dans sa rôle."
                elif entryNumber == 293:  # punct
                    origtext = u'Des clochars s\'y sont plû, des noctambulles s\'y sont éggarés,' \
                               u' des poêtes s\'en sont inspiré, et d\'ailleur' \
                               u' "leur chansons courrent encore dans les rue."'

                print origtext
                print origTextMainPage
                print correctedText
                print correctedtextmainpage
                if re.sub(ur"[^\w\-']+", "", origtext, flags=re.UNICODE) != re.sub(ur"[^\w\-']+", "", origTextMainPage,
                                                                             flags=re.UNICODE):
                    print "orig prob"
                    print
                    exit(1)

                corpus.append(Entry(entryNumber, origtext, correctedText, worderrors))

            rowcount += 1
            # if rowcount > 300: break
    return corpus


# base file name will have _ + entry number + .txt added to it
# and ".json" for the whole corpus
def save_corpus(corpus, baseFilename, outjsonfilename):
    # save one text file per entry and a .json for the whole
    for entry in corpus:
        outtextfilename = baseFilename + "_" + str(entry.entrynumber) + ".txt"
        with codecs.open(outtextfilename, mode='w', encoding='utf8') as outtextfile:
            outtextfile.write(entry.origtext)
    # outjsonfilename = baseFilename + ".json"
    jsoncorpus = [(entry.entrynumber, entry.origtext, entry.correctedtext, entry.worderrorlist) for entry in corpus]
    with codecs.open(outjsonfilename, mode='w', encoding='utf8') as outjsonfile:
        json.dump(jsoncorpus, outjsonfile)


corpushtmlfile = "/home/nparslow/Documents/AutoCorrige/SpellChecker/errorsCorpusCorrected.html"

corpus = readCorpus(corpushtmlfile)
outjsonfilename = "/home/nparslow/Documents/AutoCorrige/Corpora/SpellCheckerJson/entry.json"
save_corpus(corpus, "/home/nparslow/Documents/AutoCorrige/Corpora/SpellChecker/entry", outjsonfilename)
