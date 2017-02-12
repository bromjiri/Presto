# fix newlines
import settings
import csv



def read_file(year, month, day, subject):

    input_file_path = settings.DOWNLOADS_STWITS + "/" + subject + "/stwits-" + subject + "-" + year + "-" + month + "-" + day + "-fix.csv"

    with open(input_file_path, "r") as stwits:
        reader = csv.reader(stwits, delimiter=',')
        for row in reader:

            if row[1] == "Bullish":
                bull_file.write(row[2] + "\n")
            elif row[1] == "Bearish":
                bear_file.write(row[2] + "\n")
            else:
                pass

            print(row)


######################

year = "2016"
month = "11"
first_day = 1
last_day = 30
subjects = ["nflx"]

bull_file_path = "bull_nflx.csv"
bull_file = open(bull_file_path, "a")
bear_file_path = "bear_nflx.csv"
bear_file = open(bear_file_path, "a")

for subject in subjects:

    for i in range(first_day, last_day+1):
        day = str(i).zfill(2)
        print("Subject: " + subject + ", Day: " + day)
        read_file(year, month, day, subject)
        # exit()