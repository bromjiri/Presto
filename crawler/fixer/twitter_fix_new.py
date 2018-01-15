# fix newlines
import settings
import os

def fix_file(year, month, day, subject):

    output_file_path = settings.DOWNLOADS_TWITTER_FINAL + "/" + subject + "/twitter-" + subject + "-" + year + "-" + month + "-" + day + "-fix.csv"
    dir = os.path.dirname(os.path.realpath(output_file_path))
    os.makedirs(dir, exist_ok=True)
    output_file = open(output_file_path, "w")

    input_file_path = settings.DOWNLOADS_TWITTER + "/" + subject + "/twitter-" + subject + "-" + year + "-" + month + "-" + day + ".csv"
    input_file = open(input_file_path, "r")
    # input_list = input_file.readlines()
    # unique_list = list(set(input_list))
    output_list = list()
    line = ""
    input_file = input_file.readlines()

    previous = input_file[0].strip()
    date = year + "-" + month + "-" + day

    for row in input_file[1:]:

        if row.strip() == "":
            continue

        if not date in row:
            previous += row.strip()
        else:
            output_list.append(previous + "\n")
            previous = row.strip()

    output_list_wo_date = list()
    for line in output_list:
        output_list_wo_date.append(line[22:])
        # print(line[22:])

    unique_list = list(set(output_list_wo_date))
    for line in unique_list:

        if line.strip() == "":
            continue

        if subject == "cola":
            if not ("coca-cola" in line.lower() or "coca cola" in line.lower()):
                continue

        if subject == "netflix":
            if "chill" in line.lower():
                continue

        if subject == "mcdonald":
            if not ("mcdonalds" in line.lower() or "mcdonald's" in line.lower()):
                continue

        output_file.write(line)

    output_file.close()



# periods = [["2016", "11"], ["2016", "12"], ["2017", "01"], ["2017", "02"], ["2017", "03"]]
periods = [["2017", "09"], ["2017", "10"], ["2017", "11"], ["2017", "12"]]
first_day = 1
last_day = 31
subjects = ["cola", "mcdonald","microsoft", "netflix", "nike", "tesla", "the"]
# subjects = ["mcdonald"]


for period in periods:

    year = period[0]
    month = period[1]

    for subject in subjects:

        for i in range(first_day, last_day+1):
            day = str(i).zfill(2)
            print("Subject: " + subject + ", Day: " + day)
            try:
                fix_file(year, month, day, subject)
            except Exception as e:
                print(e)