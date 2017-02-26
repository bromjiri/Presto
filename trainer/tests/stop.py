import datetime

import trainer.trainer_mod as tr

import trainer.old.dataset as ds


def run(dataset):
    COUNT = 2000
    DATASET = dataset
    stop_array = [True, False]


    # file
    output_file = "stop-" + DATASET + ".txt"
    output = open(output_file, 'a')
    output.write(dataset + ", " + str(datetime.datetime.today()) + "\n")

    # cycle
    for x in range(0, 10):
        stanford_set = ds.Dataset(DATASET, count=COUNT)

        for stop in stop_array:

            output.write(str(stop) + ", ")
            stanford_set.create_grams(pos=None, stop=stop, stem=False, bigram=False, lower=True)
            feature_set = tr.get_feature_set(stanford_set)
            training_set = feature_set[:round(COUNT * 8 / 10)]
            testing_set = feature_set[round(COUNT * 8 / 10):]
            output.write(tr.run_classifiers(training_set, testing_set))

        output.write("\n")
        output.flush()


dataset_array = ["stanford", "stwits"]

for dataset in dataset_array:
    run(dataset)