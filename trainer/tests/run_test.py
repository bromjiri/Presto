import datetime

import trainer.corpora as crp
import trainer.features as ftr
import trainer.classifier_test as cls





def run_test(dataset, type, iter=10, count=5000, shuffle=False, nltk_run=True, sklearn_run=True, inf_count=-1,
                 bigram_count=50, pos=None, stop=False, stem="none", bigram=False, lower=True):

    cut = int((count / 2) * 3 / 4)

    nlt = dict()
    skl = dict()

    # file
    for variable in array:
        var_name = str(variable)

        if nltk_run:
            nlt_file = "output/" + dataset + "/" + dataset + "-" + type + "-" + var_name + "-nlt.csv"
            nlt[var_name] = open(nlt_file, 'a')
            nlt[var_name].write(str(datetime.datetime.today()) + "\n")

        if sklearn_run:
            skl_file = "output/" + dataset + "/" + dataset + "-" + type + "-" + var_name + "-skl.csv"
            skl[var_name] = open(skl_file, 'a')
            skl[var_name].write(str(datetime.datetime.today()) + "\n")

    # cycle
    for x in range(0, iter):
        print(x)
        corpora = crp.Corpora(dataset, count, shuffle)

        for variable in array:
            print(str(variable[1]))
            var_name = str(variable[0]) + str(variable[1])
            features = ftr.Features(corpora, count, inf_count, bigram_count, pos, stop, stem, bigram, lower)

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
                print(str(nlt_output))
                skl[var_name].write(skl_output)
                nlt[var_name].flush()


# dataset_array = ["stwits"]
#
# for dataset in dataset_array:
#     run(dataset)