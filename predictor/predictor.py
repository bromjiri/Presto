import settings
import random
import nltk
import csv

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

def get_dict(input_file):

    stock_dict = dict()

    with open(input_file, 'r') as input:
        reader = csv.reader(input, delimiter=',')
        prev = next(reader)[1]
        for row in reader:
            if row[1] > prev:
                stock_dict[row[0]] = 4
            else:
                stock_dict[row[0]] = 0
            prev = row[1]
    return stock_dict


subject = "coca-cola"
source = "twitter"
conf_limit = "1.0"

input_file = settings.PREDICTOR_STOCK + "/" + subject + ".csv"
stock_dict = get_dict(input_file)

input_file = settings.PREDICTOR_SENTIMENT + "/" + source + "/" + source + "-sent-" + subject + "-" + conf_limit + ".csv"
sent_dict = get_dict(input_file)

days = dict()
days = Days([x for x in sorted(stock_dict)[0:3]])

# for key in sorted(stock_dict):
#     print(key, stock_dict[key], sent_dict[key])

features_list = list()
for key in sorted(stock_dict)[2:]:
    features = days.get_features(sent_dict)
    # print(features)
    features_list.append([features, stock_dict[key]])
    days.shift(key)
    # print(key, stock_dict[key], sent_dict[key])

for f in features_list:
    print(f)

random.shuffle(features_list)

training_set = features_list[:60]
testing_set = features_list[60:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
classifier.show_most_informative_features(1)