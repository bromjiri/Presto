import settings
import csv

subject = "microsoft"

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


input_file = settings.PREDICTOR_STOCK + "/" + subject + ".csv"
stock_dict = get_dict(input_file)

input_file = settings.PREDICTOR_SENTIMENT + "/news/news-sent-" + subject + ".csv"
sent_dict = get_dict(input_file)

for key in sorted(stock_dict):
    print(key, stock_dict[key], sent_dict[key])