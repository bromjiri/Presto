import requests
import logging
import datetime
from nltk.tokenize import sent_tokenize
import os
from bs4 import BeautifulSoup




def getArticleLinks(date):
    linkSet = set()

    fileName = date + "/links.txt"

    with open(fileName, 'rt') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('#'):
                linkSet.add(line.replace('\n', ''))

    return linkSet

def processArticles(link_set, companies, date):

    # files and vars
    file_comp = os.path.dirname(os.path.realpath(__file__)) + "/output/comp/news-comp-" + date + ".csv"
    file_the = os.path.dirname(os.path.realpath(__file__)) + "/output/the/news-the-" + date + ".csv"
    write_comp = open(file_comp, 'w')
    write_the = open(file_the, 'w')
    iter = 1

    for link in link_set:

        try:
            source_code = requests.get(link).text
            soup = BeautifulSoup(source_code, "lxml")

            for post in soup.findAll(['p']):
                logger.debug(post.text)
                sentences = sent_tokenize(post.text)

                for sentence in sentences:
                    write_the.write(sentence.lower().strip() + '\n')

                    for company in companies:
                        if company in sentence.lower():
                            write_comp.write('"' + company + '","' + sentence + '"\n')
                            logger.debug('"' + company + '","' + sentence + '"\n')

            logger.info(str(iter) + " of " + str(len(link_set)))
            iter += 1


        except Exception as e:
            logger.error(e)
            pass


    write_the.close()
    write_comp.close()

    return True

##################
# start

# Logging settings
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt='%Y%m%d-%H:%M')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# file
# log_file = os.path.dirname(os.path.realpath(__file__)) + "/log/news-comp.log"
# fileHandler = logging.FileHandler(log_file)
# fileHandler.setFormatter(logFormatter)
# logger.addHandler(fileHandler)

# console
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


logger.info("starting " + os.path.basename(__file__))


#####

date = "2016-11-12"
articles = getArticleLinks(date)
companies = ["microsoft", "coca-cola", "mcdonald", "samsung", "netflix", "nike", "tesla"]

processArticles(articles, companies, date)


logger.info("ending " + os.path.basename(__file__))


# end
###################