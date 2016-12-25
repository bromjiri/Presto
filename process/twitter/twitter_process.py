import csv


MONTH = "11"
SUBJECT = "cola"


def process_day(day):

    input_file = "../../presto/downloads/twitter/" + SUBJECT + "/twitter-" + SUBJECT + "-2016-" + MONTH + "-" + day + "-fix.csv"


    pos = 0
    neg = 0
    total = 0

    with open(input_file, "r") as twi:
        reader = csv.reader(twi, delimiter=',')
        for row in reader:
            total+=1
            try:
                sent = row[-1]
            except:
                print("error: " + str(row))
                pass

            if("pos" in sent):
                pos+=1
            elif("neg" in sent):
                neg+=1
            else:
                print("not recognized sentiment" + str(row))

    pos_per = pos/total
    print("day: " + str(day) + " pos: " + "{:.2f}".format(pos_per*100))
    return "{:.2f}".format(pos_per*100)


### start processing ###

subjects = ["microsoft", "cola", "mcdonald", "samsung", "netflix", "nike", "tesla", "the"]

output_file = "../sentiment/twitter/twitter-sent-" + SUBJECT + "-2016-" + MONTH + ".csv"
output =  open(output_file, "w")
writer = csv.writer(output, delimiter=',')

for i in range(1,31):
    day = str(i).zfill(2)
    pos_day = process_day(day)
    writer.writerow([MONTH, day, pos_day])

output.close()