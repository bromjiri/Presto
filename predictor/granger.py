import settings
import pandas as pd
import numpy as np
import os


class Stock:

    def __init__(self, subject):
        input_file = settings.PREDICTOR_STOCK + "/" + subject + ".csv"
        self.stock_df = pd.read_csv(input_file, sep=',', index_col='Date')

    def get_diff(self, from_date, to_date):
        return self.stock_df['Diff'].loc[from_date:to_date]


class Sent:

    def __init__(self, source, subject):
        input_file = settings.PREDICTOR_SENTIMENT + "/" + source + "/" + source + "-sent-" + subject + ".csv"
        self.sent_df = pd.read_csv(input_file, sep=',', index_col='Date')

    def get_diff(self, col_name, from_date, to_date):
        self.diff_df = np.round(self.sent_df.diff(), 2)
        return self.diff_df[col_name].loc[from_date:to_date]


from_date = '2016-11-01'
to_date = '2017-03-31'
source = "twitter"
subject = "microsoft"

stock = Stock("microsoft")
stock_df = stock.get_diff(from_date, to_date)
# print(stock_df)

sent = Sent(source, subject)
sent_df = sent.get_diff('Sent1.0', from_date, to_date)
# print(sent_df)


new_df = stock_df.to_frame().join(sent_df.to_frame(), how='left')
print(new_df)

file_path = settings.PREDICTOR_DIFF + '/' + source + '/' + source + '-diff-' + subject + '.csv'
dir = os.path.dirname(os.path.realpath(file_path))
os.makedirs(dir, exist_ok=True)
new_df.to_csv(file_path)