# get final sentences
import settings
import nltk
import os
import re
from langdetect import detect


def fix_file(year, month, day, subject, source):
    date = year + "-" + month + "-" + day

    try:
        output_file_path = settings.DOWNLOADS_NEWS + "/final/" + subject + "/news-" + subject + "-" + year + "-" + month + "-" + day + "-final.csv"
        dir = os.path.dirname(os.path.realpath(output_file_path))
        os.makedirs(dir, exist_ok=True)
        output_file = open(output_file_path, "w")

        if source == "bing":
            input_file_path = settings.DOWNLOADS_NEWS + "/bing/" + subject + "/news-" + subject + "-" + year + "-" + month + "-" + day + ".csv"
        elif source == "google":
            input_file_path = settings.DOWNLOADS_NEWS + "/google/" + subject + "/" + date + "/" + subject + "_old_sentences_" + date + ".txt"

        input_file = open(input_file_path, "r")

        for row in input_file:
            row = re.sub(r'(\.)([A-Z])', r'\1 \2', row)
            for sentence in nltk.sent_tokenize(row):

                if len(sentence) > 140:
                    continue

                if subject not in sentence.lower():
                    continue
                else:
                    if detect(sentence) == "es":
                        continue

                    output_file.write(sentence.strip() + "\n")

    except Exception as e:
        print(e)
        pass


source = "bing"
year = "2017"
month = "01"
first_day = 1
last_day = 31
# subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]
subjects = ["the"]

for subject in subjects:

    for i in range(first_day, last_day+1):
        day = str(i).zfill(2)
        print("Subject: " + subject + ", Day: " + day)
        fix_file(year, month, day, subject, source)