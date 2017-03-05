# fix newlines
import settings
import csv
import re
import nltk


# months = [["2016", "11"], ["2016", "12"], ["2017", "01"], ["2017", "02"]]
year = "2017"
month = "01"
# subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]
subjects = ["the"]
limit = 80

for subject in subjects:


    my_set = set()
    # pos_file_path = "news_pos_" + subject + "-" + year + "-" + month + ".csv"
    # pos_file = open(pos_file_path, "w")
    neg_file_in = "data/auto_dataset/news_neg_" + subject + "-" + year + "-" + month + ".csv"
    neg_in = open(neg_file_in, "r")
    neg_file_out = "data/auto_dataset/news_neg_" + subject + "-" + year + "-" + month + "-8090.csv"
    neg_out = open(neg_file_out, "w")


    for line in neg_in:
        my_set.add(line)

    for line in my_set:
        if(len(line) < 90 and len(line) > 80):
            neg_out.write(line)