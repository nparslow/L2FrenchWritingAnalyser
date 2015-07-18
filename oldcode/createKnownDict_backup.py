# coding=utf-8
__author__ = 'nparslow'

import codecs
import re
import unicodedata
import json

corpusdirectory = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/"
corpusdirectory = "/home/nparslow/Documents/AutoCorrige/SpellChecker/sxpipeTokenisedWiki/divided/"

#corpusfilename = "mi-frwiki1" # half wiki
corpusfilename = "frwiki_net.tok" # full wiki
corpusfilename = "mini_frwiki_net_train.tok" # first 50k lines of dev part
corpusfilename = "frwiki_net_dev.tok" # 7,000,000 lines
#corpusfilename = "editions.tok"


#def readfile(fullfilename):
word2count = {}

#with codecs.open(corpusdirectory + corpusfilename, encoding='utf-8') as corpusfile:
fullfilename = corpusdirectory + corpusfilename
with codecs.open(fullfilename, encoding='utf-8') as corpusfile:

    lineNumber = 0
    for line in corpusfile:
        origline = line
        lineNumber += 1
        # remove lines with jpg/gif files in them as the filename is often split
        # same for urls
        if not re.search(ur'((jpg|gif)\\\||http : )', line, flags=re.UNICODE | re.IGNORECASE ):
            # there are lots of encodings {alternative form of word} e.g. {specialisé \( e \) } spécialisées
            line = re.sub(ur'\{.+\}', ur'', line) # note this can lead to two subsequent spaces, so need to avoid empty string
            # remove { { citation\| parts:
            line = re.sub(ur'\{ \{ citation\\\|', ur'', line)
            # split on space or \|, make the brackets non-capturing with ?:
            words = re.split(ur'\s*(?:\s|(?:\\\|))\s*', line.strip(), flags=re.UNICODE)
            # there are some empty lines and these lead to the empty string in the vocab, or lines with everything but
            # a space removed
            #print words
            for word in words:
                # found word with 'left to right mark' !?!?!?
                word = re.sub(ur'\u200e', '', word, flags=re.UNICODE)

                if len(word) > 0 and not re.match(ur'\s+$', word, flags=re.UNICODE):



                    if word == "": print words, len(line), line, lineNumber, origline


                    try:
                        word2count[word] += 1
                    except KeyError:
                        word2count[word] = 1
        #if lineNumber > 1000000: break
        if lineNumber % 100000 == 0: print lineNumber, "lines read" # about 22 million I think


#readfile(corpusdirectory + corpusfilename)
MINCOUNT = 50
replacedwords = {}

# we do a loop first to divide up tokens which are rare but divisible:
for word in word2count.keys():
    if word2count[word] < MINCOUNT:
        # try segmenting the word further using -, ~ and ., if we get words already seen then keep them
        newtokens = re.split(ur'[\-~_/→，]', word, flags=re.UNICODE)
        newtokensdot = re.split(ur'[\.\-\~_/→，]', word, flags=re.UNICODE)
        if len(newtokens) > 1 and len([x for x in newtokens if x not in word2count]) == 0:
            for newtoken in newtokens:
                word2count[newtoken] += word2count[word]

            #print "adding 2"
            #totaltokens += len(newtokens)*word2count[word]
            del(word2count[word])
        elif len(newtokensdot) > 1 and len([x for x in newtokensdot if x not in word2count]) == 0:
            for newtoken in newtokensdot:
                word2count[newtoken] += word2count[word]
            #print "adding 3"
            #totaltokens += len(newtokensdot)*word2count[word]
            del(word2count[word])


