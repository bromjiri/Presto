import settings
import pandas as pd







def run_process(year, month, day, subject, dataset):

    # news
    input_file = settings.PREDICTOR_SENTIMENT + "/" + dataset + "/" + dataset + "-sent-" + subject + ".csv"
    sent_df = pd.read_csv(input_file, sep=',', index_col='Date')

    my_date = year + "-" + month + "-" + day

    length = sent_df.loc[my_date]['Tot0.6']
    print(length)
    sums_dict[subject] += length





year = "2017"
month = "06"
first_day = 1
last_day = 30

dataset = "news"

# twitter
# subjects = ["cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]

# stocktwits
# subjects = ["ko", "mcd", "msft", "nflx", "nke", "ssnlf", "tsla", "compq", "djia", "spx", "the"]

# news
subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "tesla", "the"]

sums_dict = dict.fromkeys(subjects, 0)

output_file_path = "average-" + str(dataset) + "-" + year + "-" + month + ".csv"
output_file = open(output_file_path, "a")

for subject in subjects:

    for i in range(first_day, last_day+1):

        if i not in [3,4,10,11,17,18,24,25]:
            continue

        day = str(i).zfill(2)
        print("Subject: " + subject + ", Day: " + day)
        try:
            run_process(year, month, day, subject, dataset)
        except Exception as e:
            print(e)


    print(subject + " = " + str(sums_dict[subject]))
    average = round(sums_dict[subject] / 8)
    print(average)

    output_file.write(subject + "," + str(average) + "\n")
