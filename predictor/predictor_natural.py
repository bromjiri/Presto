import settings
import pandas as pd
import numpy as np
import os
from datetime import datetime
from datetime import timedelta
import trainer.classifier_test as cls
import random
import nltk


class Stock:

    def __init__(self, subject):
        input_file = settings.PREDICTOR_STOCK + "/" + subject + ".csv"
        self.stock_df = pd.read_csv(input_file, sep=',', index_col='Date')

    def create_dict(self, from_date, to_date):
        stock_ser = self.stock_df['Diff'].loc[from_date:to_date]

        # binning
        stock_ser = stock_ser.apply(func)

        self.stock_dict = stock_ser.dropna().astype(int).to_dict()
        print(sorted(self.stock_dict.items()))

    def get_dict(self):
        return self.stock_dict


class Sent:

    def __init__(self, subject, source):
        input_file = settings.PREDICTOR_SENTIMENT + "/" + source + "/" + source + "-sent-" + subject + ".csv"
        self.sent_df = pd.read_csv(input_file, sep=',', index_col='Date')

    def create_dict(self, precision, from_date, to_date):
        sentiment_col = "Sent" + precision
        sent_ser = self.sent_df[sentiment_col].diff().loc[from_date:to_date]

        # binning
        sent_ser = sent_ser.apply(func)

        self.sent_dict = sent_ser.dropna().astype(int).to_dict()
        print(sorted(self.sent_dict.items()))

    def get_features(self, date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d")

        features = dict()
        features['d1'] = self.sent_dict[str(date.date() - timedelta(days=3))]
        features['d2'] = self.sent_dict[str(date.date() - timedelta(days=2))]
        features['d3'] = self.sent_dict[str(date.date() - timedelta(days=1))]
        return features


def func(row):

    if row > 0:
        return 4
    elif row < 0:
        return 0
    else:
        return row


def run_one(source, subject, from_date, to_date, precision):

    # stock dataframe
    stock = Stock(subject)
    stock.create_dict(from_date, to_date)
    stock_dict = stock.get_dict()

    # sentiment dataframe
    sent = Sent(subject, source)
    sent.create_dict(precision, from_date, to_date)

    features_list = list()
    for key in sorted(stock_dict)[3:]:
        features = sent.get_features(key)
        features_list.append([features, stock_dict[key]])

    output_dir_path = settings.PREDICTOR_PREDICTION + '/' + source + '/' + subject
    os.makedirs(output_dir_path, exist_ok=True)
    output_file_path = output_dir_path + '/' + source + '-prediction-' + subject + '-' + precision + '-' + method + '.csv'
    output_file = open(output_file_path, 'w')

    for x in range(0, 50):

        random.shuffle(features_list)
        # print(len(features_list))

        trainfeats = features_list[:170]
        testfeats = features_list[170:]

        nlt_output, skl_output = cls.train(trainfeats, testfeats, nlt=nltk_run, skl=sklearn_run)

        classifier = nltk.NaiveBayesClassifier.train(trainfeats)
        print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testfeats)) * 100)
        classifier.show_most_informative_features(1)

        if nltk_run:
            print(str(nlt_output))
            output_file.write(nlt_output)
            # nlt[var_name].flush()
        if sklearn_run:
            print(str(skl_output))
            output_file.write(skl_output)
            # skl[var_name].flush()


nltk_run = False
sklearn_run = True

from_date = '2016-11-01'
to_date = '2017-08-31'
source = "stwits"
subjects = ["tesla"]
precisions = ["0.6", "0.8" , "1.0"]
method = 'natural'

for precision in precisions:
    for subject in subjects:
        print(subject, precision)
        run_one(source, subject, from_date, to_date, precision)
