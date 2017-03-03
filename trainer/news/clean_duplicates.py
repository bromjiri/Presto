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


for subject in subjects:


    neg_set = set()
    # pos_file_path = "news_pos_" + subject + "-" + year + "-" + month + ".csv"
    # pos_file = open(pos_file_path, "w")
    neg_file_in = "news_neg_" + subject + "-" + year + "-" + month + ".csv"
    neg_in = open(neg_file_in, "w")
    neg_file_out = "news_neg_" + subject + "-" + year + "-" + month + ".csv"
    neg_out = open(neg_file_out, "w")


    for line in neg_in:
        neg_set.add(line)


    for line in neg_set:
        neg_out.write(line)