import datetime
import os
import trainer.corpora as crp
import trainer.features as ftr
import trainer.classifier_test as cls


def run(dataset):

    COUNT = 5000
    cut = int((COUNT / 2) * 3 / 4)

    nlt = dict()
    skl = dict()

    dir = "output/" + dataset + "/pos/"
    os.makedirs(dir, exist_ok=True)

    # cycle
    for x in range(0, 10):
        print(x)
        corpora = crp.Corpora(dataset, count=COUNT, shuffle=True)

        #####

        var = "NONE"
        nlt_file = dir + dataset + "-" + "pos" + "-" + var + "-nlt.csv"
        # skl_file = "output/" + dataset + "/" + dataset + "-" + "pos" + "-" + var + "-skl.csv"
        nlt[var] = open(nlt_file, 'a')
        # skl[var] = open(skl_file, 'a')

        features = ftr.Features(corpora, total=COUNT, pos=None)

        posfeats = features.get_features_pos()
        negfeats = features.get_fearures_neg()

        trainfeats = negfeats[:cut] + posfeats[:cut]
        testfeats = negfeats[cut:] + posfeats[cut:]

        nlt_output, skl_output = cls.train(trainfeats, testfeats, skl=False)

        nlt[var].write(nlt_output)
        nlt[var].flush()
        print(str(nlt_output))
        # skl[var].write(skl_output)

        #####

        var = "JVNR"

        nlt_file = dir + dataset + "-" + "pos" + "-" + var + "-nlt.csv"
        # skl_file = "output/" + dataset + "/" + dataset + "-" + "pos" + "-" + var + "-skl.csv"
        nlt[var] = open(nlt_file, 'a')
        # skl[var] = open(skl_file, 'a')

        features = ftr.Features(corpora, total=COUNT, pos=["J", "V", "N", "R"])

        posfeats = features.get_features_pos()
        negfeats = features.get_fearures_neg()

        trainfeats = negfeats[:cut] + posfeats[:cut]
        testfeats = negfeats[cut:] + posfeats[cut:]

        nlt_output, skl_output = cls.train(trainfeats, testfeats, skl=False)

        nlt[var].write(nlt_output)
        nlt[var].flush()
        print(str(nlt_output))
        # skl[var].write(skl_output)

        #####

        var = "EUJVNR"

        nlt_file = dir + dataset + "-" + "pos" + "-" + var + "-nlt.csv"
        # skl_file = "output/" + dataset + "/" + dataset + "-" + "pos" + "-" + var + "-skl.csv"
        nlt[var] = open(nlt_file, 'a')
        # skl[var] = open(skl_file, 'a')

        features = ftr.Features(corpora, total=COUNT, pos=["E", "U", "J", "V", "N", "R"])

        posfeats = features.get_features_pos()
        negfeats = features.get_fearures_neg()

        trainfeats = negfeats[:cut] + posfeats[:cut]
        testfeats = negfeats[cut:] + posfeats[cut:]

        nlt_output, skl_output = cls.train(trainfeats, testfeats, skl=False)

        nlt[var].write(nlt_output)
        nlt[var].flush()
        print(str(nlt_output))
        # skl[var].write(skl_output)

        #####


        var = "FEUPJVNR"

        nlt_file = dir + dataset + "-" + "pos" + "-" + var + "-nlt.csv"
        # skl_file = "output/" + dataset + "/" + dataset + "-" + "pos" + "-" + var + "-skl.csv"
        nlt[var] = open(nlt_file, 'a')
        # skl[var] = open(skl_file, 'a')

        features = ftr.Features(corpora, total=COUNT, pos=["F", "E", "U", "P", "J", "V", "N", "R"])

        posfeats = features.get_features_pos()
        negfeats = features.get_fearures_neg()

        trainfeats = negfeats[:cut] + posfeats[:cut]
        testfeats = negfeats[cut:] + posfeats[cut:]

        nlt_output, skl_output = cls.train(trainfeats, testfeats, skl=False)

        nlt[var].write(nlt_output)
        nlt[var].flush()
        print(str(nlt_output))
        # skl[var].write(skl_output)



dataset_array = ["stanford"]

for dataset in dataset_array:
    print(dataset)
    run(dataset)