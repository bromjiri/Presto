import trainer.classifier_load as cls

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures


class Features:


    @staticmethod
    def find_features(tweet, bigram_count=1, pos=None, stop=False, stem=False, bigram=True, lower=True):

        words = nltk.word_tokenize(tweet)
        # print(words)

        unigrams = Features.create_unigrams(pos, stop, stem, lower, words)
        # print(unigrams)

        features = Features.create_features(bigram_count, unigrams)
        # print(features)

        return features

    @staticmethod
    def create_unigrams(pos, stop, stem, lower, words):

        # if pos != None:
        #     words = Features.filter_pos(words, pos)
        if stem:
            words = Features.filter_stem(words)
        if lower:
            words = Features.filter_lower(words)
        # if stop:
        #     words = Features.filter_stop(words)

        return words

    @staticmethod
    def create_features(bigram_count, words):

        score_fn = BigramAssocMeasures.chi_sq
        bigram_finder = BigramCollocationFinder.from_words(words)
        bigrams = bigram_finder.nbest(score_fn, bigram_count)
        d = dict([(bigram, True) for bigram in bigrams])
        d.update(dict([(word, True) for word in words]))
        return d

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
    def filter_stem(words):

        ps = PorterStemmer()
        words_stem = list()
        for w in words:
            try:
                words_stem.append(ps.stem(w))
            except:
                continue
        return words_stem


    @staticmethod
    def filter_pos(words, disallowed_types):

        pos = nltk.pos_tag(words)
        words_pos = list()
        for p in pos:
            if p[1] not in disallowed_types:
                words_pos.append(p[0])

        return words_pos


def sent_twitter(text):
    features = Features.find_features(text, stem=True, bigram_count=5)
    return cls.classify(features, "twitter", "4k-75.6-full")


def sent_stwits(text):
    features = Features.find_features(text, bigram_count=5)
    return cls.classify(features, "stwits", "20k-77.6-full")


if __name__ == '__main__':

    sent, conf = sent_twitter("Samsung is rumored to have plans of reintroducing the Note series with the Galaxy Note 8.")
    print(sent, conf)