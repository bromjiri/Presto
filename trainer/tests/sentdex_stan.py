import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode

from nltk.tokenize import word_tokenize
import settings


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



stanford_pos = settings.TRAINER_DATA + "/twitter/stanford_pos_5000.csv"
stanford_neg = settings.TRAINER_DATA + "/twitter/stanford_neg_5000.csv"


stanford_pos_list = list()
stanford_neg_list = list()
with open(stanford_pos, 'r') as stanford_p:
    for line in stanford_p:
        stanford_pos_list.append(line.strip())

with open(stanford_neg, 'r') as stanford_n:
    for line in stanford_n:
        stanford_neg_list.append(line.strip())

stanford_p = stanford_pos_list[:1000]
stanford_n = stanford_neg_list[:1000]


documents_p = []
documents_n = []

for r in stanford_p:
    documents_p.append((r, "pos"))

for r in stanford_n:
    documents_n.append((r, "neg"))

all_words = []

for line in stanford_p:
    words = word_tokenize(line)
    for w in words:
        all_words.append(w)

for line in stanford_n:
    words = word_tokenize(line)
    for w in words:
        all_words.append(w)

all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


featureset_p = [(find_features(rev), category) for (rev, category) in documents_p]
featureset_n = [(find_features(rev), category) for (rev, category) in documents_n]



negcutoff = int(len(featureset_n) * 3 / 4)
poscutoff = int(len(featureset_p) * 3 / 4)

training_set = featureset_n[:negcutoff] + featureset_p[:poscutoff]
testing_set = featureset_n[negcutoff:] + featureset_p[poscutoff:]


classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)))
classifier.show_most_informative_features(15)
#
# MNB_classifier = SklearnClassifier(MultinomialNB())
# MNB_classifier.train(training_set)
# print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)
#
# BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
# BernoulliNB_classifier.train(training_set)
# print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set)) * 100)
#
# LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
# LogisticRegression_classifier.train(training_set)
# print("LogisticRegression_classifier accuracy percent:",
#       (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)
#
# SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
# SGDClassifier_classifier.train(training_set)
# print("SGDClassifier_classifier accuracy percent:",
#       (nltk.classify.accuracy(SGDClassifier_classifier, testing_set)) * 100)
#
# LinearSVC_classifier = SklearnClassifier(LinearSVC())
# LinearSVC_classifier.train(training_set)
# print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)
#
# NuSVC_classifier = SklearnClassifier(NuSVC())
# NuSVC_classifier.train(training_set)
# print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set)) * 100)
#
# voted_classifier = VoteClassifier(
#     NuSVC_classifier,
#     LinearSVC_classifier,
#     MNB_classifier,
#     BernoulliNB_classifier,
#     LogisticRegression_classifier)
#
# print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set)) * 100)