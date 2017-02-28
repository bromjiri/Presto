import datetime

import trainer.corpora as crp
import trainer.features as ftr
import trainer.classifier as cls


def run(dataset):

    COUNT = 10000
    cut = int((COUNT / 2) * 3 / 4)
    array = [False, True]

    nlt = dict()
    skl = dict()

    # file
    for variable in array:
        nlt_file = "stop-" + dataset + "-" + str(variable) + "-nlt.csv"
        skl_file = "stop-" + dataset + "-" + str(variable) + "-skl.csv"
        nlt[str(variable)] = open(nlt_file, 'a')
        skl[str(variable)] = open(skl_file, 'a')
        nlt[str(variable)].write(str(datetime.datetime.today()) + " COUNT= " + str(COUNT) + "\n")
        skl[str(variable)].write(str(datetime.datetime.today()) + " COUNT= " + str(COUNT) + "\n")

    # cycle
    for x in range(0, 20):
        print(x)
        corpora = crp.Corpora(dataset, count=COUNT, shuffle=True)

        for variable in array:
            features = ftr.Features(corpora, total=COUNT, stop=variable)

            posfeats = features.get_features_pos()
            negfeats = features.get_fearures_neg()

            trainfeats = negfeats[:cut] + posfeats[:cut]
            testfeats = negfeats[cut:] + posfeats[cut:]

            nlt_output, skl_output = cls.classify(trainfeats, testfeats)

            nlt[str(variable)].write(nlt_output)
            skl[str(variable)].write(skl_output)



dataset_array = ["stanford"]

for dataset in dataset_array:
    run(dataset)