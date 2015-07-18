import codecs
import re

__author__ = 'nparslow'


'''
Reads an options file,
ignores lines starting with # (or any line containing only space(s))
options should be of form
optionname tab parameter
(with multiple parameters separated by tabs)
sequences of repeated tabs are interpretted as single tabs
divides options into two groups: global parameters and variable parameters
global parameters:
  dictionary, name : list of values
variable parameters:
  list of 2-tuples (variable name, list of parameters)
returns the global params and the variable params
if an option is unrecognised, prints a warning and continues
'''
def readOptionsFile( optionsfilename ):
    globalparams = {
        "lexiqueDict":None,
        "word2vecmodel":None,
        "bigrammodel":None,
        "outdir":None,
        "origtextdir":None,
        "melteddir":None,
        "ddageddir":None,
        "frmgeddir":None,
        "corpusName":None,
        "headerInfo":None,
    }
    possiblevariables = {
        "paragraphs",
        "sentences",
        "words",
        "sentsPerPara",
        "wordsPerSent",
        "lettersPerWord",
        "syllablesPerWord",
        "PLex",
        "S",
        "altS",
        "vocd",
        "mtld",
        "hdd",
        "LFP",
        "spellcorr",
        "meltdiff",
        "meanmelt",
        "parsed",
        "weightPerWord",
        "verb",
        "clause",
        "w2vct",
        "treeTypesPerSent",
        "TreeTypesHDD",
        "TreeTypesYuleK",
        "noVerbSentences",
        "toksBeforeMainVerb",
    }
    variableparams = []
    with codecs.open( optionsfilename, mode="r") as ofile:
        for line in ofile:
            if line[0] != "#" and re.search(ur'\S', line, flags=re.UNICODE):
                line = line.strip()
                # in python 3 can do a, *b = somelist to assign first element to a and the rest to b
                option_params = line.split('\t')
                option_params = re.split(ur'\t+', line, flags=re.UNICODE)
                # parrams can be an empty list
                option, params = option_params[0], option_params[1:]
                # if params has one element it won't be a list, so we change it for consistency:
                if type(params) != list:
                    params = [params]
                # convert to int if possible, else float, else leave as a unicode string
                for i in range(len(params)):
                    try:
                        params[i] = int(params[i])
                    except:
                        try:
                            params[i] = float(params[i])
                        except:
                            pass
                if option in globalparams:
                    globalparams[option] = params
                elif option in possiblevariables:
                    variableparams.append( (option, params) )
                else:
                    print "Warning: unknown option in optionsfile", line
    return globalparams, variableparams


# testing the function
def main():
    filename = "optionsfile.txt"
    globalparams, variableparams = readOptionsFile(filename)
    print globalparams
    print variableparams




if __name__ == "__main__":
    main()