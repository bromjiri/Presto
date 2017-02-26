import datetime

import trainer.trainer_mod as tr

import trainer.old.dataset as ds

# variables
COUNT = 2000
DATASET = "stanford"
lower_array = [True, False]


# file
output_file = "lower-" + DATASET + ".txt"
output = open(output_file, 'a')
output.write(str(datetime.datetime.today()) + "\n")

# cycle
for x in range(0, 10):
    stanford_set = ds.Dataset(DATASET, count=COUNT)

    for lower in lower_array:

        output.write(str(lower) + ", ")
        stanford_set.create_grams(pos=None, stop=False, stem=False, bigram=False, lower=lower)
        feature_set = tr.get_feature_set(stanford_set)
        training_set = feature_set[:round(COUNT * 8 / 10)]
        testing_set = feature_set[round(COUNT * 8 / 10):]
        output.write(tr.run_classifiers(training_set, testing_set))

    output.write("\n")
    output.flush()
