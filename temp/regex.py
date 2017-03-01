
import re

row = "yes hey here"
word = "hey"

re_word = r"\b" + word + r"\b"
my_regex = re.compile(re_word, re.IGNORECASE)
match = re.search(word, row)
print(match)
if match:
    print(word)
    print(row)