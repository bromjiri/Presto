import nltk
import collections
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import precision, recall, f_measure
import datetime
import pickle
from statistics import mode

import trainer.corpora as crp
import trainer.features as ftr

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


def train(trainfeats, testfeats, nlt = True, skl = True, most = 0):
    # print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

    nltk_output = "none"
    sklearn_output = "none"

    if nlt:

        my_classifier = NaiveBayesClassifier.train(trainfeats)
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)

        for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed = my_classifier.classify(feats)
            testsets[observed].add(i)

        # precision and recall
        accuracy = nltk.classify.util.accuracy(my_classifier, testfeats) * 100
        pos_prec = precision(refsets['pos'], testsets['pos']) * 100
        pos_rec = recall(refsets['pos'], testsets['pos']) * 100
        neg_prec = precision(refsets['neg'], testsets['neg']) * 100
        neg_rec = recall(refsets['neg'], testsets['neg']) * 100

        # round
        accuracy = round(accuracy, 1)
        pos_prec = round(pos_prec, 1)
        pos_rec = round(pos_rec, 1)
        neg_prec = round(neg_prec, 1)
        neg_rec = round(neg_rec, 1)

        # print('pos F-measure:', f_measure(refsets['pos'], testsets['pos']))
        # print('neg F-measure:', f_measure(refsets['neg'], testsets['neg']))
        my_classifier.show_most_informative_features(most)

        nltk_output = "nlt, " + str(accuracy) + ", " + str(pos_prec) + ", " + str(neg_prec) + ", " + str(
            pos_rec) + ", " + str(neg_rec) + "\n"

    if skl:

        MNB_classifier = SklearnClassifier(MultinomialNB())
        MNB_classifier._vectorizer.sort = False
        MNB_classifier.train(trainfeats)
        mnb = (nltk.classify.accuracy(MNB_classifier, testfeats)) * 100
        mnb = round(mnb, 1)
        print(mnb)

        BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
        BernoulliNB_classifier._vectorizer.sort = False
        BernoulliNB_classifier.train(trainfeats)
        bnb = (nltk.classify.accuracy(BernoulliNB_classifier, testfeats)) * 100
        bnb = round(bnb, 1)
        print(bnb)

        LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
        LogisticRegression_classifier._vectorizer.sort = False
        LogisticRegression_classifier.train(trainfeats)
        lr = (nltk.classify.accuracy(LogisticRegression_classifier, testfeats)) * 100
        lr = round(lr, 1)
        print(lr)

        LinearSVC_classifier = SklearnClassifier(LinearSVC())
        LinearSVC_classifier._vectorizer.sort = False
        LinearSVC_classifier.train(trainfeats)
        lsvc = (nltk.classify.accuracy(LinearSVC_classifier, testfeats)) * 100
        lsvc = round(lsvc, 1)
        print(lsvc)

        NuSVC_classifier = SklearnClassifier(NuSVC())
        NuSVC_classifier._vectorizer.sort = False
        NuSVC_classifier.train(trainfeats)
        nsvc = (nltk.classify.accuracy(NuSVC_classifier, testfeats)) * 100
        nsvc = round(nsvc, 1)
        print(nsvc)

        voted_classifier = VoteClassifier(
            NuSVC_classifier,
            LinearSVC_classifier,
            MNB_classifier,
            BernoulliNB_classifier,
            LogisticRegression_classifier)
        voted = (nltk.classify.accuracy(voted_classifier, testfeats)) * 100
        voted = round(voted, 1)
        print(voted)

        sklearn_output = "skl, " + str(mnb) + ", " + str(bnb) + ", " + str(lr) + ", " + str(lsvc) + ", " + str(nsvc) + ", " + str(voted) + "\n"


    return (nltk_output, sklearn_output)



if __name__ == '__main__':
    COUNT = 5000
    cut = int((COUNT/2)*3/4)

    corpora = crp.Corpora("news", count=COUNT, shuffle=True)
    features = ftr.Features(corpora, total=COUNT, bigram=False, pos=["J", "V", "N", "R"])
    features = ftr.Features(corpora, total=COUNT, bigram=False, stem="porter")

    posfeats = features.get_features_pos()
    negfeats = features.get_fearures_neg()

    trainfeats = negfeats[:cut] + posfeats[:cut]
    testfeats = negfeats[cut:] + posfeats[cut:]

    print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))
    nlt, skl = train(trainfeats, testfeats, skl=False, most=50)
    print(nlt, skl)