# fix newlines
import settings
import os

def fix_file(year, month, day, subject):

    try:

        date = year + "-" + month + "-" + day

        # define i/o
        try:
            input_file_path = settings.DOWNLOADS_STWITS + "/" + subject + "/stwits-" + subject + "-" + year + "-" + month + "-" + day + ".csv"
            input_file = open(input_file_path, "r")
            normal = True
        except:
            print("no normal for " + date)
            normal = False

        try:
            input_file_hist_path = settings.DOWNLOADS_STWITS + "/" + subject + "/stwits-" + subject + "-" + year + "-" + month + "-" + day + "-hist.csv"
            input_file_hist = open(input_file_hist_path, "r")
            hist = True
        except:
            print("no hist for " + date)
            hist = False

        if normal == False and hist == False:
            return

        output_file_path = settings.DOWNLOADS_STWITS_FINAL + "/" + subject + "/stwits-" + subject + "-" + year + "-" + month + "-" + day + "-fix.csv"
        dir = os.path.dirname(os.path.realpath(output_file_path))
        os.makedirs(dir, exist_ok=True)
        output_file = open(output_file_path, "w")

        output_list = list()

        # cycle normal
        if normal == True:
            input_file = input_file.readlines()
            previous = input_file[0].strip()

            for row in input_file[1:]:

                if row.strip() == "":
                    continue

                if not date in row:
                    previous += row.strip()
                else:
                    output_list.append(previous + "\n")
                    previous = row.strip()

        # cycle hist
        if hist == True:
            input_file_hist = input_file_hist.readlines()
            previous = input_file_hist[0].strip()

            for row in input_file_hist[1:]:

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

    except Exception as e:
        print(e)
        pass


periods = [["2017", "09"], ["2017", "10"]]
# periods = [["2017", "01"]]
first_day = 1
last_day = 31
# subjects = ["msft", "ko", "mcd", "ssnlf", "nflx", "nke", "tsla", "compq", "spx", "djia", "the"]
subjects = ["msft", "ko", "nflx", "tsla"]


for period in periods:

    year = period[0]
    month = period[1]

    for subject in subjects:

        for i in range(first_day, last_day+1):
            day = str(i).zfill(2)
            print("Subject: " + subject + ", Day: " + day)
            fix_file(year, month, day, subject)

