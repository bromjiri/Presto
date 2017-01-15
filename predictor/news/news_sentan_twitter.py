import settings
from datetime import datetime
import crawler.sentan.sentan_twitter as s
import csv


def sentiment_day(year_str, month_str, day_str, subject):

    date_str = year_str + "-" + month_str + "-" + day_str
    # google
    input_file_path = settings.DOWNLOADS_NEWS + "/google/" + subject + "/" + date_str + "/" + subject + "_old_sentences_" + date_str + ".txt"
    # bing
    # input_file_path = settings.DOWNLOADS

    pos = 0
    neg = 0
    total = 0

    with open(input_file_path, "r") as input_file:
        for row in input_file:
            total += 1
            try:
                sentiment_value, confidence = s.sentiment(row)
                if confidence * 100 >= 80:
                    sent = sentiment_value
                else:
                    sent = "neu"
            except:
                print("error: " + str(row))
                pass

            if ("pos" in sent):
                pos += 1
            elif ("neg" in sent):
                neg += 1

            print(sent + ": " + str(row.strip()))

    pos_per = pos / total
    print("Subject: " + subject + ", Day: " + day_str + " pos: " + "{:.2f}".format(pos_per * 100))
    return "{:.2f}".format(pos_per * 100)



    #sentiment_value, confidence = s.sentiment(tweet.text)


### start processing ###

year = 2016
month = 12
first_day = 1
last_day = 31
weekend = set([5,6])
#subjects = ["microsoft", "cola", "mcdonald", "samsung", "netflix", "nike", "tesla", "the"]
subjects = ["microsoft"]

us_holidays = settings.PROCESS_SENTIMENT + "/us_holidays.txt"

year_str = str(year)
month_str = str(month).zfill(2)


for subject in subjects:

    output_file_path = settings.PROCESS_SENTIMENT + "/news/news-sent-" + subject + "-2016-" + month_str + ".csv"
    with open(output_file_path, "w") as output_file:
        writer = csv.writer(output_file, delimiter=',')

        for i in range(first_day, last_day+1):
            day_str = str(i).zfill(2)
            date = datetime(year, month, i).date()
            if (date.weekday() not in weekend and str(date) not in open(us_holidays).read()):
                pos_day = sentiment_day(year_str, month_str, day_str, subject)
                writer.writerow([year_str, month_str, day_str, pos_day])
                output_file.flush()

        output_file.close()