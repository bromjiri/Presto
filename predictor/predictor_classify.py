import pickle

logreg_f = open("pickled/tesla_logreg.pickle", "rb")
logreg = pickle.load(logreg_f)
logreg_f.close()


vector_f = open("pickled/tesla_vector.pickle", "rb")
vectorizer = pickle.load(vector_f)
vector_f.close()

feature = dict()
feature['d1'] = 4
feature['d2'] = 4
feature['d3'] = 4

vector = vectorizer.transform(feature)

label = logreg.predict(vector)
print("predicted: " + str(label))

print("all classes: " + str(logreg.classes_))
probs = logreg.predict_proba(vector)
print("probabilities: " + str(probs))