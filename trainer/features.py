import trainer.corpora as corp
import trainer.classifier as cls

import random
import nltk
import itertools

from nltk.stem import PorterStemmer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist


class Features:
    total = 0
    inf_count = 0
    bigram_count = 0
    unigrams_pos = list()
    unigrams_neg = list()
    features_pos = list()
    features_neg = list()
    bestwords = list()

    def __init__(self, corpora, total, inf_count=-1, bigram_count=200, pos=None, stop=False, stem=False, bigram=False, lower=True):
        self.features_pos = list()
        self.features_neg = list()
        self.unigrams_pos = list()
        self.unigrams_neg = list()
        self.total = total
        self.inf_count = inf_count
        self.bigram_count = bigram_count

        # create unigrams
        for line in corpora.get_lines_pos():
            words = nltk.word_tokenize(line)
            self.unigrams_pos.append(self.create_unigrams(pos, stop, stem, lower, words))
            # words = line

        for line in corpora.get_lines_neg():
            words = nltk.word_tokenize(line)
            self.unigrams_neg.append(self.create_unigrams(pos, stop, stem, lower, words))
            # words = line

        self.create_bestwords()

        # create features
        for unigrams in self.unigrams_pos:
            try:
                features = self.create_features(bigram, unigrams)
                self.features_pos.append((features, "pos"))
            except:
                pass

        for unigrams in self.unigrams_neg:
            try:
                features = self.create_features(bigram, unigrams)
                self.features_neg.append((features, "neg"))
            except:
                pass

    def create_unigrams(self, pos, stop, stem, lower, words):

        if lower:
            words = Features.filter_lower(words)
        if stem:
            words = Features.filter_stem(words)
        return words

    def create_features(self, bigram, words, ):

        # create dictionaries
        if not bigram:
            return dict([(word, True) for word in words if word in self.bestwords])

        if bigram:
            score_fn = BigramAssocMeasures.chi_sq
            bigram_finder = BigramCollocationFinder.from_words(words)
            bigrams = bigram_finder.nbest(score_fn, self.bigram_count)
            d = dict([(bigram, True) for bigram in bigrams])
            d.update(dict([(word, True) for word in words if word in self.bestwords]))
            return d

    def create_bestwords(self):
        word_fd = FreqDist()
        label_word_fd = ConditionalFreqDist()

        cut = int((self.total / 2) * 3 / 4)
        for unigrams in self.unigrams_pos[:cut]:
            for word in unigrams:
                word_fd[word] += 1
                label_word_fd['pos'][word] += 1

        for unigrams in self.unigrams_neg[:cut]:
            for word in unigrams:
                word_fd[word] += 1
                label_word_fd['neg'][word] += 1

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

        best = sorted(word_scores.items(), key=lambda tup: tup[1], reverse=True)[:self.inf_count]
        # print(len(best))
        bestwords = set([w for w, s in best])
        self.bestwords = bestwords

    @staticmethod
    def filter_lower(words):
        words_lower = list()
        for w in words:
            words_lower.append(w.lower())
        return words_lower

    @staticmethod
    def filter_stem(words):
        ps = PorterStemmer()
        words_stem = list()
        for w in words:
            words_stem.append(ps.stem(w))
        return words_stem

    def get_features_pos(self):
        return self.features_pos

    def get_fearures_neg(self):
        return self.features_neg

    def print_features_pos(self):
        for feature in self.features_pos:
            print(feature)


if __name__ == '__main__':
    COUNT = 15000
    cut = int((COUNT/2)*3/4)

    crp = corp.Corpora("stanford", count=COUNT)
    ftr = Features(crp, total=COUNT, bigram=True)
    # ftr.print_features_pos()

    posfeats = ftr.get_features_pos()
    negfeats = ftr.get_fearures_neg()
    # random.shuffle(posfeats)
    # random.shuffle(negfeats)

    trainfeats = negfeats[:cut] + posfeats[:cut]
    testfeats = negfeats[cut:] + posfeats[cut:]

    cls.classify(trainfeats, testfeats)