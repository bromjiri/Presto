import settings
import pandas as pd
import numpy as np
import os
from datetime import datetime
from datetime import timedelta
import predictor.predictor_classifier as cls
import predictor.predictor_statistic as stat
import random
import nltk


class Stock:

    def __init__(self, subject):
        input_file = settings.PREDICTOR_STOCK + "/" + subject + ".csv"
        self.stock_df = pd.read_csv(input_file, sep=',', index_col='Date')

    def create_dict(self, from_date, to_date):
        self.stock_ser = self.stock_df['Diff'].loc[from_date:to_date]

        # binning
        self.stock_ser = self.stock_ser.apply(binning_none)

        self.stock_dict = self.stock_ser.dropna().astype(int).to_dict()

    def get_dict(self):
        return self.stock_dict

    def get_stock_dates(self):
        return self.stock_ser.index.values


class Sent:

    def __init__(self, subject, source):
        input_file = settings.PREDICTOR_SENTIMENT + "/" + source + "/" + source + "-sent-" + subject + ".csv"
        self.sent_df = pd.read_csv(input_file, sep=',', index_col='Date')

    def get_weekend(self, col_name, stock_dates):

        weekend_df = np.round(self.sent_df, 2)

        aggreg = 0
        days = 1
        for idx, row in weekend_df.iterrows():
            value = row[col_name]
            date = pd.to_datetime(idx)
            date_plus = date + timedelta(days=1)
            if str(date_plus.date()) not in stock_dates:
                # print("weekend")
                value += aggreg
                aggreg = value
                days += 1
            else:
                total = value + aggreg
                mean = total / days
                aggreg = 0
                days = 1
                weekend_df.set_value(idx, col_name, mean)

            # print(date.date(), row[col_name], value)

        return np.round(weekend_df[col_name].diff().loc[stock_dates], 2)

    def create_dict(self, precision, method, from_date, to_date, stock_dates, binning):
        sentiment_col = "Sent" + precision
        sent_ser = self.sent_df[sentiment_col]

        if method == "Natural":
            sent_ser = sent_ser.diff().loc[from_date:to_date]
        elif method == "Friday":
            sent_ser = sent_ser.loc[stock_dates].diff()
        elif method == "Sunday":
            sent_ser = sent_ser.diff().loc[stock_dates]
        elif method == "Weekend":
            sent_ser = self.get_weekend(sentiment_col, stock_dates)

        # binning
        std_dev1 = sent_ser.std() / 4
        std_dev2 = sent_ser.std()

        if binning == 'none':
            sent_ser_new = sent_ser.apply(binning_none)
        elif binning == 'low':
            sent_ser_new = sent_ser.apply(binning_low, args=(std_dev1,))
        else:
            sent_ser_new = sent_ser.apply(binning_high, args=(std_dev1, std_dev2,))

        # print(pd.concat([sent_ser, sent_ser_new], axis=1))

        self.sent_dict = sent_ser_new.dropna().astype(int).to_dict()
        self.key_list = sorted(self.sent_dict.keys())

    def get_dict(self):
        return self.sent_dict

    def get_features(self, key):
        index = self.key_list.index(key)

        features = dict()
        features['d1'] = self.sent_dict[self.key_list[index-3]]
        features['d2'] = self.sent_dict[self.key_list[index-2]]
        features['d3'] = self.sent_dict[self.key_list[index-1]]
        return features


def binning_none(row):

    if row > 0:
        return 4
    elif row < 0:
        return 0
    else:
        return row


def binning_low(row, std_dev1):

    if row > std_dev1:
        return 4
    elif row < std_dev1 and row > -std_dev1:
        return 2
    elif row < -std_dev1:
        return 0
    else:
        return row


def binning_high(row, std_dev1, std_dev2):

    if row > std_dev2:
        return 4
    elif row < std_dev2 and row > std_dev1:
        return 3
    elif row < std_dev1 and row > -std_dev1:
        return 2
    elif row < -std_dev1 and row > -std_dev2:
        return 1
    elif row < -std_dev2:
        return 0
    else:
        return row


