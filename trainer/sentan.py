import trainer.classifier_load as cls

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures


class Features:

    @staticmethod
    def find_features(tweet, pos=["CD"], stop=False, stem="porter", bigram=True, lower=True):

        words = nltk.word_tokenize(tweet)
        print(words)

        unigrams = Features.create_unigrams(pos, stop, stem, lower, words)
        print(unigrams)

        features = Features.create_features(bigram, unigrams)
        print(features)

        return features

    @staticmethod
    def create_unigrams(pos, stop, stem, lower, words):

        if pos != None:
            words = Features.filter_pos(words, pos)
        if stem != "none":
            words = Features.filter_stem(words, stem)
        if lower:
            words = Features.filter_lower(words)
        if stop:
            words = Features.filter_stop(words)

        return words

    @staticmethod
    def create_features(bigram, words):

        b_count = round(len(words))

        # create dictionaries
        if not bigram:
            return dict([(word, True) for word in words])

        if bigram:
            score_fn = BigramAssocMeasures.chi_sq
            bigram_finder = BigramCollocationFinder.from_words(words)
            bigrams = bigram_finder.nbest(score_fn, b_count)
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
            if p[1] not in disallowed_types:
                words_pos.append(p[0])

        return words_pos


def sent_twitter(text):
    features = Features.find_features(text)
    return cls.classify(features, "twitter", "60000")


if __name__ == '__main__':

    sent, conf = sent_twitter("Microsoft software is constantly being targeted by cyber criminals.")
    print(sent, conf)