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
    # for variable in array:
    #     nlt_file = "stop-" + dataset + "-" + str(variable) + "-nlt.csv"
    #     skl_file = "stop-" + dataset + "-" + str(variable) + "-skl.csv"
    #     nlt[str(variable)] = open(nlt_file, 'a')
    #     skl[str(variable)] = open(skl_file, 'a')
    #     nlt[str(variable)].write(str(datetime.datetime.today()) + " COUNT= " + str(COUNT) + "\n")
    #     skl[str(variable)].write(str(datetime.datetime.today()) + " COUNT= " + str(COUNT) + "\n")

    # cycle
    for x in range(0, 10):
        print(x)
        corpora = crp.Corpora(dataset, count=COUNT, shuffle=True)

        #####

        var = "NONE"

        nlt_file = "pos-" + dataset + "-" + var + "-nlt.csv"
        skl_file = "pos-" + dataset + "-" + var + "-skl.csv"
        nlt[var] = open(nlt_file, 'a')
        skl[var] = open(skl_file, 'a')

        features = ftr.Features(corpora, total=COUNT, pos=None)

        posfeats = features.get_features_pos()
        negfeats = features.get_fearures_neg()

        trainfeats = negfeats[:cut] + posfeats[:cut]
        testfeats = negfeats[cut:] + posfeats[cut:]

        nlt_output, skl_output = cls.classify(trainfeats, testfeats)

        nlt[var].write(nlt_output)
        skl[var].write(skl_output)

        #####

        var = "JVNR"

        nlt_file = "pos-" + dataset + "-" + var + "-nlt.csv"
        skl_file = "pos-" + dataset + "-" + var + "-skl.csv"
        nlt[var] = open(nlt_file, 'a')
        skl[var] = open(skl_file, 'a')

        features = ftr.Features(corpora, total=COUNT, pos=["J", "V", "N", "R"])

        posfeats = features.get_features_pos()
        negfeats = features.get_fearures_neg()

        trainfeats = negfeats[:cut] + posfeats[:cut]
        testfeats = negfeats[cut:] + posfeats[cut:]

        nlt_output, skl_output = cls.classify(trainfeats, testfeats)

        nlt[var].write(nlt_output)
        skl[var].write(skl_output)

        #####

        var = "PJVNR"

        nlt_file = "pos-" + dataset + "-" + var + "-nlt.csv"
        skl_file = "pos-" + dataset + "-" + var + "-skl.csv"
        nlt[var] = open(nlt_file, 'a')
        skl[var] = open(skl_file, 'a')

        features = ftr.Features(corpora, total=COUNT, pos=["P", "J", "V", "N", "R"])

        posfeats = features.get_features_pos()
        negfeats = features.get_fearures_neg()

        trainfeats = negfeats[:cut] + posfeats[:cut]
        testfeats = negfeats[cut:] + posfeats[cut:]

        nlt_output, skl_output = cls.classify(trainfeats, testfeats)

        nlt[var].write(nlt_output)
        skl[var].write(skl_output)

        #####

        var = "UJVNR"

        nlt_file = "pos-" + dataset + "-" + var + "-nlt.csv"
        skl_file = "pos-" + dataset + "-" + var + "-skl.csv"
        nlt[var] = open(nlt_file, 'a')
        skl[var] = open(skl_file, 'a')

        features = ftr.Features(corpora, total=COUNT, pos=["U", "J", "V", "N", "R"])

        posfeats = features.get_features_pos()
        negfeats = features.get_fearures_neg()

        trainfeats = negfeats[:cut] + posfeats[:cut]
        testfeats = negfeats[cut:] + posfeats[cut:]

        nlt_output, skl_output = cls.classify(trainfeats, testfeats)

        nlt[var].write(nlt_output)
        skl[var].write(skl_output)

        #####

        var = "UPJVNR"

        nlt_file = "pos-" + dataset + "-" + var + "-nlt.csv"
        skl_file = "pos-" + dataset + "-" + var + "-skl.csv"
        nlt[var] = open(nlt_file, 'a')
        skl[var] = open(skl_file, 'a')

        features = ftr.Features(corpora, total=COUNT, pos=["U", "P", "J", "V", "N", "R"])

        posfeats = features.get_features_pos()
        negfeats = features.get_fearures_neg()

        trainfeats = negfeats[:cut] + posfeats[:cut]
        testfeats = negfeats[cut:] + posfeats[cut:]

        nlt_output, skl_output = cls.classify(trainfeats, testfeats)

        nlt[var].write(nlt_output)
        skl[var].write(skl_output)

        #####

        var = "EUPJVNR"

        nlt_file = "pos-" + dataset + "-" + var + "-nlt.csv"
        skl_file = "pos-" + dataset + "-" + var + "-skl.csv"
        nlt[var] = open(nlt_file, 'a')
        skl[var] = open(skl_file, 'a')

        features = ftr.Features(corpora, total=COUNT, pos=["E", "U", "P", "J", "V", "N", "R"])

        posfeats = features.get_features_pos()
        negfeats = features.get_fearures_neg()

        trainfeats = negfeats[:cut] + posfeats[:cut]
        testfeats = negfeats[cut:] + posfeats[cut:]

        nlt_output, skl_output = cls.classify(trainfeats, testfeats)

        nlt[var].write(nlt_output)
        skl[var].write(skl_output)


        #####

        var = "FEUPJVNR"

        nlt_file = "pos-" + dataset + "-" + var + "-nlt.csv"
        skl_file = "pos-" + dataset + "-" + var + "-skl.csv"
        nlt[var] = open(nlt_file, 'a')
        skl[var] = open(skl_file, 'a')

        features = ftr.Features(corpora, total=COUNT, pos=["F", "E", "U", "P", "J", "V", "N", "R"])

        posfeats = features.get_features_pos()
        negfeats = features.get_fearures_neg()

        trainfeats = negfeats[:cut] + posfeats[:cut]
        testfeats = negfeats[cut:] + posfeats[cut:]

        nlt_output, skl_output = cls.classify(trainfeats, testfeats)

        nlt[var].write(nlt_output)
        skl[var].write(skl_output)



dataset_array = ["stanford"]

for dataset in dataset_array:
    run(dataset)