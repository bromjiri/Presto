import trainer.trainer_mod as tr

import trainer.old.dataset as ds

COUNT = 2000


stwits_set = ds.Dataset("stwits", COUNT)
stwits_set.create_grams(pos=None, stop=True, stem=True, bigram=True, lower=False)
feature_set = tr.get_feature_set(stwits_set)

training_set = feature_set[:round(COUNT*8/10)]
testing_set = feature_set[round(COUNT*8/10):]

tr.run_classifiers(training_set, testing_set)