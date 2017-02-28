# fix newlines
import settings

def fix_file(year, month, day, subject):

    try:

        output_file_path = settings.DOWNLOADS_STWITS + "/" + subject + "/stwits-" + subject + "-" + year + "-" + month + "-" + day + "-fix.csv"
        output_file = open(output_file_path, "w")

        input_file_path = settings.DOWNLOADS_STWITS + "/" + subject + "/stwits-" + subject + "-" + year + "-" + month + "-" + day + ".csv"
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


        unique_list = list(set(output_list))
        for line in unique_list:
            if line.strip() != "\n":
                output_file.write(line)

        output_file.close()

    except:
        pass


year = "2016"
month = "12"
first_day = 1
last_day = 30
subjects = ["msft", "ko", "mcd", "ssnlf", "nflx", "nke", "tsla", "compq", "spx", "djia"]

for subject in subjects:

    for i in range(first_day, last_day+1):
        day = str(i).zfill(2)
        print("Subject: " + subject + ", Day: " + day)
        fix_file(year, month, day, subject)

