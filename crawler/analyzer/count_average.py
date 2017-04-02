import settings








def run_process(year, month, day, subject):

    # twitter
    # input_file_path = settings.DOWNLOADS_TWITTER + "/" + subject + "/twitter-" + subject + "-" + year + "-" + month + "-" + day + "-fix.csv"

    # stocktwits
    # input_file_path = settings.DOWNLOADS_STWITS + "/" + subject + "/stwits-" + subject + "-" + year + "-" + month + "-" + day + "-fix.csv"

    # news
    input_file_path = settings.DOWNLOADS_NEWS + "/final/" + subject + "/news-" + subject + "-" + year + "-" + month + "-" + day + "-final.csv"

    input_file = open(input_file_path, "r")

    length = len(input_file.readlines())
    print(length)
    sums_dict[subject] += length





year = "2017"
month = "02"
first_day = 1
last_day = 28

dataset = "twitter"

# twitter
# subjects = ["cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]

# stocktwits
# subjects = ["ko", "mcd", "msft", "nflx", "nke", "ssnlf", "tsla", "compq", "djia", "spx", "the"]

# news
subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]

sums_dict = dict.fromkeys(subjects, 0)

output_file_path = "average-" + str(dataset) + "-" + year + "-" + month + ".csv"
output_file = open(output_file_path, "w")

for subject in subjects:

    for i in range(first_day, last_day+1):
        day = str(i).zfill(2)
        print("Subject: " + subject + ", Day: " + day)
        try:
            run_process(year, month, day, subject)
        except Exception as e:
            print(e)


    print(subject + " = " + str(sums_dict[subject]))
    average = round(sums_dict[subject] / 31)
    print(average)
    # output_file.write(subject + "," + str(average) + "\n")
