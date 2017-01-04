import os
import settings
import requests
import logging
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize


def get_sentences(date, subject):

    # files and vars
    input_file = settings.GOOGLE_HTML + "/" + subject + "/" + date + "/" + subject + "_old_links_" + date + ".txt"
    output_file = settings.GOOGLE_HTML + "/" + subject + "/" + date + "/" + subject + "_old_sentences_" + date + ".txt"
    link_set = open(input_file, 'r')
    sentences_file = open(output_file, 'w')
    iter = 1

    for link in link_set:

        try:
            source_code = requests.get(link).text
            soup = BeautifulSoup(source_code, "lxml")

            for post in soup.findAll(['p']):
                sentences = sent_tokenize(post.text)

                for sentence in sentences:
                    if subject in sentence.lower():
                        sentences_file.write(sentence.lower().strip() + '\n')

            #logger.info(str(iter) + " of " + str(len(link_set)))
            iter += 1


        except Exception as e:
            logger.error(e)
            pass

    sentences_file.close()

    return True



##################
# start

# Logging settings
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt='%Y%m%d-%H:%M')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# console
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


logger.info("starting " + os.path.basename(__file__))


#####

year = "2016"
month = "12"
first_day = 1
last_day = 31
#subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]
subjects = ["microsoft"]



for subject in subjects:
    for i in range(first_day, last_day+1):
        day = str(i).zfill(2)
        date = year + "-" + month + "-" + day
        get_sentences(date, subject)
        print(date)


logger.info("ending " + os.path.basename(__file__))


# end
###################