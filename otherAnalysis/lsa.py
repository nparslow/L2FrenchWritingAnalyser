from numpy import zeros
#from scipy.linalg import svd
from scipy.sparse.linalg import svds as svd # for memory heavy applications use this
#following needed for TFIDF
from math import log
from numpy import asarray, sum

# re. http://www.puffinwarellc.com/index.php/news-and-articles/articles/33.html?showall=1



class LSA(object):
    def __init__(self, stopwords, ignorechars):
        self.stopwords = stopwords
        self.ignorechars = ignorechars
        self.wdict = {} # word to list of doc_ids in which it appears e.g. self.wdict['book'] = [3,4]
        self.dcount = 0        
    def parse(self, doc):
        words = doc.split();
        for w in words:
            #print w, self.ignorechars, type(w)
            # translate won't work directly with unicode, so try this:
            if type(w) == unicode:
                translation_table = dict.fromkeys(map(ord, self.ignorechars), None)
                w = w.lower().translate(translation_table)
            else:
                w = w.lower().translate(None, self.ignorechars) # None = no translation, self.ignorechars = list of chars that will be deleted from the string
            if w in self.stopwords:
                continue
            elif w in self.wdict:
                self.wdict[w].append(self.dcount)
            else:
                self.wdict[w] = [self.dcount]
        self.dcount += 1      
    def build(self): # builds the matrix from the counts
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        self.keys.sort()
        self.A = zeros([len(self.keys), self.dcount])
        for i, k in enumerate(self.keys):
            for d in self.wdict[k]:
                self.A[i,d] += 1
    def calc(self): # calculate the svd
        self.U, self.S, self.Vt = svd(self.A)
    # TFIDF = (Ni,j / N*,j ) * log( D / Di ) where
    # Ni,j = no. of times term i appears in doc j
    # N*,j = no. of total words in document
    # D = no. of documents
    # Di = no. of documents in which word i appears
    def TFIDF(self): 
        WordsPerDoc = sum(self.A, axis=0)        
        DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
        rows, cols = self.A.shape
        for i in range(rows):
            for j in range(cols):
                self.A[i,j] = (self.A[i,j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])
    def printA(self): # print the count matrix
        print 'Here is the count matrix, dimensions', len(self.A), " by ", len(self.A[0])
        print self.A
    def printSVD(self):
        print 'Here are the singular values'
        print self.S
        print 'Here are the first 3 columns of the U matrix' # U is the list of vectors for each term
        print -1*self.U[:, 0:3]
        print 'Here are the first 3 rows of the Vt matrix' # V is the list of vectors for each document
        print -1*self.Vt[0:3, :]
	# note that 1st dimension is ignored as correlates with how many words are in each document
	# don't center matrix as you want it to remain sparse


#titles = ["The Neatest Little Guide to Stock Market Investing",
#          "Investing For Dummies, 4th Edition",
#          "The Little Book of Common Sense Investing: The Only Way to Guarantee Your Fair Share of Stock Market Returns",
#          "The Little Book of Value Investing",
#          "Value Investing: From Graham to Buffett and Beyond",
#          "Rich Dad's Guide to Investing: What the Rich Invest in, That the Poor and the Middle Class Do Not!",
#          "Investing in Real Estate, 5th Edition",
#          "Stock Investing For Dummies",
#          "Rich Dad's Advisors: The ABC's of Real Estate Investing: The Secrets of Finding Hidden Profits Most Investors Miss"
#          ]
#stopwords = ['and','edition','for','in','little','of','the','to'] # words to ignore
#ignorechars = ''',:'!''' # punctuation (characters) to ignore (in 3 quotes, so ,:'! are the four ignored
'''
mylsa = LSA(stopwords, ignorechars)
for t in titles:
    mylsa.parse(t)
mylsa.build()
mylsa.printA()
mylsa.calc()
mylsa.printSVD()
'''
