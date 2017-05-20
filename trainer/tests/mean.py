import settings
import csv
from os import listdir
from os.path import isfile, join



COLUMNS = 7

dataset = "twitter"
subject = "tesla"
my_type = "stop-pos"

# mypath = settings.TRAINER + "/tests/output/" + dataset + "/" + my_type
mypath = settings.PREDICTOR_PREDICTION + '/' + dataset + '/' + subject + '/'

files_list = list()
for f in listdir(mypath):
    file_path = join(mypath, f)
    if isfile(file_path):
        files_list.append(file_path)

for f in files_list:
    if "s" in f:
        input_file_path = f

        with open(input_file_path, "r") as test_file:
            reader = csv.reader(test_file, delimiter=',')

            # skip already processed
            for x in reader: pass
            if x[0] == "":
                print("skip: " + input_file_path)
                continue

            # prepare dict
            sum = dict()
            for i in range(1, COLUMNS):
                sum[i] = 0.0


            test_file.seek(0)
            count = 0
            for row in reader:

                if "2017" in row[0]:
                    print("skip: " + str(row))
                    continue

                count += 1
                for i in range(1,COLUMNS):
                    # print(row, i)
                    sum[i] += float(row[i])


        with open(input_file_path, "a") as test_file:
            print(count)
            mean = dict()
            new_line = "mean"
            for i in range(1, COLUMNS):
                mean[i] = round(sum[i]/count, 2)
                new_line += " & " + str(mean[i])

            new_line += "\n"
            print("new_line: " + new_line)
            test_file.write(new_line)
