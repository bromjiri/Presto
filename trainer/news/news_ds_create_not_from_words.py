# create news datasets
import settings
import re


def read_file(year, month, sentiment):

    input_file_path = settings.TRAINER + "/news/data/auto_dataset/news_" + sentiment + "_140-" + year + ".csv"

    try:
        with open(input_file_path, "r") as news_file:
            i = 0
            for row in news_file:
                print(i)
                i = i+1

                pos_match = False
                neg_match = False

                if sentiment == "neg":
                    my_words = neg_words
                    my_file = not_neg_file
                else:
                    my_words = pos_words
                    my_file = not_pos_file

                for my_word in my_words:
                    re_not = r"\bnot." + my_word +  r"\b"
                    my_regex = re.compile(re_not)
                    not_match = re.search(my_regex, row)

                    re_nt = r"n\'t." + my_word +  r"\b"
                    my_regex = re.compile(re_nt)
                    nt_match = re.search(my_regex, row)


                    if not_match or nt_match:
                        print(my_word)
                        print(row)
                        my_file.write(row)
                        my_file.flush()
                        break



    except Exception as e:
        print(e)
        pass


######################

periods = [["2017", "01"]]
first_day = 1
last_day = 31
# subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]
subjects = ["pos", "neg"]


neg_words_path = "data/neg_words_hu.txt"
neg_words_file = open(neg_words_path, "r")
neg_words = list()
for n_word in neg_words_file:
    neg_words.append(n_word.strip())

pos_words_path = "data/pos_words_hu.txt"
pos_words_file = open(pos_words_path, "r")
pos_words = list()
for p_word in pos_words_file:
    pos_words.append(p_word.strip())

# print(neg_words)
# print(len(neg_words))

for period in periods:

    year = period[0]
    month = period[1]

    not_pos_file_path = "news_not_pos_" + year + "-" + month + ".csv"
    not_pos_file = open(not_pos_file_path, "w")
    not_neg_file_path = "news_not_neg_" + year + "-" + month + ".csv"
    not_neg_file = open(not_neg_file_path, "w")

    for subject in subjects:

        # for i in range(first_day, last_day+1):
        print("Subject: " + subject)
        read_file(year, month, subject)