toolowtypes = 0
toolowtokens = 0
totaltokens = 0
#print sum(word2count.values())
#runningtotal = 0
digitdict = {}
for word in word2count.keys():
    #print word, word2count[word]
    #runningtotal += word2count[word]

    if word2count[word] >= MINCOUNT:
        #print "adding 1"
        totaltokens += word2count[word]
    else:
        # i.e. less than MINCOUNT
        #print x
        toolowtypes +=1
        toolowtokens += word2count[word]

        # NB: (?:[^\W_\d]|\'|\-)  means any letter or ' or -
        # [^W_\d](?:[^\W_\d]|\'|\-)* is any such sequence starting with a letter


        # try to categorise the word:
        newword = word
        # strip any punctuation before (if not before a number) or after: require at least 2 characters
        if (not word[0] in u'†') and len(word) > 1:
            newword = re.sub(ur'^[\W_]+(?=[^\W\d_])', '', newword, flags=re.UNICODE)
            newword = re.sub(ur'^[^\w\-][\W-]*(?=[^\W_])', '', newword, flags=re.UNICODE)
            newword = re.sub(ur'(?<=[^\W_])\W+$', '', newword, flags=re.UNICODE)
        #print "wo", word2count[word], newword
        if newword == word or newword not in word2count:

            #print "yo", word2count[word]

            # group numbers together (we ignore the no. of digits, if it's decimal etc.), optional - in front
            if re.match(ur'([Nn]°)?\-?\d+(\.\d+)?$', newword, flags=re.UNICODE):
                newword = "_NUM_"
                '''
                # todo we could group numbers by pos/neg, no. of digits, dec or not, more than 2 after point etc.
                print "number:", word, len(word)
                lennum = re.findall(ur'\d', newword, flags=re.UNICODE)
                if len(word) not in digitdict: digitdict[len(word)] = 0
                digitdict[len(word)] += 1
                '''
            # numbers of form 0000.00000.0000 etc.
            elif re.match(ur'(\d+\.)+\d*$', newword, flags=re.UNICODE):
                newword = "_DOTNUMBER_"

            # filenames: (before foreign as can include foreign characters)
            elif re.match(ur'[\w\-]+\.(?:pdf|svg|je?pg|doc|png|html?|aspx?)$', newword.lower(), flags=re.UNICODE):
                newword = "_FILENAME_"
                #print "filename:", word # doesn't seem to pick up many atm ...

            # look for foreign words (with non-french characters) # latin1 has too many non-french chars
            # Ll = latin 1, Zs = Separator Space, Cc = other control characters
            # Nd = number etc. Po & Ps = Punctuation
            #elif len([x for x in categories if x not in  ['Ll', 'Po', 'Nd']
            #          and x not in [ '-', '(', ')', u'«', u'»', '[', ']', u'€', u'’', u'“', u'”']]) > 0:
            #    newword = "_FOREIGN_"
            # note this will include alpha, beta etc.
            # note this will include 'modifier characters' (e.g. a diacritic but without a letter) as \w detects it
            # also includes ² which matches \w but doesn't match \d  wtf?!?!?!
            elif len([x for x in newword.lower() if x not in
                    u'abcdefghijklmnopqrstuvwxyz0123456789ùûüÿàâæçéèêëïîôœ_' and re.match(ur'\w', x, re.UNICODE)]) > 0:
                #print "foreign?                                 ", newword, [x for x in newword.lower() if x not in
                #    u'abcdefghijklmnopqrstuvwxyz0123456789ùûüÿàâæçéèêëïîôœ_' and re.match(ur'\w', x, re.UNICODE)]
                newword = "_FOREIGN_"
                #print "foreign:", word
                # could subclassify as one character v multiple characters

            # look for acronyms:
            # this includes a lot of words in caps, and other stuff, todo check if lower version is known?
            # some roman numerals in here
            elif re.match(ur'(?:[^\W_\d]\.?)+$', newword, flags=re.UNICODE) and newword.isupper():
                newword = "_INITIALS_"
                #print "initials:", word

            # look for if word is only letters and all lower case:
            # this is where the interesting stuff is:, some foreign words in here
            elif re.match(ur'[^\W_\d](?:[^\W_\d]|\'|\-)*$', newword, flags=re.UNICODE) and newword.islower():
                newword = "_ALLLOWER_"
                #print "all lower:", word

            # look for first letter in upper case, the rest in lower case: (we need the min trick as python doesn't check in the right order)
            # includes some 2 & 3 letter abbreviations Etc, It , some hyphenated place names
            # elements Hg
            elif len(word) > 1 and newword[0].isupper() and re.match(ur'(?:[^\W_\d]|\'|\-)+$', newword[min(1,len(word)-1):], flags=re.UNICODE):
                newword = "_FIRSTUPPER_"
                #print "first upper:", word

            # look for mixed upper and lower:
            # a lot of d' or de or l'or -l' etc.l+ caps, some foreign e.g. el-Name al-Name todo separate l/d
            elif len(word) > 1 and re.match(ur'[^\W_\d](?:[^\W_\d]|\'|\-)*$', newword, flags=re.UNICODE) and not newword.islower() and \
                not newword.isupper():
                newword = "_MIXEDUPPERLOWER_"
                #print "mixed upperlower", word

            # look for pure punctuation:
            elif re.match(ur'[^\w_]+$', newword, flags=re.UNICODE):
                newword = "_PUNCT_"
                #print "punct", word

            # look for a mix of upper case letters and numbers (dashes and underscores and dots allowed):
            elif re.match(ur'[\w\-\.]+$', newword, flags=re.UNICODE) and newword.isupper():
                newword = "_NUMUPPERMIX_"
                #print "mix nums and uppers", word

            # look for dates with dots :
            elif re.match(ur'\d{1,4}\.\d{1,4}\.\d{2,4}$', newword, flags=re.UNICODE):
                newword = "_DATE_"
                #print "date", word # todo nothing here!

            # look for 39e / 15ème / 5è: etc.
            elif re.match(ur'\d+(?:e|i?èmes?|è|i?ères?|emes?|nd|rd|th|st)$', newword, flags=re.UNICODE):
                newword = "_ORDINAL_"
                #print "ordinal", word

            # look for area: e.g. 300x200
            elif re.match(ur'\d+(?:\.\d+)?x\d+(?:\.\d+)?$', newword, flags=re.UNICODE):
                newword = "_AREA_"
                #print "area", word

            # look for a web addresse, the www is optional:
            elif re.match(ur'(?:www\.)?(?:[\w\-]+\.)+(?:edu|org|comfgov|com|gov|tv|net|info|mil|ac|biz|art|ep|bz|gouv|'
                          ur'sk|cz|ie|ua|cu|by|in|eu|pt|nl|es|lu|lib|nu|bf|rm|go|id|co|ch|de|ru|fm|fr|be|it|ee|'
                          ur'ws|yu|pa|bg|tk|pf|uk|jp|ro|pl|se|au|dk|lv|hr|fi|ae|za|bg|ge|lu|us|at|ba|cl|pt|ca|'
                          ur'gl|si|om|gr|mg|nc|hu|ma)+', newword, flags=re.UNICODE):
                newword = "_WEBSITE_"
                #print "website", word

            # some www don't have an ending:
            elif re.match(ur'www\.\w+', newword, flags=re.UNICODE):
                newword = "_WEBSITE_"

            # look for a time
            elif re.match(ur'[0-2]?[0-9]h(?:[0-5][0-9])?', newword, flags=re.UNICODE):
                newword = "_TIME_"
                #print "time type1", word

            # note can be anything after it atm... may cause problems
            elif re.match(ur'(?:\d?\d[Hh])?\d+min(?:utes)?(?:\d\d)?', newword, flags=re.UNICODE):
                newword = "_TIME_"
                print "time type2", word # todo none here!!

            # partially segmented ISBN:
            elif re.match(ur'[0-3]\-\d{2,6}', newword, flags=re.UNICODE):
                newword = "_PARTIALISBN_"
                #print "isbn part", word

            # num dash num e.g. 2-3
            elif re.match(ur'\d\-\d$', newword, flags=re.UNICODE):
                newword = "_NUMDASHNUM_"
                print "num dash num", word # todo none here!!

            # check if there's a . at the end, maybe with a ' before it:
            #elif (word.endswith('.') and newword[:-1] in word2count) or \
            #    (word.endswith("'.") and newword[:-2] in word2count):
            #    newword = newword[:-1]
            #    print "punc before/after", word # todo none here!!

            elif re.match(ur'†', newword, flags=re.UNICODE):
                newword = "_CHURCH_"
                #print "church", word

            # a@b (with no dots after @) seems to be missed:
            # todo should check if replacing @ with a makes a word
            # e.g. Les@anarchistes, Cryptogra@phie, System@tic
            elif re.match(ur'([\w\-]\.)*[\w\-]+@[\w\-]+(?:\.[^\W\d]{2,4}){0,2}$', newword, flags=re.UNICODE):
                newword = "_AATB_"
                #print "a at b", word

            elif re.match(ur'\d+bis$', newword, flags=re.UNICODE):
                newword = "_BIS_"
                #print "bis", word

            # alphanumeric hat alphanumeric seems to come up a lot
            elif re.match(ur'\w\^\w$', newword, flags=re.UNICODE):
                newword = "_HAT_"
                #print "hat", word # todo none here

            # date range is missed:
            elif re.match(ur'(janv?|févr?|mars?|avri?|mai|juin|juil|août|sept?|octo?|nove?|déc)\.?\-'
                          ur'(janv?|févr?|mars?|avri?|mai|juin|juil|août|sept?|octo?|nove?|déc)\.?$', newword.lower(), flags=re.UNICODE):
                newword = "_DATERANGE_"
                print "date range", word # todo none here

            # if after all the others it has only letters call it a word:
            elif re.match(ur'[^\W_\d](?:[^\W_\d]|\'|\-)*$', newword, flags=re.UNICODE):
                newword = "_OTHERWORD_"
                # never seems to come in here ...
                #print "                                          ", newword, newword
                print "other word", word # todo this is covered by the alllower and similar above!

            # numbers followed by one or two letters: (this includes some years like 1983a etc.)
            # todo this doesn't seem to be a particularly coherent group! some years
            # todo e.g. 1987b 2005a etc.
            elif re.match(ur'(?:\-?\d+\.)?\d+[^\W\d_]{1,2}$', newword, flags=re.UNICODE):
                newword = "_MEASURE_"
                #print "measure", word

            # letters followed by numbers, can have _ and -:
            # most common x l a b : could sub categorise for these
            elif re.match(ur'[^\W\d][\d\-_]+$', newword, flags=re.UNICODE):
                newword = "_MODEL_"
                #print "model", word

            # known abbreviations: (prob should be earlier)
            elif re.match(ur'(km2|i\.e\.|e\.g\.|a\.k\.a\.)', newword, flags=re.UNICODE):
                newword = "_ABBREV"
                #print "abbrev", word
            # no. ? n°
            #elif re.match(ur'n°')

            # todo these should be cut in 2 and see if the word-like part is a word
            elif re.match(ur'[^\W\d]+\d+$', newword, flags=re.UNICODE):
                newword ="_LETTSNUMS_"

            # numbers followed by letters
            elif re.match(ur'\d+[^\W\d]+$', newword, flags=re.UNICODE):
                newword = "_NUMSLETTS_"

            elif re.match(ur'(([^\W\d]|\')\-)+([^\W\d]|\')$', newword, flags=re.UNICODE):
                newword = "_HYPHENATED_"

            # these are with letters rather than pure numbers:
            elif re.match(ur'[nN]°\w+$', newword, flags=re.UNICODE):
                newword = "_NUMERONAME_"

            # if a word
            else:
                #print word, "\t", newword #, len(word) > 1, re.match(ur'[^\W_\d]([^\W_\d]|\'|\-)*$', word, flags=re.UNICODE), not word.islower(), not word.isupper()
                newword = "_OTHER_"
                print "other", word

        if len(newword) > 0:
            if newword[0] == "_":
                if newword not in replacedwords: replacedwords[newword] = []
                replacedwords[newword].append(word)

        if newword not in word2count: word2count[newword] = 0
        word2count[newword] += word2count[word]
        #print "adding 4", word2count[word]
        totaltokens += word2count[word]
        del(word2count[word])
    #print runningtotal, totaltokens
    #if totaltokens > runningtotal + 10: break



