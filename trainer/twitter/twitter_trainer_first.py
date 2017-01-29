# sentdex NLTK tutorial: sentiment module
# stem, stop


import nltk
import random
import pickle
from nltk.classify.scikitlearn import SklearnClassifier

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
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


print("start")

tweets = []
all_words = []

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()


# append positive tweets

reader = open("../data/stanford_pos_2000.csv", "r").read()
for row in reader.split('\n'):
    tweets.append((row, "pos"))

    twe_pos_words = word_tokenize(row)
    for w in twe_pos_words:
        if not w in stop_words:
            all_words.append(ps.stem(w.lower()))

# append negative tweets
reader = open("../data/stanford_neg_2000.csv", "r").read()
for row in reader.split('\n'):
    tweets.append((row, "neg"))

    twe_neg_words = word_tokenize(row)
    for w in twe_neg_words:
        if not w in stop_words:
            all_words.append(ps.stem(w.lower()))



all_words = nltk.FreqDist(all_words).most_common(5000)
word_features = list()
for word in all_words:
    word_features.append(word[0])

# pickle reviews
# tweets_f = open("pickled/tweets.pickle", "wb")
# pickle.dump(tweets, tweets_f)
# tweets_f.close()

# pickle word_features
# word_features_f = open("pickled/word_features.pickle", "wb")
# pickle.dump(word_features, word_features_f)
# word_features_f.close()


def find_features(document):
    words = word_tokenize(document)
    lower_words = []
    for w in words:
        lower_words.append(ps.stem(w.lower()))

    features = {}
    for w in word_features:
        features[w] = (w in lower_words)

    return features


featuresets = [(find_features(tweet), category) for (tweet, category) in tweets]
# featuresets_f = open("pickled/featuresets.pickle", "wb")
# pickle.dump(featuresets, featuresets_f)
# featuresets_f.close()

random.shuffle(featuresets)

training_set = featuresets[:3600]
testing_set = featuresets[3600:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
classifier.show_most_informative_features(15)


MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)
# MNB_classifier_f = open("pickled/MNB_classifier.pickle", "wb")
# pickle.dump(MNB_classifier, MNB_classifier_f)
# MNB_classifier_f.close()


BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set)) * 100)
# BernoulliNB_classifier_f = open("pickled/BernoulliNB_classifier.pickle", "wb")
# pickle.dump(BernoulliNB_classifier, BernoulliNB_classifier_f)
# BernoulliNB_classifier_f.close()


LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:",
      (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)
# LogisticRegression_classifier_f = open("pickled/LogisticRegression_classifier.pickle", "wb")
# pickle.dump(LogisticRegression_classifier, LogisticRegression_classifier_f)
# LogisticRegression_classifier_f.close()


# SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
# SGDClassifier_classifier.train(training_set)
# print("SGDClassifier_classifier accuracy percent:",
#       (nltk.classify.accuracy(SGDClassifier_classifier, testing_set)) * 100)


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)
# LinearSVC_classifier_f = open("pickled/LinearSVC_classifier.pickle", "wb")
# pickle.dump(LinearSVC_classifier, LinearSVC_classifier_f)
# LinearSVC_classifier_f.close()


NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set)) * 100)
# NuSVC_classifier_f = open("pickled/NuSVC_classifier.pickle", "wb")
# pickle.dump(NuSVC_classifier, NuSVC_classifier_f)
# NuSVC_classifier_f.close()


voted_classifier = VoteClassifier(
    NuSVC_classifier,
    LinearSVC_classifier,
    MNB_classifier,
    BernoulliNB_classifier,
    LogisticRegression_classifier)

print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set)) * 100)

