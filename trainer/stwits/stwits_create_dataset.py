# fix newlines
import settings
import csv
import re
import nltk


def read_file(year, month, day, subject):



    input_file_path = settings.DOWNLOADS_STWITS + "/" + subject + "/stwits-" + subject + "-" + year + "-" + month + "-" + day + "-fix.csv"

    try:
        with open(input_file_path, "r") as stwits:
            reader = csv.reader(stwits, delimiter=',')
            for row in reader:

                subject_ticker = "\$" + subject
                my_regex = re.compile(subject_ticker, re.IGNORECASE)
                post = my_regex.sub('sbjct', row[2])

                my_regex = re.compile(subject, re.IGNORECASE)
                post = my_regex.sub('sbjct', post)

                ref = re.compile(r"([@])(\w+)\b")
                my_regex = re.compile(ref)
                post = my_regex.sub('ref', post)

                other_ticker = re.compile(r"([$])(\w+)\b")
                my_regex = re.compile(other_ticker)
                post = my_regex.sub('', post)

                http = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                my_regex = re.compile(http)
                post = my_regex.sub('url', post)

                post = re.sub("\d+", "num", post)

                post = re.sub("[,\.\-:;|]", " ", post)

                post = re.sub("\s\s+", " ", post)

                post_words = nltk.word_tokenize(post)
                word_count = 0
                for word in post_words:
                    if word != "sbjct":
                        word_count+=1

                if(word_count < 3):
                    continue


                if row[1] == "Bullish":
                    bull_file.write(post + "\n")
                    # print(post)
                elif row[1] == "Bearish":
                    bear_file.write(post + "\n")
                    # print(post)
                else:
                    pass


    except:
        print(input_file_path)
        pass


######################

year = "2016"
month = "12"
first_day = 1
last_day = 30
subjects = ["msft", "ko", "mcd", "ssnlf", "nflx", "nke", "tsla", "compq", "spx", "djia"]

bull_file_path = "bull_mix.csv"
bull_file = open(bull_file_path, "a")
bear_file_path = "bear_mix.csv"
bear_file = open(bear_file_path, "a")

for subject in subjects:

    for i in range(first_day, last_day+1):
        day = str(i).zfill(2)
        print("Subject: " + subject + ", Day: " + day)
        read_file(year, month, day, subject)
        # exit()