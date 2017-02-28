import datetime

import trainer.corpora as crp
import trainer.features as ftr
import trainer.classifier as cls


def run(dataset):

    COUNT = 10000
    cut = int((COUNT / 2) * 3 / 4)
    stem_array = ["none", "porter", "lemma"]

    nlt = dict()
    skl = dict()

    # file
    for stem in stem_array:
        nlt_file = "stem-" + dataset + "-" + stem + "-nlt.txt"
        skl_file = "stem-" + dataset + "-" + stem + "-skl.txt"
        nlt[stem] = open(nlt_file, 'a')
        skl[stem] = open(skl_file, 'a')
        # nlt[stem].write(str(datetime.datetime.today()) + "\n")
        # skl[stem].write(str(datetime.datetime.today()) + "\n")

    # cycle
    for x in range(0, 10):
        print(x)
        corpora = crp.Corpora(dataset, count=COUNT, shuffle=True)

        for stem in stem_array:
            features = ftr.Features(corpora, total=COUNT, stem=stem)

            posfeats = features.get_features_pos()
            negfeats = features.get_fearures_neg()

            trainfeats = negfeats[:cut] + posfeats[:cut]
            testfeats = negfeats[cut:] + posfeats[cut:]

            nlt_output, skl_output = cls.classify(trainfeats, testfeats)

            nlt[stem].write(nlt_output)
            skl[stem].write(skl_output)



dataset_array = ["stanford"]

for dataset in dataset_array:
    run(dataset)