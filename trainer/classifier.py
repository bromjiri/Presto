import nltk
import collections
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import precision, recall, f_measure
import datetime
from statistics import mode

from nltk.classify import ClassifierI
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, NuSVC


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


def classify(trainfeats, testfeats):
    print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

    my_classifier = NaiveBayesClassifier.train(trainfeats)
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = my_classifier.classify(feats)
        testsets[observed].add(i)

    print('accuracy:', nltk.classify.util.accuracy(my_classifier, testfeats))
    print('pos precision:', precision(refsets['pos'], testsets['pos']))
    print('pos recall:', recall(refsets['pos'], testsets['pos']))
    print('pos F-measure:', f_measure(refsets['pos'], testsets['pos']))
    print('neg precision:', precision(refsets['neg'], testsets['neg']))
    print('neg recall:', recall(refsets['neg'], testsets['neg']))
    print('neg F-measure:', f_measure(refsets['neg'], testsets['neg']))
    my_classifier.show_most_informative_features()



    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier._vectorizer.sort = False
    MNB_classifier.train(trainfeats)
    print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testfeats)) * 100)
    # mnb = (nltk.classify.accuracy(MNB_classifier, testfeats)) * 100
    # mnb = round(mnb, 1)

    BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    BernoulliNB_classifier._vectorizer.sort = False
    BernoulliNB_classifier.train(trainfeats)
    print("BernoulliNB_classifier accuracy percent:",
          (nltk.classify.accuracy(BernoulliNB_classifier, testfeats)) * 100)
    # bnb = (nltk.classify.accuracy(BernoulliNB_classifier, testfeats)) * 100
    # bnb = round(bnb, 1)

    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier._vectorizer.sort = False
    LogisticRegression_classifier.train(trainfeats)
    print("LogisticRegression_classifier accuracy percent:",
          (nltk.classify.accuracy(LogisticRegression_classifier, testfeats)) * 100)
    # lr = (nltk.classify.accuracy(LogisticRegression_classifier, testfeats)) * 100
    # lr = round(lr, 1)

    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier._vectorizer.sort = False
    LinearSVC_classifier.train(trainfeats)
    print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testfeats)) * 100)
    # lsvc = (nltk.classify.accuracy(LinearSVC_classifier, testfeats)) * 100
    # lsvc = round(lsvc, 1)

    NuSVC_classifier = SklearnClassifier(NuSVC())
    NuSVC_classifier._vectorizer.sort = False
    NuSVC_classifier.train(trainfeats)
    print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testfeats)) * 100)
    # nsvc = (nltk.classify.accuracy(NuSVC_classifier, testfeats)) * 100
    # lsvc = round(lsvc, 1)

    voted_classifier = VoteClassifier(
        NuSVC_classifier,
        LinearSVC_classifier,
        MNB_classifier,
        BernoulliNB_classifier,
        LogisticRegression_classifier)

    print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testfeats)) * 100)
    # voted = (nltk.classify.accuracy(voted_classifier, testfeats)) * 100
    # voted = round(voted, 1)

    # return (str(nb) + ", " + str(mnb) + ", " + str(bnb) + ", " + str(lr) + ", " + str(lsvc) + ", " + str(nsvc) + ", " + str(voted) + "\n")