import settings
import csv
import pandas as pd
import numpy as np


class StockDiff:

    def __init__(self, source):
        input_file = settings.PREDICTOR_STOCK + "/" + source + ".csv"
        df = pd.read_csv(input_file, sep=',', index_col='Date')

        df['Diff'] = df['Close'].diff()
        df['Binary'] = np.where(df['Diff'] > 0, 4, 0)
        print(df)



stock_diff = StockDiff("coca-cola")