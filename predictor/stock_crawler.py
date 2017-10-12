import datetime as dt
import pandas as pd
import numpy as np


start = dt.datetime(2016,11,1)
end = dt.datetime(2017,8,31)


def download_stock(key):

    try:
        # df = web.DataReader(stock_list[key], 'yahoo', start, end)
        df = pd.read_csv("data/stock/" + stock_list[key] + ".csv", index_col="Date")
        output_file = "data/stock/" + key + ".csv"

        df_new = np.round(df[['Close']], 2)

        df_new['Diff'] = np.round(df_new['Close'].diff(), 2)
        df_new['Binary'] = np.where(df_new['Diff'] > 0, 4, 0)
        print(df_new)
        df_new.to_csv(output_file, sep=',')

    except Exception as e:
        print(e)

# stock_list = {"coca-cola": "KO", "mcdonalds": "MCD", "microsoft": "MSFT", "netflix": "NFLX", "nike": "NKE",
#               "samsung": "005930.KS", "tesla": "TSLA", "nasdaq": "NDAQ", "djia": ".DJI", "snp": "^GSPC"}

stock_list = {"snp": "GSPC"}

for key in stock_list:
    print(key)
    download_stock(key)