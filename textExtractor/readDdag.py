import codecs
import re

__author__ = 'nparslow'


def readDdag( ddagfilename, keepSentences = True ):

    sentences = []
    tokens = []
    with codecs.open(ddagfilename, mode="r", encoding="utf8") as udagfile:
        for line in udagfile:
            line = line.strip()
            if not line.startswith("##"):
                starttoknum, info_token , endtoknum =  line.split('\t')

                # we only want the token at this point:
                token = re.search(ur'(?:\{.+\})+ (.+)', line, flags=re.UNICODE).groups()[0]

                tokens.append(token)
            elif line.startswith("##DAG END"):
                # if we want to keep the sentence structure, make a separation
                if keepSentences:
                    sentences.append(tokens)
                    tokens = []
    if keepSentences:
        return sentences
    else:
        return tokens


def testDdag():
    filename = "/home/nparslow/Documents/AutoCorrige/Corpora/makePLexSplots/Calle_sxpipe_tokenised.txt"
    toks = readDdag(filename, keepSentences=True)
    print toks





if __name__ == "__main__":
    testDdag()