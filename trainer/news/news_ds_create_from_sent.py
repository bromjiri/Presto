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
                twi_sent, twi_conf = stn.sent_stwits(row)
                if twi_sent == "pos" and twi_conf == 1.0:
                    pos_file.write(row)
                    # print("pos")
                    pos_file.flush()
                    i += 1
                    print(i)
                elif twi_sent == "neg" and twi_conf > 0.6:
                    neg_file.write(row)
                    # print("neg")
                    neg_file.flush()
                    i += 1
                    print(i)



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