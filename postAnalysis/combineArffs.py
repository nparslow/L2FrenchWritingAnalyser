import codecs
import re

__author__ = 'nparslow'

def readarff( filename ):
    vars = []
    rows = []
    header = ""
    with codecs.open( filename, mode="r", encoding="utf8") as f1:
        indata = False
        for line in f1:
            if line.lower().startswith("@attribute"):
                att, name, typ = re.split(ur'\s', line.strip(), flags=re.UNICODE)
                vars.append( (att, name, typ) )
            elif line.lower().startswith("@data"):
                indata = True
            elif indata:
                row = line.strip().split(',')
                rows.append(row)
            else:
                # add to header
                header += line
    return header, vars, rows


def main():
    arff1 = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/testclass.arff"
    arff2 = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/testtrees.arff"
    outarff = "/home/nparslow/Documents/AutoCorrige/Corpora/figures/testcombined.arff"

    header = ""



    header1, vars1, rows1 = readarff(arff1)
    header2, vars2, rows2 = readarff(arff2)

    with codecs.open( outarff, mode="w", encoding="utf8") as of:
        of.write(header1)
        nvars = 0
        for i_var in range(len(vars1)-1):
            var = vars1[i_var]
            #print var
            of.write( u"\t".join(var) + "\n")
            nvars += 1
        for i_var in range(len(vars2)):
            var = vars2[i_var]
            of.write( "\t".join(var) + "\n")
            nvars += 1
        of.write("\n")
        of.write("@DATA\n")
        rowlen = 0
        for row1, row2 in zip(rows1, rows2):
            of.write(",".join(row1[:-1]+row2) + "\n")
            rowlen = len(row1[:-1] + row2)

        print "vars", nvars, rowlen



if __name__ == "__main__":
    main()


