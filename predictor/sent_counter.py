import settings
import csv
import trainer.sentan as st

from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)



def count_sent(day, subject, writer):


    if source == "news":
        input_file = settings.DOWNLOADS_NEWS + "/final/" + subject + "/news-" + subject + "-" + day + "-final.csv"
    elif source == "twitter":
        input_file = settings.DOWNLOADS_TWITTER + "/" + subject + "/" + "twitter-" + subject + "-" + day + ".csv"

    pos = 0
    neg = 0
    total = 0

    with open(input_file, "r") as file:
        for row in file:
            total += 1
            try:
                sent, conf = st.sent_news(row.strip())
            except Exception as e:
                print(e)
                continue

            if (sent == "pos"):
                # print("pos: " + row)
                pos += 1
            else:
                # print("neg: " + row)
                neg += 1

    if(total < 10):
        pos_per = 0.5
    else:
        pos_per = pos / total

    pos_per = "{:.2f}".format(pos_per * 100)
    print(day, total, pos_per)
    writer.writerow([day, pos_per])






source = "news"
subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]
# subjects = ["coca-cola"]

start_date = date(2016, 11, 1)
end_date = date(2017, 2, 28)

for subject in subjects:
    print(subject)

    output_file = settings.PREDICTOR_SENTIMENT + "/news/news-sent-" + subject + ".csv"
    output = open(output_file, "a")
    writer = csv.writer(output, delimiter=',')

    for single_date in daterange(start_date, end_date):
        day = single_date.strftime("%Y-%m-%d")
        count_sent(day, subject, writer)
