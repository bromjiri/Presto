import trainer.dataset as ds
import random
import nltk

from statistics import mode

from nltk.classify import ClassifierI
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, NuSVC


def find_features(sentence_original, all_grams):

    sentence_grams = ds.create_grams(pos=None, stop=True, stem=True, bigram=True, sentence=sentence_original)

    features = {}
    for gram in all_grams:
        features[gram] = (gram in sentence_grams)
    return features

def find_features_train(sentence_grams, all_grams):

    features = {}
    for gram in all_grams:
        features[gram] = (gram in sentence_grams)
    return features

def get_feature_set(dataset):

    all_grams = dataset.get_common_grams(5000)
    sentence_list = dataset.get_sentence_list()

    feature_set = list()
    for sentence in sentence_list:
        features = find_features_train(sentence.grams, all_grams)
        feature_set.append([features, sentence.sentiment])

    return feature_set


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


if __name__ == '__main__':
    stanford_set = ds.Dataset("stanford", count=2000)
    stanford_set.create_grams(pos=None, stop=False, stem=False, bigram=False, lower=True)
    # stanford_set.create_grams(pos=["J", "V", "N", "R"], stop=True, stem=True, bigram=True)
    feature_set = get_feature_set(stanford_set)

    print(len(feature_set))
    print("feature_set loaded")

    training_set = feature_set[:1800]
    testing_set = feature_set[1800:]

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
    classifier.show_most_informative_features(20)

    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier._vectorizer.sort = False
    MNB_classifier.train(training_set)
    print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)

    BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    BernoulliNB_classifier._vectorizer.sort = False
    BernoulliNB_classifier.train(training_set)
    print("BernoulliNB_classifier accuracy percent:",
          (nltk.classify.accuracy(BernoulliNB_classifier, testing_set)) * 100)

    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier._vectorizer.sort = False
    LogisticRegression_classifier.train(training_set)
    print("LogisticRegression_classifier accuracy percent:",
          (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)

    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier._vectorizer.sort = False
    LinearSVC_classifier.train(training_set)
    print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)

    NuSVC_classifier = SklearnClassifier(NuSVC())
    NuSVC_classifier._vectorizer.sort = False
    NuSVC_classifier.train(training_set)
    print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set)) * 100)


    voted_classifier = VoteClassifier(
        NuSVC_classifier,
        LinearSVC_classifier,
        MNB_classifier,
        BernoulliNB_classifier,
        LogisticRegression_classifier)

    print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set)) * 100)