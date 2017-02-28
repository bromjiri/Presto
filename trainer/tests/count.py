import datetime

import trainer.corpora as crp
import trainer.features as ftr
import trainer.classifier_test as cls


def run(dataset):


    array = [50000, 40000, 30000, 20000]

    nlt = dict()
    skl = dict()

    # file
    for variable in array:
        var_name = str(variable)
        nlt_file = "inf-" + dataset + "-" + var_name + "-nlt.csv"
        skl_file = "inf-" + dataset + "-" + var_name + "-skl.csv"
        nlt[var_name] = open(nlt_file, 'a')
        skl[var_name] = open(skl_file, 'a')
        # nlt[var_name].write(str(datetime.datetime.today()) + " COUNT= " + str(COUNT) + "\n")
        # skl[var_name].write(str(datetime.datetime.today()) + " COUNT= " + str(COUNT) + "\n")

    # cycle
    for variable in array:

        COUNT = variable
        cut = int((COUNT / 2) * 3 / 4)
        print(str(variable))

        corpora = crp.Corpora(dataset, count=COUNT, shuffle=True)

        for x in range(0, 5):
            print(x)

            var_name = str(variable)
            features = ftr.Features(corpora, total=COUNT, bigram=True)

            posfeats = features.get_features_pos()
            negfeats = features.get_fearures_neg()

            trainfeats = negfeats[:cut] + posfeats[:cut]
            testfeats = negfeats[cut:] + posfeats[cut:]

            nlt_output, skl_output = cls.train(trainfeats, testfeats)

            nlt[var_name].write(nlt_output)
            skl[var_name].write(skl_output)



dataset_array = ["stanford"]

for dataset in dataset_array:
    run(dataset)