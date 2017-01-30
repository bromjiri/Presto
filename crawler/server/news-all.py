import requests
import settings
import datetime
from nltk.tokenize import sent_tokenize
import os
from bs4 import BeautifulSoup

logger = settings.get_logger(os.path.realpath(__file__))


def fileToSet(fileName):
    feeds = set()
    with open(fileName, 'rt') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('#'):
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
    file_comp = settings.DOWNLOADS_NEWS + "/comp/news-comp-" + str(today) + ".csv"
    dir = os.path.dirname(os.path.realpath(file_comp))
    os.makedirs(dir, exist_ok=True)
    write_comp = open(file_comp, 'w')

    file_the = settings.DOWNLOADS_NEWS + "/the/news-the-" + str(today) + ".csv"
    dir = os.path.dirname(os.path.realpath(file_the))
    os.makedirs(dir, exist_ok=True)
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
logger.info("starting " + os.path.basename(__file__))


feeds = fileToSet(os.path.dirname(os.path.realpath(__file__)) + "data/feeds.txt")
articles = getArticleLinks(feeds)
companies = ["microsoft", "coca-cola", "mcdonald", "samsung", "netflix", "nike", "tesla"]

processArticles(articles, companies)


logger.info("ending " + os.path.basename(__file__))
# end
###################