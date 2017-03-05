import settings
from nltk.corpus import movie_reviews
import random

stanford_pos = settings.TRAINER_DATA + "/twitter/stanford_pos_20k.csv"
stanford_neg = settings.TRAINER_DATA + "/twitter/stanford_neg_20k.csv"
stwits_pos = settings.TRAINER_DATA + "/stwits/stwits_pos_the.csv"
stwits_neg = settings.TRAINER_DATA + "/stwits/stwits_neg_the.csv"
news_pos = settings.TRAINER_DATA + "/news/news_pos_mix.csv"
news_neg = settings.TRAINER_DATA + "/news/news_neg_mix.csv"


class Corpora:
    lines_pos = list()
    lines_neg = list()

    def __init__(self, source, count=-1, shuffle = False):
        self.lines_neg = list()
        self.lines_pos = list()

        pos_list = list()
        neg_list = list()

        if source is None:
            pass
        elif source == "stanford":
            pos_list, neg_list = self.read_stanford(shuffle)
        elif source == "stwits":
            pos_list, neg_list = self.read_stwits(shuffle)
        elif source == "news":
            pos_list, neg_list = self.read_news(shuffle)
        elif source == "movie":
            pos_list, neg_list = self.read_movie()

        if count == -1:
            self.lines_pos = pos_list
            self.lines_neg = neg_list
        else:
            cut = int((count / 2) + 1)
            self.lines_pos = pos_list[:cut]
            self.lines_neg = neg_list[:cut]

    def get_lines_pos(self, count=-1):
        if count == -1:
            return self.lines_pos
        else:
            return self.lines_pos[:count]

    def get_lines_neg(self, count=-1):
        if count == -1:
            return self.lines_neg
        else:
            return self.lines_neg[:count]

    def print_lines_pos(self, count=-1):
        for line in self.lines_pos[:count]:
            print(line)

    def print_lines_neg(self, count=-1):
        for line in self.lines_neg[:count]:
            print(line)

    # @staticmethod
    def read_stanford(self, shuffle):

        stanford_pos_list = list()
        with open(stanford_pos, 'r') as stanford_p:
            for line in stanford_p:
                stanford_pos_list.append(line.strip())

        stanford_neg_list = list()
        with open(stanford_neg, 'r') as stanford_n:
            for line in stanford_n:
                stanford_neg_list.append(line.strip())

        if shuffle:
            random.shuffle(stanford_pos_list)
            random.shuffle(stanford_neg_list)

        return stanford_pos_list, stanford_neg_list

    def read_stwits(self, shuffle):

        stwits_pos_list = list()
        with open(stwits_pos, 'r') as bull:
            for line in bull:
                stwits_pos_list.append(line.strip())

        stwits_neg_list = list()
        with open(stwits_neg, 'r') as bear:
            for line in bear:
                stwits_neg_list.append(line.strip())

        if shuffle:
            random.shuffle(stwits_pos_list)
            random.shuffle(stwits_neg_list)

        return stwits_pos_list, stwits_neg_list

    def read_news(self, shuffle):

        news_pos_list = list()
        with open(news_pos, 'r') as n_pos:
            for line in n_pos:
                news_pos_list.append(line.strip())

        news_neg_list = list()
        with open(news_neg, 'r') as n_neg:
            for line in n_neg:
                news_neg_list.append(line.strip())

        if shuffle:
            random.shuffle(news_pos_list)
            random.shuffle(news_neg_list)

        return news_pos_list, news_neg_list

    def read_movie(self):

        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')

        for f in negids:
            self.lines_neg.append(movie_reviews.words(f))

        for f in posids:
            self.lines_pos.append(movie_reviews.words(f))

if __name__ == '__main__':
    corp = Corpora("stwits", shuffle=True)
    for line in corp.get_lines_neg(100):
        print(line)