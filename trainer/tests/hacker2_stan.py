import collections
import nltk.metrics
import settings
from nltk.metrics import precision, recall, f_measure
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords

import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures


stanford_pos = settings.TRAINER_DATA + "/twitter/stanford_pos_5000.csv"
stanford_neg = settings.TRAINER_DATA + "/twitter/stanford_neg_5000.csv"


def evaluate_classifier(featx):

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


    negfeats = [(featx(nltk.word_tokenize(line)), 'neg') for line in stanford_n]
    posfeats = [(featx(nltk.word_tokenize(line)), 'pos') for line in stanford_p]

    negcutoff = int(len(negfeats) * 3 / 4)
    poscutoff = int(len(posfeats) * 3 / 4)

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

    classifier = NaiveBayesClassifier.train(trainfeats)
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)

    print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
    print('pos precision:', precision(refsets['pos'], testsets['pos']))
    print('pos recall:', recall(refsets['pos'], testsets['pos']))
    print('pos F-measure:', f_measure(refsets['pos'], testsets['pos']))
    print('neg precision:', precision(refsets['neg'], testsets['neg']))
    print('neg recall:', recall(refsets['neg'], testsets['neg']))
    print('neg F-measure:', f_measure(refsets['neg'], testsets['neg']))
    classifier.show_most_informative_features(15)

####

def word_feats(words):
    return dict([(word, True) for word in words])

evaluate_classifier(word_feats)

####

stopset = set(stopwords.words('english'))
def stopword_filtered_word_feats(words):
    return dict([(word, True) for word in words if word not in stopset])

# evaluate_classifier(stopword_filtered_word_feats)

####

def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

# evaluate_classifier(bigram_word_feats)