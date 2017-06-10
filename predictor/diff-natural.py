import settings
import pandas as pd
import numpy as np
import datetime
import os


class Stock:

    def __init__(self, subject):
        input_file = settings.PREDICTOR_STOCK + "/" + subject + ".csv"
        self.stock_df = pd.read_csv(input_file, sep=',', index_col='Date')

    def get_diff(self, from_date, to_date):
        return self.stock_df['Diff'].loc[from_date:to_date]


class Sent:

    def __init__(self, subject, source):
        input_file = settings.PREDICTOR_SENTIMENT + "/" + source + "/" + source + "-sent-" + subject + ".csv"
        self.sent_df = pd.read_csv(input_file, sep=',', index_col='Date')


    def create_diff(self, precision, stock_dates):

        sentiment_col = "Sent" + precision
        total_col = "Tot" + precision

        diff_df = pd.DataFrame(index=stock_dates, columns=['Natural1', 'Natural2', 'Natural3'])
        diff_df.index.name = "Date"

        for i in range(1,4):
            col = "Natural" + str(i)

            temp_df = pd.DataFrame(index=stock_dates, columns=['Natural'])
            temp_df['Total'] = self.sent_df[total_col]

            sunday_df = np.round(self.sent_df[sentiment_col].to_frame().diff(), 2)
            april26 = sunday_df[sentiment_col].loc['2017-04-26']
            april27 = sunday_df[sentiment_col].loc['2017-04-27']
            april28 = sunday_df[sentiment_col].loc['2017-04-28']

            # shift up
            sunday_df[sentiment_col] = sunday_df[sentiment_col].shift(i)

            # merge
            temp_df['Natural'] = sunday_df[sentiment_col].loc[stock_dates]

            # shift down
            temp_df['Natural'] = temp_df['Natural'].shift(-i)

            diff_df[col] = temp_df.apply(func, args=('Natural',), axis=1)
            diff_df.set_value('2017-04-26', col, april26)
            diff_df.set_value('2017-04-27', col, april27)
            diff_df.set_value('2017-04-28', col, april28)


        return diff_df


def func(row, col):
    if row['Total'] >= 10:
        return row[col]
    else:
        return 0

def run_one(subject, from_date, to_date, precision):

    # stock dataframe
    stock = Stock(subject)
    stock_df = stock.get_diff(from_date, to_date)
    # print(stock_df)

    # sentiment dataframe
    sent = Sent(subject, source)
    diff_df = sent.create_diff(precision, stock_df.index.values)
    # print(diff_df)

    # combine
    diff_df['Stock'] = stock_df
    # print(diff_df)

    # save output
    output_file_path = settings.PREDICTOR_DIFF + '/' + source + '/' + subject + '/' + source + '-diff-' + subject + '-' + precision + '-nat.csv'
    dir = os.path.dirname(os.path.realpath(output_file_path))
    os.makedirs(dir, exist_ok=True)
    diff_df.to_csv(output_file_path)




from_date = '2016-11-01'
to_date = '2017-04-30'
source = "twitter"
subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla"]
# subjects = ["tesla"]

precisions = ["0.6", "0.8", "1.0"]
# precisions = ["0.6"]



for precision in precisions:
    for subject in subjects:
        print(subject, precision)
        run_one(subject, from_date, to_date, precision)
