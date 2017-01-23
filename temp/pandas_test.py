import pandas_datareader.data as web
import datetime as dt

start = dt.datetime(2016, 11, 1)
end = dt.datetime(2016, 12, 31)

df = web.DataReader('TSLA', "yahoo", start, end)

print(df)