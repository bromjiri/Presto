import requests
import logging
import datetime
from nltk.tokenize import sent_tokenize
import os
from bs4 import BeautifulSoup


def fileToSet(fileName):
    feeds = set()
    with open(fileName, 'rt') as f:
        for line in f:
            feeds.add(line.replace('\n', ''))
    return feeds


def getArticleLinks(feeds):
    linkSet = set()
    for feed in feeds:

        try:
            sourceCode = requests.get(feed).text
            soup = BeautifulSoup(sourceCode, "xml")

            for item in soup.findAll('item'):
                link = item.find('link').text
                linkSet.add(link)

        except Exception as e:
            logger.error(str(e))
            pass

    return linkSet

def processArticles(link_set, companies):

    # files and vars
    today = datetime.date.today()
    file_comp = os.path.dirname(os.path.realpath(__file__)) + "/output/comp/twitter-comp-" + str(today) + ".csv"
    file_the = os.path.dirname(os.path.realpath(__file__)) + "/output/the/twitter-the-" + str(today) + ".csv"
    write_comp = open(file_comp, 'a')
    write_the = open(file_the, 'a')
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
log_file = os.path.dirname(os.path.realpath(__file__)) + "/log/news-comp.log"
fileHandler = logging.FileHandler(log_file)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

# console
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


logger.info("starting " + os.path.basename(__file__))


#####

feeds = fileToSet("feeds.txt")
articles = getArticleLinks(feeds)
companies = ["microsoft", "coca-cola", "mcdonald", "samsung", "netflix", "nike", "tesla"]

processArticles(articles, companies)


logger.info("ending " + os.path.basename(__file__))


# end
###################