print sum(word2count.values())
print "tokens:", totaltokens, "types:", len(word2count)
print "too low tokens:", totaltokens, "too low types:", toolowtypes
print "fraction too low tokens", 1.0*toolowtokens/totaltokens
print "fraction too low types", 1.0*toolowtypes/len(word2count)

# for 100000 lines, 0.072 frac tokens, 0.78 frac types
# for 1000000 lines 0.030 frac tokens, 0.76 frac types
# for 22000000 lines (half wiki) 0.012 frac tokens, 0.78 frac types

# full wiki:
# wc -l frwiki_net.tok
# 44197571 frwiki_net.tok

#44100000 lines read
#tokens: 524061443 types: 4610298
#too low tokens: 524061443 too low types: 3649482
#fraction too low tokens 0.0101368571776
#fraction too low types 0.791593515213

if "" in word2count: print "empty string"
if " " in word2count: print "space"

# now save a vocab file with low freq words replaced by _UNK
# one word per line
vocabfilename = "wiki_vocab.txt"
with codecs.open(corpusdirectory + vocabfilename, 'w', encoding='utf-8') as vocabfile:
    vocabfile.write("_UNK\n")
    for x in sorted(word2count.keys()):
        if word2count[x] > MINCOUNT:
            vocabfile.write(x + "\n")

replacedFileName = "replaced.txt"
with codecs.open(corpusdirectory + replacedFileName, 'w', encoding='utf-8') as replfile:
    json.dump(replacedwords, replfile)