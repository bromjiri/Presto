import nltk
import collections
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import precision, recall, f_measure
import datetime
import pickle
from statistics import mode
import os

from nltk.classify import ClassifierI

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


def classify(features, source, type):
    dir_path = os.path.dirname(__file__)

    file_path = os.path.join(dir_path, source + '/pickled/' + type + '/MNB_classifier.pickle')
    open_file = open(file_path, "rb")
    MNB_classifier = pickle.load(open_file)
    open_file.close()

    file_path = os.path.join(dir_path, source + '/pickled/' + type + '/BernoulliNB_classifier.pickle')
    open_file = open(file_path, "rb")
    BernoulliNB_classifier = pickle.load(open_file)
    open_file.close()

    file_path = os.path.join(dir_path, source + '/pickled/' + type + '/LogisticRegression_classifier.pickle')
    open_file = open(file_path, "rb")
    LogisticRegression_classifier = pickle.load(open_file)
    open_file.close()

    file_path = os.path.join(dir_path, source + '/pickled/' + type + '/LinearSVC_classifier.pickle')
    open_file = open(file_path, "rb")
    LinearSVC_classifier = pickle.load(open_file)
    open_file.close()

    file_path = os.path.join(dir_path, source + '/pickled/' + type + '/NuSVC_classifier.pickle')
    open_file = open(file_path, "rb")
    NuSVC_classifier = pickle.load(open_file)
    open_file.close()

    voted_classifier = VoteClassifier(
        NuSVC_classifier,
        LinearSVC_classifier,
        MNB_classifier,
        BernoulliNB_classifier,
        LogisticRegression_classifier)

    return voted_classifier.classify(features), voted_classifier.confidence(features)


def test(trainfeats, testfeats, source, type):
    # print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

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
    my_classifier.show_most_informative_features(50)

    dir_path = os.path.dirname(__file__)

    file_path = os.path.join(dir_path, source + '/pickled/' + type + '/MNB_classifier.pickle')
    open_file = open(file_path, "rb")
    MNB_classifier = pickle.load(open_file)
    open_file.close()
    mnb = (nltk.classify.accuracy(MNB_classifier, testfeats)) * 100
    print(mnb)
    mnb = round(mnb, 1)

    file_path = os.path.join(dir_path, source + '/pickled/' + type + '/BernoulliNB_classifier.pickle')
    open_file = open(file_path, "rb")
    BernoulliNB_classifier = pickle.load(open_file)
    open_file.close()
    bnb = (nltk.classify.accuracy(BernoulliNB_classifier, testfeats)) * 100
    print(bnb)
    bnb = round(bnb, 1)

    file_path = os.path.join(dir_path, source + '/pickled/' + type + '/LogisticRegression_classifier.pickle')
    open_file = open(file_path, "rb")
    LogisticRegression_classifier = pickle.load(open_file)
    open_file.close()
    lr = (nltk.classify.accuracy(LogisticRegression_classifier, testfeats)) * 100
    print(lr)
    lr = round(lr, 1)

    file_path = os.path.join(dir_path, source + '/pickled/' + type + '/LinearSVC_classifier.pickle')
    open_file = open(file_path, "rb")
    LinearSVC_classifier = pickle.load(open_file)
    open_file.close()
    lsvc = (nltk.classify.accuracy(LinearSVC_classifier, testfeats)) * 100
    print(lsvc)
    lsvc = round(lsvc, 1)

    file_path = os.path.join(dir_path, source + '/pickled/' + type + '/NuSVC_classifier.pickle')
    open_file = open(file_path, "rb")
    NuSVC_classifier = pickle.load(open_file)
    open_file.close()
    nsvc = (nltk.classify.accuracy(NuSVC_classifier, testfeats)) * 100
    print(nsvc)
    nsvc = round(nsvc, 1)

    voted_classifier = VoteClassifier(
        NuSVC_classifier,
        LinearSVC_classifier,
        MNB_classifier,
        BernoulliNB_classifier,
        LogisticRegression_classifier)

    voted = (nltk.classify.accuracy(voted_classifier, testfeats)) * 100
    print(voted)
    voted = round(voted, 1)

    nltk_output = "nlt, " + str(accuracy) + ", " + str(pos_prec) + ", " + str(neg_prec) + ", " + str(pos_rec) + ", " + str(neg_rec) + "\n"
    sklearn_output = "skl, " + str(mnb) + ", " + str(bnb) + ", " + str(lr) + ", " + str(lsvc) + ", " + str(nsvc) + ", " + str(voted) + "\n"

    return (nltk_output, sklearn_output)


if __name__ == '__main__':
    COUNT = 60000
    cut = int((COUNT/2)*19/20)
    source = "twitter"
    type = "60000"

    # corpora = crp.Corpora("stanford", count=COUNT)
    # features = ftr.Features(corpora, total=COUNT, bigram=True, stem="porter", pos=["CD"])


    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, source + '/pickled/' + type + '/NuSVC_classifier.pickle')
    features_f = open(file_path, "rb")
    features = pickle.load(features_f)
    features_f.close()

    posfeats = features.get_features_pos()
    negfeats = features.get_fearures_neg()

    trainfeats = negfeats[:cut] + posfeats[:cut]
    testfeats = negfeats[cut:] + posfeats[cut:]

    print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))
    nlt, skl = test(trainfeats, testfeats)
    print(nlt, skl)