import datetime

import trainer.trainer_mod as tr

import trainer.old.dataset as ds


def run(dataset):
    COUNT = 2000
    DATASET = dataset
    bigram_array = [[["U", "J", "V", "N", "R"], False, True], [None, True, True], [None, False, True]]


    # file
    output_file = "bigram-comb-" + DATASET + ".txt"
    output = open(output_file, 'a')
    output.write(dataset + ", " + str(datetime.datetime.today()) + "\n")

    # cycle
    common_count_array = [4000, 4000, 7000, 7000, 10000, 10000, 13000, 13000, 16000, 16000]

    for common in common_count_array:
        stanford_set = ds.Dataset(DATASET, count=COUNT)
        output.write(str(common) + "\n")

        for bigram in bigram_array:

            output.write(str(bigram) + ", ")
            stanford_set.create_grams(pos=bigram[0], stop=bigram[1], stem=True, bigram=bigram[2], lower=False)
            feature_set = tr.get_feature_set(stanford_set, common_count=common)
            training_set = feature_set[:round(COUNT * 8 / 10)]
            testing_set = feature_set[round(COUNT * 8 / 10):]
            output.write(tr.run_classifiers(training_set, testing_set))

        output.write("\n")
        output.flush()


dataset_array = ["stanford", "stwits"]

for dataset in dataset_array:
    run(dataset)