import settings
import random
import nltk
import csv
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.util import ngrams

kaggle_path = settings.TRAINER_DATA + "/twitter/kaggle_full.txt"
marino_path = settings.TRAINER_DATA + "/twitter/marino_full.arff"
sanders_path = settings.TRAINER_DATA + "/twitter/sanders_full.csv"
stanford_pos = settings.TRAINER_DATA + "/twitter/stanford_pos_5000.csv"
stanford_neg = settings.TRAINER_DATA + "/twitter/stanford_neg_5000.csv"
bull_nflx = settings.TRAINER_DATA + "/stwits/bull_spx.csv"
bear_nflx = settings.TRAINER_DATA + "/stwits/bear_spx.csv"


class Sentence:
    original = ""
    sentiment = ""
    grams = list()

    def __init__(self):
        self.original = ""
        self.sentiment = ""
        self.grams = list()

    def print_grams(self):
        print(self.grams)

    @staticmethod
    def filter_lower(words):
        words_lower = list()
        for w in words:
            words_lower.append(w.lower())

        return words_lower

    @staticmethod
    def filter_bigram(words):
        bigrams = ngrams(words, 2)
        words_bigram = list()
        for w in words:
            words_bigram.append(w)

        for b in bigrams:
            words_bigram.append(b)

        return words_bigram

    @staticmethod
    def filter_stem(words):
        ps = PorterStemmer()
        words_stem = list()
        for w in words:
            words_stem.append(ps.stem(w.lower()))

        return words_stem

    @staticmethod
    def filter_stop(words):
        stop_words = set(stopwords.words('english'))
        words_stop = list()
        for w in words:
            if w not in stop_words:
                words_stop.append(w)

        return words_stop

    @staticmethod
    def filter_pos(words, allowed_types):

        pos = nltk.pos_tag(words)
        words_pos = list()
        for p in pos:
            if p[1][0] in allowed_types:
                words_pos.append(p[0])

        return words_pos


def create_grams(pos, stop, stem, bigram, lower, sentence):

    words = nltk.word_tokenize(sentence)

    # part-of-speech
    if pos is not None:
        words = Sentence.filter_pos(words, pos)
    # stopwords
    if stop is True:
        words = Sentence.filter_stop(words)
    # stemming
    if stem is True:
        words = Sentence.filter_stem(words)
    # lower
    if lower is True:
        words = Sentence.filter_lower(words)
    # bigrams
    if bigram is True:
        words = Sentence.filter_bigram(words)



    return words


class Dataset:
    sentence_list = list()
    all_grams = list()

    def __init__(self, source=None, count=-1):
        self.sentence_list = list()
        self.all_grams = list()
        source = str(source)

        if source is None:
            pass
        elif source == "kaggle":
            self.sentence_list = self.read_kaggle()
        elif source == "sanders":
            self.sentence_list = self.read_sanders()
        elif source == "stanford":
            self.sentence_list = self.read_stanford(count)
        elif source == "stwits":
            self.sentence_list = self.read_stwits(count)
        elif source == "marino":
            self.sentence_list = self.read_marino(count)

    def __exit__(self, *err):
        self.close()

    def create_grams(self, pos, stop, stem, bigram, lower):

        for sentence in self.sentence_list:

            sentence.grams = create_grams(pos, stop, stem, bigram, lower, sentence.original)

            # add to all_grams
            for g in sentence.grams:
                self.all_grams.append(g)

    def get_grams_count(self):
        return len(self.all_grams)

    def get_sentence_list(self):
        return self.sentence_list

    def get_common_grams(self, count=None):
        numbered_grams = nltk.FreqDist(self.all_grams).most_common(count)
        common_grams = list()
        for gram in numbered_grams:
            common_grams.append(gram[0])
        return common_grams

    def print_content(self, count):
        for sentence in self.sentence_list[:count]:
            print(sentence.original)
            print(sentence.sentiment)
            print(sentence.grams)

    @staticmethod
    def read_marino(count):

        sentence_list = list()
        with open(marino_path, 'r') as marino:
            for line in marino:
                if line[0] == "0":
                    sentence = Sentence()
                    sentence.original = line[3:-2]
                    sentence.sentiment = 0
                    sentence_list.append(sentence)
                elif line[0] == "4":
                    sentence = Sentence()
                    sentence.original = line[3:-2]
                    sentence.sentiment = 4
                    sentence_list.append(sentence)


        random.schuffle(sentence_list)
        return sentence_list[:count]

    @staticmethod
    def read_stwits(count):

        sentence_list = list()
        with open(bull_nflx, 'r') as bull:
            for line in bull:
                sentence = Sentence()
                sentence.original = line.strip()
                sentence.sentiment = 4
                sentence_list.append(sentence)

        with open(bear_nflx, 'r') as bear:
            for line in bear:
                sentence = Sentence()
                sentence.original = line.strip()
                sentence.sentiment = 0
                sentence_list.append(sentence)

        random.shuffle(sentence_list)

        return sentence_list[:count]

    @staticmethod
    def read_stanford(count):

        sentence_list_pos = list()
        sentence_list_neg = list()
        sentence_list = list()
        with open(stanford_pos, 'r') as stanford_p:
            for line in stanford_p:
                sentence = Sentence()
                sentence.original = line.strip()
                sentence.sentiment = 4
                sentence_list_pos.append(sentence)

        with open(stanford_neg, 'r') as stanford_n:
            for line in stanford_n:
                sentence = Sentence()
                sentence.original = line.strip()
                sentence.sentiment = 0
                sentence_list_neg.append(sentence)

        if count != -1:
            sentence_list = sentence_list_pos[:int(count/2)] + sentence_list_neg[:int(count/2)]
        else:
            sentence_list = sentence_list_pos + sentence_list_neg

        random.shuffle(sentence_list)

        return sentence_list

    @staticmethod
    def read_kaggle():
        kaggle = open(kaggle_path)

        sentence_list = list()
        for line in kaggle:
            parts = line.split('\t')
            if parts[0] == "1":
                category = "4"
            else:
                category = "0"

            sentence = Sentence()
            sentence.original = parts[1].strip()
            sentence.sentiment = category
            sentence_list.append(sentence)
        return sentence_list

    @staticmethod
    def read_sanders():
        with open(sanders_path, "r") as sanders:
            reader = csv.reader(sanders, delimiter=',')
            sentence_list = list()
            for row in reader:
                try:

                    if row[1] == "positive":
                        sentiment = "4"
                    elif row[1] == "negative":
                        sentiment = "0"
                    else:
                        sentiment = "2"
                    sentence = Sentence()
                    sentence.original = row[4]
                    sentence.sentiment = sentiment
                    sentence_list.append(sentence)
                except:
                    pass

            return sentence_list


if __name__ == '__main__':
    # kaggle_set = Dataset("kaggle")

    # kaggle_set.create_grams(pos=["J", "V"],stem=True, bigram=True)

    # kaggle_set.create_grams(pos=["J", "V", "N", "R"], stop=True, stem=True, bigram=True)
    # kaggle_set.create_grams(pos=None, stop=False, stem=False, bigram=True)

    # kaggle_set.do_pos(["J", "V"])
    # kaggle_set.print_content()

    # kaggle_set.print_content(10)
    # common_grams = kaggle_set.get_common_grams(10)
    # print(common_grams)

    my_set = Dataset("stanford", 100)
    my_set.create_grams(pos=None, stop=True, stem=False, bigram=True, lower=False)
    my_set.print_content(-1)