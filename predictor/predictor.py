import settings
import random
import nltk
import csv
import pandas as pd
import numpy as np

class Days:

    def __init__(self, three_days_list):
        self.days = dict()
        self.days[0] = three_days_list[0]
        self.days[1] = three_days_list[1]
        self.days[2] = three_days_list[2]
        # print(self.days)

    def shift(self, new_day):
        self.days[0] = self.days[1]
        self.days[1] = self.days[2]
        self.days[2] = new_day

    def get_features(self, sent_dict):
        features = dict()
        features[0] = sent_dict[self.days[0]]
        features[1] = sent_dict[self.days[1]]
        features[2] = sent_dict[self.days[2]]
        return features


# def get_dict(input_file):
#
#     stock_dict = dict()
#
#     with open(input_file, 'r') as input:
#         reader = csv.reader(input, delimiter=',')
#         prev = next(reader)[1]
#         for row in reader:
#             if row[1] > prev:
#                 stock_dict[row[0]] = 4
#             else:
#                 stock_dict[row[0]] = 0
#             prev = row[1]
#     return stock_dict

def get_dicts(diff_df, method):
    diff_df['SentBin'] = diff_df.apply(func, args=(method,), axis=1)
    diff_df['StockBin'] = diff_df.apply(func, args=('Stock',), axis=1)
    # print(diff_df)

    sent_dict = diff_df['SentBin'].dropna().astype(int).to_dict()
    stock_dict = diff_df['StockBin'].dropna().astype(int).to_dict()

    return sent_dict, stock_dict


def func(row, col):
    if pd.isnull(row[col]):
        return row[col]
    elif row[col] > 0:
        return 4
    else:
        return 0


def run_one(source, subject, precision, method):
    input_file_path = settings.PREDICTOR_DIFF + '/' + source + '/' + subject + '/' + source + '-diff-' + subject + '-' + precision + '.csv'
    # stock_dict = get_dict(input_file)
    diff_df = pd.read_csv(input_file_path, sep=',', index_col='Date')

    sent_dict, stock_dict = get_dicts(diff_df, method)

    days = Days([x for x in sorted(stock_dict)[0:3]])

    # for key in sorted(stock_dict):
    #     print(key, stock_dict[key], sent_dict[key])

    features_list = list()
    for key in sorted(stock_dict)[3:]:
        features = days.get_features(sent_dict)
        # print(features)
        features_list.append([features, stock_dict[key]])
        days.shift(key)
        # print(key, stock_dict[key], sent_dict[key])

    for f in features_list:
        print(f)

    random.shuffle(features_list)
    # print(len(features_list))

    training_set = features_list[:90]
    testing_set = features_list[90:]

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
    classifier.show_most_informative_features(1)


source = "stwits"
subjects = ["microsoft"]
# precisions = ["Sent0.6", "Sent0.8", "Sent1.0"]
# method = ["Friday", "Sunday", "Weekend"]
precisions = ["Sent0.6"]
methods = ["Friday"]

for precision in precisions:
    for subject in subjects:
        for method in methods:
            print(source, subject, precision, method)
            run_one(source, subject, precision, method)



