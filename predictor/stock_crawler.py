import datetime as dt
import pandas_datareader.data as web
import numpy as np


start = dt.datetime(2016,11,1)
end = dt.datetime(2017,2,28)


def download_stock(key):

    try:
        df = web.DataReader(stock_list[key], 'yahoo', start, end)
        output_file = "data/stock/" + key + ".csv"
        # print(np.round(df[['Close']], 2))

        np.round(df[['Close']], 2).to_csv(output_file, sep=',', header=None)
    except Exception as e:
        print(e)

stock_list = {"coca-cola": "KO", "mcdonalds": "MCD", "microsoft": "MSFT", "netflix": "NFLX", "nike": "NKE",
              "samsung": "005930.KS", "tesla": "TSLA", "nasdaq": "NDAQ", "djia": "DJIA", "snp": "^GSPC"}

for key in stock_list:
    print(key)
    download_stock(key)