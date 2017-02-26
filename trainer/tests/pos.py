import datetime

import trainer.trainer_mod as tr

import trainer.old.dataset as ds

# variables
COUNT = 2000
DATASET = "stwits"

# file
output_file = "pos-" + DATASET + ".txt"
output = open(output_file, 'a')
output.write(str(datetime.datetime.today()) + "\n")

# cycle
for x in range(0, 10):
    stanford_set = ds.Dataset(DATASET, count=COUNT)

    output.write(str(None) + ", ")
    stanford_set.create_grams(pos=None, stop=False, stem=False, bigram=False, lower=True)
    feature_set = tr.get_feature_set(stanford_set)
    training_set = feature_set[:round(COUNT * 8 / 10)]
    testing_set = feature_set[round(COUNT * 8 / 10):]
    output.write(tr.run_classifiers(training_set, testing_set))

    output.write("FUPJVNR, ")
    stanford_set.create_grams(pos=["F", "U", "P", "J", "V", "N", "R"], stop=False, stem=False, bigram=False, lower=True)
    feature_set = tr.get_feature_set(stanford_set)
    training_set = feature_set[:round(COUNT * 8 / 10)]
    testing_set = feature_set[round(COUNT * 8 / 10):]
    output.write(tr.run_classifiers(training_set, testing_set))

    output.write("UPJVNR, ")
    stanford_set.create_grams(pos=["U", "P", "J", "V", "N", "R"], stop=False, stem=False, bigram=False, lower=True)
    feature_set = tr.get_feature_set(stanford_set)
    training_set = feature_set[:round(COUNT * 8 / 10)]
    testing_set = feature_set[round(COUNT * 8 / 10):]
    output.write(tr.run_classifiers(training_set, testing_set))

    output.write("PJVNR, ")
    stanford_set.create_grams(pos=["P", "J", "V", "N", "R"], stop=False, stem=False, bigram=False, lower=True)
    feature_set = tr.get_feature_set(stanford_set)
    training_set = feature_set[:round(COUNT * 8 / 10)]
    testing_set = feature_set[round(COUNT * 8 / 10):]
    output.write(tr.run_classifiers(training_set, testing_set))

    output.write("JVNR, ")
    stanford_set.create_grams(pos=["J", "V", "N", "R"], stop=False, stem=False, bigram=False, lower=True)
    feature_set = tr.get_feature_set(stanford_set)
    training_set = feature_set[:round(COUNT * 8 / 10)]
    testing_set = feature_set[round(COUNT * 8 / 10):]
    output.write(tr.run_classifiers(training_set, testing_set))

    output.write("JVR, ")
    stanford_set.create_grams(pos=["J", "V", "R"], stop=False, stem=False, bigram=False, lower=True)
    feature_set = tr.get_feature_set(stanford_set)
    training_set = feature_set[:round(COUNT * 8 / 10)]
    testing_set = feature_set[round(COUNT * 8 / 10):]
    output.write(tr.run_classifiers(training_set, testing_set))

    output.write("\n")
    output.flush()
