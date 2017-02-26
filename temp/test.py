
def make_dict(words):
    return dict([(word, True) for word in words])

words = ["a", "b", "c"]

features = make_dict(words)

for key in features.keys():
    print(key)


