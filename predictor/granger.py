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

    def get_weekend(self, col_name, stock_dates):

        weekend_df = np.round(self.sent_df, 2)

        aggreg = 0
        days = 1
        for idx, row in weekend_df.iterrows():
            value = row[col_name]
            date = pd.to_datetime(idx)
            date_plus = date + datetime.timedelta(days=1)
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

        return np.round(weekend_df[col_name].to_frame().diff(), 2)

    def create_diff(self, col_name, stock_dates):

        diff_df = pd.DataFrame(index=stock_dates, columns=['Friday', 'Sunday', "Weekend"])
        diff_df.index.name = "Date"

        friday_df = self.sent_df[col_name].loc[stock_dates]
        diff_df['Friday'] = np.round(friday_df.diff(), 2)

        sunday_df = np.round(self.sent_df[col_name].to_frame().diff(), 2)
        # print(sunday_df)
        diff_df['Sunday'] =  sunday_df[col_name].loc[stock_dates]


        weekend_df = self.get_weekend(col_name, stock_dates)
        # print(weekend_df)
        diff_df['Weekend'] = weekend_df[col_name].loc[stock_dates]

        return diff_df


def run_one(subject, from_date, to_date, precision_col):

    # stock dataframe
    stock = Stock(subject)
    stock_df = stock.get_diff(from_date, to_date)
    # print(stock_df)

    # sentiment dataframe
    sent = Sent(subject, source)
    diff_df = sent.create_diff(precision_col, stock_df.index.values)
    # print(diff_df)

    # combine
    diff_df['Stock'] = stock_df
    # print(diff_df)

    # save output
    output_file_path = settings.PREDICTOR_DIFF + '/' + source + '/' + subject + '/' + source + '-diff-' + subject + '-' + precision + '.csv'
    dir = os.path.dirname(os.path.realpath(output_file_path))
    os.makedirs(dir, exist_ok=True)
    diff_df.to_csv(output_file_path)


def run_the(subject, from_date, to_date, precision_col):

    stock = Stock('djia')
    stock_df = stock.get_diff(from_date, to_date)

    # sentiment dataframe
    sent = Sent(subject, source)
    diff_df = sent.create_diff(precision_col, stock_df.index.values)

    indexes = ['djia', 'nasdaq', 'snp']

    for index in indexes:

        # stock dataframe
        stock = Stock(index)
        stock_df = stock.get_diff(from_date, to_date)

        # combine
        diff_df[index] = stock_df

    # save output
    output_file_path = settings.PREDICTOR_DIFF + '/' + source + '/' + subject + '/' + source + '-diff-' + subject + '-' + precision + '.csv'
    dir = os.path.dirname(os.path.realpath(output_file_path))
    os.makedirs(dir, exist_ok=True)
    diff_df.to_csv(output_file_path)



from_date = '2016-11-01'
to_date = '2017-04-30'
source = "stwits-comb"
subjects = ["microsoft", "netflix", "nike", "tesla"]
# subjects = ["tesla"]

precisions = ["Sent0.6", "Sent0.8", "Sent1.0"]

for precision in precisions:
    for subject in subjects:
        print(subject, precision)
        run_one(subject, from_date, to_date, precision)
    # run_the('the', from_date, to_date, precision)
