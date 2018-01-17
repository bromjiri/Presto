import settings
import pandas as pd
import numpy as np
import os
from datetime import timedelta
import predictor.predictor_statistic as stat
import random
import pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


logreg_f = open("pickled/tesla_logreg.pickle", "rb")
logreg = pickle.load(logreg_f)
logreg_f.close()


vector_f = open("pickled/tesla_vector.pickle", "rb")
vectorizer = pickle.load(vector_f)
vector_f.close()

feature = dict()
feature['d1'] = 0
feature['d2'] = 4
feature['d3'] = 4

vector = vectorizer.transform(feature)

label = logreg.predict(vector)
print("predicted: " + str(label))

print("all classes: " + str(logreg.classes_))
probs = logreg.predict_proba(vector)
print("probabilities: " + str(probs))