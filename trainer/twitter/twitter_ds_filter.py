# fix newlines

# not used

import settings
import csv
import re
import nltk


inputs = ["pos", "neg"]

for input in inputs:
    try:
        input_path = settings.TRAINER_DATA + "/twitter/stanford_" + input + "_25k.csv"
        output_path = settings.TRAINER_DATA + "/twitter/stanford_" + input + "_25k_new.csv"
        output_file = open(output_path, 'w')

        with open(input_path, "r") as file:
            for post in file:

                # reference
                # ref = re.compile(r"([@])(\w+)\b")
                # my_regex = re.compile(ref)
                # post = my_regex.sub('ref', post)

                # link
                # http = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                # my_regex = re.compile(http)
                # post = my_regex.sub('url', post)

                # number
                post = re.sub("\d+[\d\.]+", "num", post)

                # interpunction
                # post = re.sub("[,\.]", " ", post)

                output_file.write(post)


    except:
        pass


