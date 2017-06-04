import nltk
import os
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
        # print(mode(votes))

        if votes.count("pos") >= 5:
            return "pos"
        elif votes.count("neg") >= 5:
            return "neg"
        else:
            return "neu"

        # return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


def get_precision(trainfeats, testfeats, my_classifier, dataset, classifier_name):

    dir = "output/" + dataset + "/algos5new/"
    os.makedirs(dir, exist_ok=True)

    file_name = dir + dataset + "-" + classifier_name + ".csv"
    output = open(file_name, 'a')
    # output.write(str(datetime.datetime.today()) + "\n")

    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    tpos = 0
    fpos = 0
    tneg = 0
    fneg = 0
    fneu = 0

    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = my_classifier.classify(feats)
        testsets[observed].add(i)

        if label == observed:
            if observed == 'pos':
                tpos += 1
            else:
                tneg += 1
        elif observed == 'pos':
            fpos += 1
        elif observed == 'neg':
            fneg += 1
        elif observed == 'neu':
            fneu += 1


    print(tpos)
    print(fpos)
    print(tneg)
    print(fneg)
    print(fneu)

    accuracy2 = round(((tpos + tneg) / (tpos + tneg + fpos + fneg)) * 100, 1)
    pos_prec2 = round((tpos / (tpos + fpos)) * 100, 1)
    pos_rec2 = round((tpos / (tpos + fneg)) * 100, 1)
    neg_prec2 = round((tneg / (tneg + fneg)) * 100, 1)
    neg_rec2 = round((tneg / (tneg + fpos)) * 100, 1)

    output_text2 = classifier_name + "-new, " + str(accuracy2) + ", " + str(pos_prec2) + ", " + str(neg_prec2) + ", " + str(
        pos_rec2) + ", " + str(neg_rec2) + "\n"
    print(output_text2)

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

    output_text = classifier_name + ", " + str(accuracy) + ", " + str(pos_prec) + ", " + str(neg_prec) + ", " + str(
        pos_rec) + ", " + str(neg_rec) + "\n"
    print(output_text)

    output.write(output_text2)
    output.flush()


def train(trainfeats, testfeats, dataset, nlt = True, skl = True, most = 0):
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
        my_classifier = MNB_classifier.train(trainfeats)
        # get_precision(trainfeats, testfeats, my_classifier, dataset, "mnb")

        # mnb = (nltk.classify.accuracy(MNB_classifier, testfeats)) * 100
        # mnb = round(mnb, 1)
        # print(mnb)

        BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
        BernoulliNB_classifier._vectorizer.sort = False
        my_classifier = BernoulliNB_classifier.train(trainfeats)
        # get_precision(trainfeats, testfeats, my_classifier, dataset, "bnb")

        # bnb = (nltk.classify.accuracy(BernoulliNB_classifier, testfeats)) * 100
        # bnb = round(bnb, 1)
        # print(bnb)

        LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
        LogisticRegression_classifier._vectorizer.sort = False
        my_classifier = LogisticRegression_classifier.train(trainfeats)
        # get_precision(trainfeats, testfeats, my_classifier, dataset, "lr")

        # lr = (nltk.classify.accuracy(LogisticRegression_classifier, testfeats)) * 100
        # lr = round(lr, 1)
        # print(lr)

        LinearSVC_classifier = SklearnClassifier(LinearSVC())
        LinearSVC_classifier._vectorizer.sort = False
        my_classifier = LinearSVC_classifier.train(trainfeats)
        # get_precision(trainfeats, testfeats, my_classifier, dataset, "lsvc")

        # lsvc = (nltk.classify.accuracy(LinearSVC_classifier, testfeats)) * 100
        # lsvc = round(lsvc, 1)
        # print(lsvc)

        NuSVC_classifier = SklearnClassifier(NuSVC())
        NuSVC_classifier._vectorizer.sort = False
        my_classifier = NuSVC_classifier.train(trainfeats)
        # get_precision(trainfeats, testfeats, my_classifier, dataset, "nsvc")

        # nsvc = (nltk.classify.accuracy(NuSVC_classifier, testfeats)) * 100
        # nsvc = round(nsvc, 1)
        # print(nsvc)

        voted_classifier = VoteClassifier(
            NuSVC_classifier,
            LinearSVC_classifier,
            MNB_classifier,
            BernoulliNB_classifier,
            LogisticRegression_classifier)
        get_precision(trainfeats, testfeats, voted_classifier, dataset, "voted")

        # voted = (nltk.classify.accuracy(voted_classifier, testfeats)) * 100
        # voted = round(voted, 1)
        # print(voted)

        # sklearn_output = "skl, " + str(mnb) + ", " + str(bnb) + ", " + str(lr) + ", " + str(lsvc) + ", " + str(nsvc) + ", " + str(voted) + "\n"
        sklearn_output = ""

    return (nltk_output, sklearn_output)



if __name__ == '__main__':
    COUNT = 5000
    cut = int((COUNT/2)*4/5)

    corpora = crp.Corpora("stwits", count=COUNT, shuffle=True)
    features = ftr.Features(corpora, total=COUNT, stem="porter", bigram=True, stop=True, inf_count=-1, lower=True)
    # features = ftr.Features(corpora, total=COUNT, bigram=True, stem="porter")

    posfeats = features.get_features_pos()
    negfeats = features.get_fearures_neg()

    trainfeats = negfeats[:cut] + posfeats[:cut]
    testfeats = negfeats[cut:] + posfeats[cut:]

    print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))
    nlt, skl = train(trainfeats, testfeats, skl=False, most=50)
    print(nlt, skl)