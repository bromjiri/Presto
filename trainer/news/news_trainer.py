# sentdex NLTK tutorial: sentiment module
# stem, stop

import logging
import os
import nltk
import random
import pickle
from nltk.classify.scikitlearn import SklearnClassifier

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


def read_input_file(reader):

    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    labeled_sentences = list()
    all_words = list()

    for row in reader:
        row_split = row.split("\t")
        labeled_sentences.append((row_split[0].strip(), row_split[1].strip()))

        words = word_tokenize(row_split[0])
        for w in words:
            if not w in stop_words:
                all_words.append(ps.stem(w.lower()))

    return all_words, labeled_sentences


def find_features(document, word_features):
    ps = PorterStemmer()
    words = word_tokenize(document)
    lower_words = []
    for w in words:
        lower_words.append(ps.stem(w.lower()))

    features = {}
    for w in word_features:
        features[w] = (w in lower_words)

    return features

##################
# start

# Logging settings
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt='%Y%m%d-%H:%M')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# console
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.info("starting " + os.path.basename(__file__))

#####

# get text from input files
all_inputs = []
input_files = ["data/amazon_cells_labelled.txt", "data/imdb_labelled.txt", "data/yelp_labelled.txt"]
for input_file in input_files:
    file = open(input_file, "r")
    all_inputs += file

all_words, labeled_sentences = read_input_file(all_inputs)

# sort words
sorted_words = nltk.FreqDist(all_words).most_common(5000)
word_features = list()
for word in sorted_words:
    word_features.append(word[0])

# get feature sets
featuresets = [(find_features(sentence, word_features), category) for (sentence, category) in labeled_sentences]
random.shuffle(featuresets)


training_set = featuresets[:2500]
testing_set = featuresets[2500:]


classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
classifier.show_most_informative_features(15)

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set)) * 100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:",
      (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set)) * 100)


voted_classifier = VoteClassifier(
    NuSVC_classifier,
    LinearSVC_classifier,
    MNB_classifier,
    BernoulliNB_classifier,
    LogisticRegression_classifier)

print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set)) * 100)


