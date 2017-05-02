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

    def get_weekend(self, col_name, dates):

        weekend_df = np.round(self.sent_df, 2)
        new_df = pd.DataFrame(index=dates, columns=['new'])


        aggeg = 0
        days = 1
        for idx, row in weekend_df.iterrows():
            value = row[col_name]
            date = pd.to_datetime(idx)
            date_plus = date + datetime.timedelta(days=1)
            if str(date_plus.date()) not in dates:
                print("weekend")
                value += aggeg
                aggeg = value
                days += 1
            else:
                total = value + aggeg
                value = total / days
                aggeg = 0
                days = 1


            print(date.date(), row[col_name], value)

        print(weekend_df)

    def create_diff(self, col_name, dates):

        diff_df = pd.DataFrame(index=dates, columns=['Friday', 'Sunday', "Weekend"])
        diff_df.index.name = "Date"

        friday_df = self.sent_df[col_name].loc[dates]
        diff_df['Friday'] = np.round(friday_df.diff(), 2)

        sunday_df = np.round(self.sent_df.diff(), 2)
        diff_df['Sunday'] =  sunday_df[col_name].loc[dates]



        diff_df['Weekend'] = self.get_weekend(col_name, dates)

        # print(diff_df)


from_date = '2016-11-01'
to_date = '2017-04-30'
source = "twitter"
subject = "microsoft"
precision_col = "Sent1.0"

stock = Stock(subject)
stock_df = stock.get_diff(from_date, to_date)
# print(stock_df)


sent = Sent(subject, source)
sent_df = sent.create_diff(precision_col, stock_df.index.values)
# print(sent_df)

# exit()

# new_df = stock_df.to_frame().join(sent_df.to_frame(), how='left')
# # print(new_df)
#
# file_path = settings.PREDICTOR_DIFF + '/' + source + '/' + source + '-diff-' + subject + '.csv'
# dir = os.path.dirname(os.path.realpath(file_path))
# os.makedirs(dir, exist_ok=True)
# new_df.to_csv(file_path)