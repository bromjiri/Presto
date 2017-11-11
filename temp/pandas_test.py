# import pandas_datareader.data as web
# import datetime as dt
import settings
import pandas as pd

# start = dt.datetime(2016, 11, 1)
# end = dt.datetime(2016, 12, 31)
#
# df = web.DataReader('TSLA', "yahoo", start, end)
#
# print(df)

dataset = "news"
subject = "netflix"
year = "2017"
month = "03"
day = "03"

input_file = settings.PREDICTOR_SENTIMENT + "/" + dataset + "/" + dataset + "-sent-" + subject + ".csv"
sent_df = pd.read_csv(input_file, sep=',', index_col='Date')

print(sent_df.loc["2016-11-01"]["Tot0.6"])

# my_date = year + "-" + month + "-" + day
#
# length = sent_df.iloc[my_date]['Tot0.6']