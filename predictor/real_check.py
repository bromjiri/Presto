import pickle
import pandas as pd
import settings
import predictor.predictor_sklearn as pred


logreg_f = open("pickled/tesla_logreg.pickle", "rb")
logreg = pickle.load(logreg_f)
logreg_f.close()


vector_f = open("pickled/tesla_vector.pickle", "rb")
vectorizer = pickle.load(vector_f)
vector_f.close()

from_date = '2017-08-29'
to_date = '2017-10-29'
binning = 'none'
precision = "0.6"
method = "Friday"

stock = pred.Stock('tesla')
stock.create_dict(from_date, to_date)
stock_dict = stock.get_dict()
# print(stock_dict)

sent = pred.Sent('tesla', 'stwits')
sent.create_dict(precision, method, from_date, to_date, stock.get_stock_dates(), binning)
sent_dict = sent.get_dict()
# print(sent_dict)


total = 0
match = 0
for key in sorted(stock_dict)[3:]:
    total += 1
    features = sent.get_features(key)
    print(key, features, stock_dict[key])
    if features['d3'] == stock_dict[key]:
        match +=1

print(total, match)