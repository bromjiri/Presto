# create news datasets
import settings
import re


def read_file(year, month, day, subject):

    # input_file_path = settings.DOWNLOADS_NEWS + "/final/" + subject + "/news-" + subject + "-" + year + "-" + month +\
    #                   "-" + day + "-final.csv"
    input_file_path = settings.TRAINER_DATA + "/news/news_pos_80_2500.csv"

    try:
        with open(input_file_path, "r") as news_file:
            for row in news_file:

                pos_match = False
                neg_match = False

                for neg_word in neg_words:
                    re_word = r"\b" + neg_word + r"\b"
                    my_regex = re.compile(re_word)
                    neg_match = re.search(my_regex, row)
                    if neg_match:
                        break

                for pos_word in pos_words:
                    re_word = r"\b" + pos_word + r"\b"
                    my_regex = re.compile(re_word)
                    pos_match = re.search(my_regex, row)
                    if pos_match:
                        break


                re_not = r"\bnot\b"
                my_regex = re.compile(re_not)
                not_match = re.search(my_regex, row)

                re_nt = r"n\'t\b"
                my_regex = re.compile(re_nt)
                nt_match = re.search(my_regex, row)


                if pos_match and neg_match:
                    neu_file.write(row)
                    neu_file.flush()
                    print(pos_word, neg_word)
                    print(row)
                # if pos_match:
                #     if not_match or nt_match:
                #         not_pos_file.write(row)
                #         not_pos_file.flush()
                #     else:
                #         pos_file.write(row)
                #         pos_file.flush()
                #         print("pos: " + pos_word)
                #         print(row)
                # if neg_match:
                #     if not_match or nt_match:
                #         not_neg_file.write(row)
                #         not_neg_file.flush()
                #     else:
                #         neg_file.write(row)
                #         neg_file.flush()
                #         print("neg: " + neg_word)
                #         print(row)

    except Exception as e:
        print(e)
        pass


######################

periods = [["2017", "01"]]
first_day = 1
last_day = 1
# subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]
subjects = ["the"]


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

    for subject in subjects:

        pos_file_path = "news_pos_" + subject + "-" + year + "-" + month + ".csv"
        pos_file = open(pos_file_path, "w")
        neg_file_path = "news_neg_" + subject + "-" + year + "-" + month + ".csv"
        neg_file = open(neg_file_path, "w")
        neu_file_path = "news_neu_" + subject + "-" + year + "-" + month + ".csv"
        neu_file = open(neu_file_path, "w")
        not_pos_file_path = "news_not_pos_" + subject + "-" + year + "-" + month + ".csv"
        not_pos_file = open(not_pos_file_path, "w")
        not_neg_file_path = "news_not_neg_" + subject + "-" + year + "-" + month + ".csv"
        not_neg_file = open(not_neg_file_path, "w")

        for i in range(first_day, last_day+1):
            day = str(i).zfill(2)
            print("Subject: " + subject + ", Day: " + day)
            read_file(year, month, day, subject)
