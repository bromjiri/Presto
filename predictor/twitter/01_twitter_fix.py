# fix newlines
import settings

def fix_file(day, month, subject):

    output_file_path = settings.DOWNLOADS_TWITTER + "/" + subject + "/twitter-" + subject + "-" + year + "-" + month + "-" + day + "-fix.csv"
    output_file = open(output_file_path, "w")

    input_file_path = settings.DOWNLOADS_TWITTER + "/" + subject + "/twitter-" + subject + "-" + year + "-" + month + "-" + day + ".csv"
    input_file = open(input_file_path, "r")
    # input_list = input_file.readlines()
    # unique_list = list(set(input_list))
    output_list = list()
    line = ""
    for row in input_file:
        if not ("\"pos\"" in row or "\"neg\"" in row):

        # try:
        #     last_char = row.strip()[-1]
        # except:
        #     continue
        #
        # if last_char != "\"":
            line += row.rstrip()
        else:
            line += row
            output_list.append(line)
            line = ""


    unique_list = list(set(output_list))
    for line in unique_list:
        output_file.write(line)

    output_file.close()


year = "2017"
month = "01"
first_day = 21
last_day = 29
subjects = ["microsoft", "cola", "mcdonald", "samsung", "netflix", "nike", "tesla", "the"]

for subject in subjects:

    for i in range(first_day, last_day+1):
        day = str(i).zfill(2)
        print("Subject: " + subject + ", Day: " + day)
        fix_file(day, month, subject)

