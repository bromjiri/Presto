import trainer.dataset_new as ds

import trainer.old.trainer_mod as tr

COUNT = 1000

for x in range(0,5):

    sanders_set = ds.Dataset("stanford", COUNT)

    sanders_set.create_grams(pos=None, stop=False, stem="porter", bigram=False, lower=True)
    feature_set = tr.get_feature_set(sanders_set)

    training_set = feature_set[:round(COUNT*8/10)]
    testing_set = feature_set[round(COUNT*8/10):]

    tr.run_classifiers(training_set, testing_set)

    sanders_set.create_grams(pos=None, stop=False, stem="lemma", bigram=False, lower=True)
    feature_set = tr.get_feature_set(sanders_set)

    training_set = feature_set[:round(COUNT*8/10)]
    testing_set = feature_set[round(COUNT*8/10):]

    tr.run_classifiers(training_set, testing_set)
