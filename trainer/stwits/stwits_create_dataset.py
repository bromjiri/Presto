# fix newlines
import settings
import csv
import re



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
                post = my_regex.sub('', post)

                other_ticker = re.compile(r"([$])(\w+)\b")
                my_regex = re.compile(other_ticker)
                post = my_regex.sub('', post)

                http = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                my_regex = re.compile(http)
                post = my_regex.sub('', post)

                if(len(post) < 10):
                    pass

                if row[1] == "Bullish":
                    bull_file.write(post + "\n")
                    print(post)
                elif row[1] == "Bearish":
                    bear_file.write(post + "\n")
                    print(post)
                else:
                    pass


    except:
        print(input_file_path)
        pass


######################

year = "2017"
month = "02"
first_day = 1
last_day = 20
subjects = ["spx"]

bull_file_path = "bull_spx.csv"
bull_file = open(bull_file_path, "a")
bear_file_path = "bear_spx.csv"
bear_file = open(bear_file_path, "a")

for subject in subjects:

    for i in range(first_day, last_day+1):
        day = str(i).zfill(2)
        print("Subject: " + subject + ", Day: " + day)
        read_file(year, month, day, subject)
        # exit()