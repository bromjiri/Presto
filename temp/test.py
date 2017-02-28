import re


def make_dict(words):
    return dict([(word, True) for word in words])

words = ["a", "b", "c"]

features = make_dict(words)

for key in features.keys():
    print(key)


array = ["one", "two", "one"]
array.remove("one")
print(array)


post = re.sub(r'(\.)([A-Z])', r'\1 \2', ".A 789")
print(post)