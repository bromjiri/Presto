import datetime

import trainer.dataset_new as ds

import trainer.old.trainer_mod as tr


def run(dataset):
    COUNT = 2000
    DATASET = dataset
    stem_array = [None, "porter", "lemma"]


    # file
    output_file = "stem-" + DATASET + ".txt"
    output = open(output_file, 'a')
    output.write(dataset + ", " + str(datetime.datetime.today()) + "\n")

    # cycle
    for x in range(0, 10):
        stanford_set = ds.Dataset(DATASET, count=COUNT)

        for stem in stem_array:

            output.write(str(stem) + ", ")
            stanford_set.create_grams(pos=None, stop=None, stem=stem, bigram=False, lower=True)
            feature_set = tr.get_feature_set(stanford_set)
            training_set = feature_set[:round(COUNT * 8 / 10)]
            testing_set = feature_set[round(COUNT * 8 / 10):]
            output.write(tr.run_classifiers(training_set, testing_set))

        output.write("\n")
        output.flush()


dataset_array = ["stanford", "stwits"]

for dataset in dataset_array:
    run(dataset)