import csv
import random
import nltk

class SentList:
    sent_list = list()
    subject = ""
    start_month = 11
    end_month = 12

    def __init__(self, subject):

        self.subject = subject
        self.read_file()
        self.append_shift()

    def read_file(self):
        # read sentiment to sent_list
        for month in range(self.start_month, self.end_month + 1):

            month_str = str(month).zfill(2)
            file_name = "../data/sentiment/twitter/twitter-sent-" + self.subject + "-2016-" + month_str + ".csv"
            with open(file_name, "r") as sent_file:
                csv_reader = csv.reader(sent_file, delimiter=',')
                for row in csv_reader:
                    self.sent_list.append(row)

        print("sent_list " + self.subject + " read")

    def append_shift(self):
        # append result
        for i in range(1, len(self.sent_list)):
            if (float(self.sent_list[i][3]) - float(self.sent_list[i - 1][3]) >= 0):
                self.sent_list[i].append(4)
            else:
                self.sent_list[i].append(0)

        print("sent_list " + self.subject + " appended")

    def get_features(self, s_list):
        features_list = list()
        offset = 3
        for i in range(offset + 1, len(self.sent_list)):
            features = {}
            features[0] = self.sent_list[i - (offset - 0)][4]
            features[1] = self.sent_list[i - (offset - 1)][4]
            features[2] = self.sent_list[i - (offset - 2)][4]

            date = str(self.sent_list[i][0]) + "-" + str(self.sent_list[i][1]) + "-" + str(self.sent_list[i][2])
            features_list.append([features, s_list.find_by_date(date)])

            print(date, features, s_list.find_by_date(date))

        return features_list

    def print_out(self):
        for x in self.sent_list:
            print(x)


class StockList:
    stock_list = list()
    subject = ""

    def __init__(self, stock):

        self.stock = stock
        self.read_file()
        self.append_shift()

    def read_file(self):
        # read stock to stock_list
        file_name = "../stock/stock-" + self.stock + "-3m.csv"
        with open(file_name, "r") as stock_file:
            csvreader = csv.reader(stock_file, delimiter=',')
            for row in csvreader:
                self.stock_list.append(row)

        del self.stock_list[0]
        self.stock_list = list(reversed(self.stock_list))
        print("stock_list read")

    def append_shift(self):
        # append result
        for i in range(0, len(self.stock_list)):
            if ((float(self.stock_list[i][4]) - float(self.stock_list[i][1])) >= 0):
                self.stock_list[i].append(4)
            else:
                self.stock_list[i].append(0)

        print("stock_list appended")

    def find_by_date(self, date):
        for line in self.stock_list:
            if date in line[0]:
                return line[7]
        return 2

    def print_out(self):
        for x in self.stock_list:
            print(x)


sent_cola = SentList("cola")
sent_cola.print_out()

stock_cola = StockList("cola")
stock_cola.print_out()

features_list = sent_cola.get_features(stock_cola)


random.shuffle(features_list)

training_set = features_list[:23]
testing_set = features_list[23:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
classifier.show_most_informative_features(1)