def run_one(source, subject, precision, method, from_date, to_date, binning, filename_nltk, filename_skl):

    # stock dataframe
    stock = Stock(subject)
    stock.create_dict(from_date, to_date)
    stock_dict = stock.get_dict()
    # print(sorted(stock_dict.items()))

    indexes = ["djia", "snp", "nasdaq"]
    # if subject in indexes:
    #     subject = "the"

    # sentiment dataframe
    sent = Sent(subject, source)
    sent.create_dict(precision, method, from_date, to_date, stock.get_stock_dates(), binning)
    # print(sorted(sent.get_dict().items()))

    # features
    features_list = list()
    for key in sorted(stock_dict)[3:]:
        features = sent.get_features(key)
        features_list.append([features, stock_dict[key]])
        # print([key, sorted(features.items()), stock_dict[key]])

    features_list_pos = list()
    features_list_neg = list()

    for feature in features_list:
        if feature[1] == 0:
            features_list_neg.append(feature)
        else:
            features_list_pos.append(feature)


    statistic = stat.Statistic(source, subject, precision, method, binning)

    # print(len(features_list), len(features_list_pos), len(features_list_neg))
    max_half = min(len(features_list_pos), len(features_list_neg))
    train_border = int(max_half * 4 / 5)
    # print(train_border, max_half)

    # exit()
    cycles = 50
    for x in range(0, cycles):

        random.shuffle(features_list_pos)
        random.shuffle(features_list_neg)
        # random.shuffle(features_list)

        trainfeats = features_list_pos[:train_border] + features_list_neg[:train_border]
        testfeats = features_list_pos[train_border:max_half] + features_list_neg[train_border:max_half]
        # print(len(trainfeats), len(testfeats))

        # trainfeats = features_list[:170]
        # testfeats = features_list[170:]

        nlt_output, skl_output = cls.train(trainfeats, testfeats, nlt=nltk_run, skl=sklearn_run)
        # print(nlt_output['most1'])

        # exit()

        if nltk_run:
            statistic.add_nltk(nlt_output)
        if sklearn_run:
            statistic.add_skl(skl_output)

    if nltk_run:
        statistic.mean_nltk(cycles)
        statistic.print_nltk()
        # statistic.write_nltk(filename_nltk)
    if sklearn_run:
        statistic.mean_skl(cycles)
        statistic.print_skl()
        statistic.print_stddev()
        # statistic.write_skl(filename_skl)

nltk_run = True
sklearn_run = True

from_date = '2016-11-01'
to_date = '2017-08-31'
source = "stwits-comb"

binnings = ['none', 'low', 'high']
# subjects = ["snp", "djia", "nasdaq"]
subjects = ["djia", "snp", "nasdaq"]
# subjects = ["microsoft"]
precisions = ["0.6", "0.8", "1.0"]
# precisions = ["0.6"]

methods = ["Friday", "Natural", "Weekend", "Sunday"]
# methods = ["Friday"]



for subject in subjects:

    folder = settings.PREDICTOR_PREDICTION + '/' + source + '/' + subject + '/'
    os.makedirs(folder, exist_ok=True)
    filename_nltk = folder + source + '-prediction-' + subject + "-nltk.csv"
    filename_skl = folder + source + '-prediction-' + subject + "-skl.csv"

    # if nltk_run:
    #     open(filename_nltk, 'w').close()
    #
    # if sklearn_run:
    #     open(filename_skl, 'w').close()

    for method in methods:

        # if nltk_run:
        #     f = open(filename_nltk, 'a')
        #     f.write(source + ", " + subject + ", " + method + ", NLTK\n")
        #     f.write("precision, binning, accuracy, pos_prec, neg_prec, pos_rec, neg_rec, d1, d2, d3\n")
        #     f.close()
        #
        # if sklearn_run:
        #     f = open(filename_skl, 'a')
        #     f.write(source + ", " + subject + ", " + method + ", SKL\n")
        #     f.write("precision, binning, mnb, bnb, lr, lsvc, nsvc, voted\n")
        #     f.close()

        for precision in precisions:
            for binning in binnings:

                # print(source, subject, precision, method)
                run_one(source, subject, precision, method, from_date, to_date, binning, filename_nltk, filename_skl)
