# fix newlines
import settings

def fix_file(day, month, subject):

    output_file = settings.DOWNLOADS_TWITTER + "/" + subject + "/twitter-" + subject + "-2016-" + month + "-" + day + "-fix.csv"
    write_file = open(output_file, "w")

    input_file = settings.DOWNLOADS_TWITTER + "/" + subject + "/twitter-" + subject + "-2016-" + month + "-" + day + ".csv"

    with open(input_file, "rt") as twi:
        for row in twi:

            if not ("\"pos\"" in row or "\"neg\"" in row):
                res = row.rstrip()
                write_file.write(res)
            else:
                write_file.write(row)

    write_file.close()



month = "12"
first_day = 1
last_day = 20
subjects = ["microsoft", "cola", "mcdonald", "samsung", "netflix", "nike", "tesla", "the"]

for subject in subjects:

    for i in range(first_day, last_day+1):
        day = str(i).zfill(2)
        print("Subject: " + subject + ", Day: " + day)
        fix_file(day, month, subject)

