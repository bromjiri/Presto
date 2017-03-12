import datetime

import trainer.corpora as crp
import trainer.features as ftr
import trainer.classifier_test as cls
import os

# vars
type = "stem-lower"
nltk_run = True
sklearn_run = False
COUNT = 5000
cut = int((COUNT / 2) * 3 / 4)
array = ["none", "porter", "lemma"]

def run(dataset):

    nlt = dict()
    skl = dict()

    dir = "output/" + dataset + "/" + type + "/"
    os.makedirs(dir, exist_ok=True)

    # file
    for variable in array:
        var_name = str(variable)

        if nltk_run:
            nlt_file = dir + dataset + "-" + type + "-" + var_name + "-nlt.csv"
            nlt[var_name] = open(nlt_file, 'a')
            nlt[var_name].write(str(datetime.datetime.today()) + "\n")

        if sklearn_run:
            skl_file = dir + dataset + "-" + type + "-" + var_name + "-skl.csv"
            skl[var_name] = open(skl_file, 'a')
            skl[var_name].write(str(datetime.datetime.today()) + "\n")

    # cycle
    for x in range(0, 10):
        print(x)
        corpora = crp.Corpora(dataset, count=COUNT, shuffle=True)

        for variable in array:
            print(str(variable))
            var_name = str(variable)
            features = ftr.Features(corpora, total=COUNT, bigram=False, stem=variable, lower=True)

            posfeats = features.get_features_pos()
            negfeats = features.get_fearures_neg()

            trainfeats = negfeats[:cut] + posfeats[:cut]
            testfeats = negfeats[cut:] + posfeats[cut:]

            nlt_output, skl_output = cls.train(trainfeats, testfeats, nlt=nltk_run, skl=sklearn_run)

            if nltk_run:
                print(str(nlt_output))
                nlt[var_name].write(nlt_output)
                nlt[var_name].flush()
            if sklearn_run:
                print(str(skl_output))
                skl[var_name].write(skl_output)
                skl[var_name].flush()



dataset_array = ["stwits", "stanford"]

for dataset in dataset_array:
    run(dataset)