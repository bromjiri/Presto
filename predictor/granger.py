import settings
import pandas as pd
import numpy as np


class Stock:

    def __init__(self, subject):
        input_file = settings.PREDICTOR_STOCK + "/" + subject + ".csv"
        self.stock_df = pd.read_csv(input_file, sep=',', index_col='Date')

    def get_diff(self, from_date, to_date):
        return self.stock_df['Diff'].loc[from_date:to_date]


class Sent:

    def __init__(self, source, subject):
        input_file = settings.PREDICTOR_SENTIMENT + "/" + source + "/" + source + "-sent-" + subject + ".csv"
        self.sent_df = pd.read_csv(input_file, sep=',', index_col='date')

    def get_diff(self, col_name, from_date, to_date):
        self.diff_df = self.sent_df.diff()
        return self.diff_df[col_name].loc[from_date:to_date]


from_date = '2017-01-01'
to_date = '2017-03-31'
subject = "spx"

stock = Stock("snp")
stock_df = stock.get_diff(from_date, to_date)
# print(stock_df)

sent = Sent("stwits", subject)
sent_df = sent.get_diff('comb1.0', from_date, to_date)
# print(sent_df)


new_df = stock_df.to_frame().join(sent_df.to_frame(), how='left')
print(new_df)
new_df.to_csv('data/output/output-' + subject + '.csv')