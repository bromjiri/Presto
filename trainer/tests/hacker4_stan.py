import collections
import nltk.metrics
from nltk.metrics import precision, recall, f_measure
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords

import settings
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

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

    stanford_p = stanford_pos_list[:5000]
    stanford_n = stanford_neg_list[:5000]

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
    classifier.show_most_informative_features()

####

def word_feats(words):
    return dict([(word.lower(), True) for word in words])

print('evaluating single word features')
evaluate_classifier(word_feats)

####

word_fd = FreqDist()
label_word_fd = ConditionalFreqDist()

negwords = list()
poswords = list()


stanford_pos_list = list()
stanford_neg_list = list()
with open(stanford_pos, 'r') as stanford_p:
    for line in stanford_p:
        stanford_pos_list.append(line.strip())

with open(stanford_neg, 'r') as stanford_n:
    for line in stanford_n:
        stanford_neg_list.append(line.strip())

stanford_p = stanford_pos_list[:3750]
stanford_n = stanford_neg_list[:3750]

for line in stanford_p:
    for word in nltk.word_tokenize(line):
        poswords.append(word)

for line in stanford_n:
    for word in nltk.word_tokenize(line):
        negwords.append(word)


for word in negwords:
    word_fd[word.lower()] += 1
    label_word_fd['pos'][word.lower()] += 1

for word in poswords:
    word_fd[word.lower()] += 1
    label_word_fd['neg'][word.lower()] += 1

# n_ii = label_word_fd[label][word]
# n_ix = word_fd[word]
# n_xi = label_word_fd[label].N()
# n_xx = label_word_fd.N()

pos_word_count = label_word_fd['pos'].N()
neg_word_count = label_word_fd['neg'].N()
total_word_count = pos_word_count + neg_word_count

word_scores = {}

for word, freq in word_fd.items():
    pos_score = BigramAssocMeasures.chi_sq(label_word_fd['pos'][word],
                                           (freq, pos_word_count), total_word_count)
    neg_score = BigramAssocMeasures.chi_sq(label_word_fd['neg'][word],
                                           (freq, neg_word_count), total_word_count)
    word_scores[word] = pos_score + neg_score

best = sorted(word_scores.items(), key=lambda tup: tup[1], reverse=True)[:7000]
bestwords = set([w for w, s in best])


def best_word_feats(words):
    return dict([(word.lower(), True) for word in words if word in bestwords])


print('evaluating best word features')
evaluate_classifier(best_word_feats)


def best_bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    d = dict([(bigram, True) for bigram in bigrams])
    d.update(best_word_feats(words))
    return d


print('evaluating best words + bigram chi_sq word features')
evaluate_classifier(best_bigram_word_feats)