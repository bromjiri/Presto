import csv
from datetime import datetime


def process_day(day, month, subject):

    input_file = "../../presto/downloads/twitter/" + subject + "/twitter-" + subject + "-2016-" + month + "-" + day + "-fix.csv"


    pos = 0
    neg = 0
    total = 0

    with open(input_file, "r") as twi:
        reader = csv.reader(twi, delimiter=',')
        for row in reader:
            total+=1
            try:
                sent = row[-1]
            except:
                print("error: " + str(row))
                pass

            if("pos" in sent):
                pos+=1
            elif("neg" in sent):
                neg+=1
            else:
                print("not recognized sentiment" + str(row))

    pos_per = pos/total
    print("Subject: " + subject + ", Day: " + day + " pos: " + "{:.2f}".format(pos_per*100))
    return "{:.2f}".format(pos_per*100)


### start processing ###

year = 2016
month = 11
first_day = 1
last_day = 30
weekend = set([5,6])
subjects = ["microsoft", "cola", "mcdonald", "samsung", "netflix", "nike", "tesla", "the"]

us_holidays = "../sentiment/us_holidays.txt"

year_str = str(year)
month_str = str(month).zfill(2)


for subject in subjects:

    output_file = "../sentiment/twitter/twitter-sent-" + subject + "-2016-" + month_str + ".csv"
    output =  open(output_file, "w")
    writer = csv.writer(output, delimiter=',')

    for i in range(first_day, last_day+1):
        day_str = str(i).zfill(2)
        date = datetime(year, month, i).date()
        if (date.weekday() not in weekend and str(date) not in open(us_holidays).read()):
            pos_day = process_day(day_str, month_str, subject)
            writer.writerow([year_str, month_str, day_str, pos_day])

    output.close()