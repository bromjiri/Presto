import datetime

import trainer.trainer_mod as tr

import trainer.old.dataset as ds


def run(dataset):
    COUNT = 2000
    DATASET = dataset
    bigram_array = [[False, False], [False, True], [True, True]]


    # file
    output_file = "bigram-" + DATASET + ".txt"
    output = open(output_file, 'a')
    output.write(dataset + ", " + str(datetime.datetime.today()) + "\n")

    # cycle
    for x in range(0, 10):
        stanford_set = ds.Dataset(DATASET, count=COUNT)

        for bigram in bigram_array:

            output.write(str(bigram) + ", ")
            stanford_set.create_grams(pos=None, stop=bigram[0], stem=False, bigram=bigram[1], lower=True)
            feature_set = tr.get_feature_set(stanford_set)
            training_set = feature_set[:round(COUNT * 8 / 10)]
            testing_set = feature_set[round(COUNT * 8 / 10):]
            output.write(tr.run_classifiers(training_set, testing_set))

        output.write("\n")
        output.flush()


dataset_array = ["stwits", "stanford"]

for dataset in dataset_array:
    run(dataset)