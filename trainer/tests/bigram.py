import datetime

import trainer.corpora as crp
import trainer.features as ftr
import trainer.classifier_test as cls

NLTK = True
SKLEARN = False

def run(dataset):

    COUNT = 20000
    cut = int((COUNT / 2) * 3 / 4)
    array = [[False, 0], [True, 10], [True, 15], [True, 20], [True, 25], [True, 30]]

    nlt = dict()
    skl = dict()

    # file
    for variable in array:
        var_name = str(variable[0]) + str(variable[1])

        if NLTK:
            nlt_file = "bigram-" + dataset + "-" + var_name + "-nlt.csv"
            nlt[var_name] = open(nlt_file, 'a')
            nlt[var_name].write(str(datetime.datetime.today()) + " COUNT= " + str(COUNT) + "\n")

        if SKLEARN:
            skl_file = "bigram-" + dataset + "-" + var_name + "-skl.csv"
            skl[var_name] = open(skl_file, 'a')
            skl[var_name].write(str(datetime.datetime.today()) + " COUNT= " + str(COUNT) + "\n")

    # cycle
    for x in range(0, 3):
        print(x)
        corpora = crp.Corpora(dataset, count=COUNT, shuffle=True)

        for variable in array:
            print(str(variable[1]))
            var_name = str(variable[0]) + str(variable[1])
            features = ftr.Features(corpora, total=COUNT, bigram=variable[0], bigram_count=variable[1])

            posfeats = features.get_features_pos()
            negfeats = features.get_fearures_neg()

            trainfeats = negfeats[:cut] + posfeats[:cut]
            testfeats = negfeats[cut:] + posfeats[cut:]

            nlt_output, skl_output = cls.train(trainfeats, testfeats, nlt=NLTK, skl=SKLEARN)

            if NLTK:
                print(str(nlt_output))
                nlt[var_name].write(nlt_output)
                nlt[var_name].flush()
            if SKLEARN:
                skl[var_name].write(skl_output)



dataset_array = ["stwits"]

for dataset in dataset_array:
    run(dataset)