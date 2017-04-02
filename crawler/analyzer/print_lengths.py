import settings








def run_process(year, month, day, subject):

    # twitter
    input_file_path = settings.DOWNLOADS_TWITTER + "/" + subject + "/twitter-" + subject + "-" + year + "-" + month + "-" + day + "-fix.csv"

    # stocktwits
    # input_file_path = settings.DOWNLOADS_STWITS + "/" + subject + "/stwits-" + subject + "-" + year + "-" + month + "-" + day + "-fix.csv"

    # news
    # input_file_path = settings.DOWNLOADS_NEWS + "/final/" + subject + "/news-" + subject + "-" + year + "-" + month + "-" + day + "-final.csv"

    input_file = open(input_file_path, "r")

    length = len(input_file.readlines())
    print(length)





year = "2017"
month = "01"
first_day = 1
last_day = 31

# twitter
# subjects = ["cola", "mcdonald", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]
subjects = ["cola", "mcdonald", "microsoft"]


# stocktwits
# subjects = ["ko", "mcd", "msft", "nflx", "nke", "ssnlf", "tsla", "compq", "djia", "spx", "the"]

# news
# subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]


for subject in subjects:

    for i in range(first_day, last_day+1):
        day = str(i).zfill(2)
        print("Subject: " + subject + ", Day: " + day)
        try:
            run_process(year, month, day, subject)
        except Exception as e:
            print(e)

