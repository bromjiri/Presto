import trainer.corpora as corp

import random
import nltk
import itertools
import pickle

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist


class Features:
    total = 0
    inf_count = 0
    bigram_count = 0
    total_word_count = 0
    unigrams_pos = list()
    unigrams_neg = list()
    features_pos = list()
    features_neg = list()
    bestwords = list()

    def __init__(self, corpora, total, inf_count=-1, bigram_count=50, pos=None, stop=False, stem="none", bigram=False, lower=True):
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

        if pos != None:
            words = Features.filter_pos(words, pos)
        if stem != "none":
            words = Features.filter_stem(words, stem)
        if lower:
            words = Features.filter_lower(words)
        if stop:
            words = Features.filter_stop(words)
        return words

    def create_features(self, bigram, words, ):

        b_count = round(len(words) * self.bigram_count)

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

        # inf_limit = round(len(word_scores.items()) * self.inf_count)
        # print("inf_count:" + str(self.inf_count))
        # print("total: " + str(len(word_scores.items())))
        # print("limit: " + str(inf_limit))

        best = sorted(word_scores.items(), key=lambda tup: tup[1], reverse=True)[:self.inf_count]
        bestwords = set([w for w, s in best])
        self.bestwords = bestwords

    @staticmethod
    def filter_stop(words):
        stop_words = set(stopwords.words('english'))
        words_stop = list()
        for w in words:
            if w not in stop_words:
                words_stop.append(w)

        return words_stop

    @staticmethod
    def filter_lower(words):
        words_lower = list()
        for w in words:
            words_lower.append(w.lower())
        return words_lower

    @staticmethod
    def filter_stem(words, stem):

        if stem == "porter":
            ps = PorterStemmer()
            words_stem = list()
            for w in words:
                try:
                    words_stem.append(ps.stem(w))
                except:
                    continue
            return words_stem
        elif stem == "lemma":
            lm = WordNetLemmatizer()
            words_stem = list()
            for w in words:
                words_stem.append(lm.lemmatize(w))
            return  words_stem

    @staticmethod
    def filter_pos(words, disallowed_types):

        pos = nltk.pos_tag(words)
        words_pos = list()
        for p in pos:
            if p[1][0] in disallowed_types:
                words_pos.append(p[0])

        return words_pos

    def get_features_pos(self):
        return self.features_pos

    def get_fearures_neg(self):
        return self.features_neg

    def print_features_pos(self):
        for feature in self.features_pos:
            print(feature)


if __name__ == '__main__':

    COUNT = 5000
    cut = int((COUNT/2)*3/4)

    crp = corp.Corpora("stanford", count=COUNT)
    ftr = Features(crp, total=COUNT, bigram=True, stem="porter", pos=["CD"])
    ftr.print_features_pos()
