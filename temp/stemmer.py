import nltk

import settings
import random
import nltk
import csv
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.util import ngrams
from nltk.corpus import movie_reviews



stop_words = set(stopwords.words('english'))
# print(stop_words)

words = nltk.word_tokenize("Sad, sad, sad. I don't know why but it it 8.67")

print(words)
pos = nltk.pos_tag(words)
print(pos)



# negids = movie_reviews.fileids('neg')
# posids = movie_reviews.fileids('pos')
#
# for f in negids:
#     words = movie_reviews.words(f)
#     for w in words:
#         print(w)
#     exit()