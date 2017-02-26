import collections
import nltk.metrics
from nltk.metrics import precision, recall, f_measure
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords

import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

for word in movie_reviews.words(categories=['pos']):
    print(word)