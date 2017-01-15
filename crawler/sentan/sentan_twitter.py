# sentiment module, pickled from stanford_filter5, 75% accuracy
import pickle
import os

from nltk.classify import ClassifierI
from statistics import mode

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


dir_path = os.path.dirname(__file__)
ps = PorterStemmer()

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


# load word_features
file_path = os.path.join(dir_path, 'pickled/word_features.pickle')
word_features_f = open(file_path, "rb")
word_features = pickle.load(word_features_f)
word_features_f.close()


def find_features(document):
    words = word_tokenize(document)
    lower_words = []
    for w in words:
        lower_words.append(ps.stem(w.lower()))

    features = {}
    for w in word_features:
        features[w] = (w in lower_words)

    return features


file_path = os.path.join(dir_path, 'pickled/MNB_classifier.pickle')
open_file = open(file_path, "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()


file_path = os.path.join(dir_path, 'pickled/BernoulliNB_classifier.pickle')
open_file = open(file_path, "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()


file_path = os.path.join(dir_path, 'pickled/LogisticRegression_classifier.pickle')
open_file = open(file_path, "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()


file_path = os.path.join(dir_path, 'pickled/LinearSVC_classifier.pickle')
open_file = open(file_path, "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()


file_path = os.path.join(dir_path, 'pickled/NuSVC_classifier.pickle')
open_file = open(file_path, "rb")
NuSVC_classifier = pickle.load(open_file)
open_file.close()


voted_classifier = VoteClassifier(
    NuSVC_classifier,
    LinearSVC_classifier,
    MNB_classifier,
    BernoulliNB_classifier,
    LogisticRegression_classifier)


def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)
