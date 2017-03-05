
from nltk.metrics import *
from nltk.tokenize import word_tokenize
import collections
import nltk



reference = 'DET NN VB DET JJ NN NN IN DET NN'.split()
test    = 'DET VB VB DET NN NN NN IN DET NN'.split()
print(accuracy(reference, test))

COUNT = 500

print(round(COUNT*8/10))

array = [1,1,1,2,2,3]

numbered_grams = nltk.FreqDist(array).most_common(None)
print(numbered_grams)

res = word_tokenize("$NFLX number on thing I have not learned trading is don&#39;t chase")
print(res)

pos = nltk.pos_tag(res)
print(pos)