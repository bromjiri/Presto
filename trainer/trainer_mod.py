import trainer.dataset as ds
import random
import nltk

import datetime
from statistics import mode

from nltk.classify import ClassifierI
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, NuSVC


output_file = "output.txt"
output = open(output_file, 'a')


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

def get_feature_set(dataset, common_count=None):

    all_grams = dataset.get_common_grams()

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


def run_classifiers(training_set, testing_set):



    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
    # classifier.show_most_informative_features(20)
    nb = (nltk.classify.accuracy(classifier, testing_set)) * 100
    nb = round(nb, 1)

    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier._vectorizer.sort = False
    MNB_classifier.train(training_set)
    print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)
    mnb = (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100
    mnb = round(mnb, 1)

    BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    BernoulliNB_classifier._vectorizer.sort = False
    BernoulliNB_classifier.train(training_set)
    print("BernoulliNB_classifier accuracy percent:",
          (nltk.classify.accuracy(BernoulliNB_classifier, testing_set)) * 100)
    bnb = (nltk.classify.accuracy(BernoulliNB_classifier, testing_set)) * 100
    bnb = round(bnb, 1)

    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier._vectorizer.sort = False
    LogisticRegression_classifier.train(training_set)
    print("LogisticRegression_classifier accuracy percent:",
          (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)
    lr = (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100
    lr = round(lr, 1)

    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier._vectorizer.sort = False
    LinearSVC_classifier.train(training_set)
    print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)
    lsvc = (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100
    lsvc = round(lsvc, 1)

    NuSVC_classifier = SklearnClassifier(NuSVC())
    NuSVC_classifier._vectorizer.sort = False
    NuSVC_classifier.train(training_set)
    print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set)) * 100)
    nsvc = (nltk.classify.accuracy(NuSVC_classifier, testing_set)) * 100
    lsvc = round(lsvc, 1)

    voted_classifier = VoteClassifier(
        NuSVC_classifier,
        LinearSVC_classifier,
        MNB_classifier,
        BernoulliNB_classifier,
        LogisticRegression_classifier)

    print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set)) * 100)
    voted = (nltk.classify.accuracy(voted_classifier, testing_set)) * 100
    voted = round(voted, 1)

    output.write(str(nb) + ", " + str(mnb) + ", " + str(bnb) + ", " + str(lr) + ", " + str(lsvc) + ", " + str(nsvc) + ", " + str(voted) + "\n")
    output.flush()



COUNT = 2000

if __name__ == '__main__':

    pos_array = [["J", "V", "N", "R"]]
    stop_array = [False]
    stem_array = [True, False]
    bigram_array = [True, False]

    # pos_array = [None, ["J", "V", "N", "R"]]
    # stop_array = [False, True]
    # stem_array = [False, True]
    # bigram_array = [True, True]



    output.write(str(datetime.datetime.today()) + "\n")
    output.write("all_grams, common_grams, nb, mnb, bnb, lr, lsvc, nsvc, voted\n")


    for pos in pos_array:
        for stop in stop_array:
            for stem in stem_array:
                for bigram in bigram_array:

                    output.write(str(datetime.datetime.today()) + "\n")
                    print("pos=" + str(pos) + ", stop=" + str(stop) + ", stem=" + str(stem) + ", bigram=" + str(bigram))
                    output.write("pos=" + str(pos) + ", stop=" + str(stop) + ", stem=" + str(stem) + ", bigram=" + str(bigram) + "\n")

                    for x in range(0,5):

                        stanford_set = ds.Dataset("stanford", count=COUNT)

                        stanford_set.create_grams(pos=pos, stop=stop, stem=stem, bigram=bigram, lower=True)
                        print("all_grams: " + str(stanford_set.get_grams_count()))
                        output.write(str(stanford_set.get_grams_count()) + ", ")

                        feature_set = get_feature_set(stanford_set, 10000)
                        print("common_grams: " + str(len(feature_set[0][0])))
                        output.write(str(len(feature_set[0][0])) + ", ")

                        training_set = feature_set[:round(COUNT * 8 / 10)]
                        testing_set = feature_set[round(COUNT * 8 / 10):]
                        run_classifiers(training_set, testing_set)

    #
    #
    # stanford_set = ds.Dataset("stanford", count=COUNT)
    # stanford_set.create_grams(pos=["J", "V", "N", "R"], stop=True, stem=True, bigram=True, lower=False)
    # # stanford_set.create_grams(pos=["J", "V", "N", "R"], stop=True, stem=True, bigram=True)
    # feature_set = get_feature_set(stanford_set)
    #
    # print(len(feature_set))
    # print("feature_set loaded")
    #
    # training_set = feature_set[:round(COUNT*8/10)]
    # testing_set = feature_set[round(COUNT*8/10):]
    #
    # run_classifiers(training_set, testing_set)


