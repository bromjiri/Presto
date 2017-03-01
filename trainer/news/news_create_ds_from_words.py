# fix newlines
import settings
import csv
import re
import nltk

import trainer.sentan as stn


def read_file(year, month, day, subject):



    input_file_path = settings.DOWNLOADS_NEWS + "/final/" + subject + "/news-" + subject + "-" + year + "-" + month + "-" + day + "-final.csv"

    i = 0
    try:
        with open(input_file_path, "r") as news_file:
            for row in news_file:
                # print(row)
                for word in neg_words:

                    re_word = r"\b" + word + r"\b"
                    my_regex = re.compile(re_word, re.IGNORECASE)
                    match = re.search(my_regex, row)
                    if match:
                        neg_file.write(row)
                        print(word)
                        print(row)




    except Exception as e:
        print(e)
        pass


######################

# months = [["2016", "11"], ["2016", "12"], ["2017", "01"], ["2017", "02"]]
year = "2017"
month = "01"
first_day = 1
last_day = 30
# subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]
subjects = ["the"]


neg_words_path = "data/neg_words.txt"
neg_words_file = open(neg_words_path, "r")
neg_words = set()
for line in neg_words_file:
    neg_words.add(line.strip().lower())

print(len(neg_words))


for subject in subjects:

    pos_file_path = "news_pos_" + subject + "-" + year + "-" + month + ".csv"
    pos_file = open(pos_file_path, "w")
    neg_file_path = "news_neg_" + subject + "-" + year + "-" + month + ".csv"
    neg_file = open(neg_file_path, "w")


    for i in range(first_day, last_day+1):
        day = str(i).zfill(2)
        print("Subject: " + subject + ", Day: " + day)
        read_file(year, month, day, subject)
        # exit()