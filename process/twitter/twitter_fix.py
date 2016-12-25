# fix newlines

MONTH = "11"
SUBJECT = "cola"


def fix_file(day):

    output_file = "../../presto/downloads/twitter/" + SUBJECT + "/twitter-" + SUBJECT + "-2016-" + MONTH + "-" + day + "-fix.csv"
    write_file = open(output_file, "w")

    input_file = "../../presto/downloads/twitter/" + SUBJECT + "/twitter-" + SUBJECT + "-2016-11-" + day + ".csv"

    with open(input_file, "rt") as twi:
        for row in twi:

            if not ("\"pos\"" in row or "\"neg\"" in row):
                res = row.rstrip()
                write_file.write(res)
            else:
                write_file.write(row)

    write_file.close()



for i in range(1,31):
    day = str(i).zfill(2)
    fix_file(day)

