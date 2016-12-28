import myapi
import requests
import settings
import logging
import datetime
import os
import json
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize


def download_json(subject):

    today = datetime.date.today()
    file_json = settings.DOWNLOADS + "/news/bing/" + subject + "/news-" + subject + "-" + str(today) + ".json"
    write_json = open(file_json, 'w')

    url = 'https://api.cognitive.microsoft.com/bing/v5.0/news/search'

    params = {
        'q': subject,
        'count': '100',
        'offset': '0',
        'mkt': 'en-us',
        'safeSearch': 'Moderate',
        'freshness' : 'Day',
    }

    headers = {
        'Ocp-Apim-Subscription-Key': myapi.BING_KEY,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
    }

    try:
        res = requests.get(url, params=params, headers=headers)
        write_json.write(res.text)

    except Exception as e:
        logger.error(e)

    return res.json()


def get_links():
    file = settings.DOWNLOADS + "/news/bing/tesla/news-tesla-2016-12-28.json"
    test = open(file, "r")
    body = ""
    for x in test:
        body += x

    body = json.loads(body)

    link_set = set()
    for value in body['value']:
        link_set.add(value['url'])

    return link_set


def process_articles(link_set, subject):

    # files and vars
    today = datetime.date.today()
    file_comp = settings.DOWNLOADS + "/news/bing/" + subject + "/news-" + subject + "-" + str(today) + ".csv"
    # file_the = os.path.dirname(os.path.realpath(__file__)) + "/output/the/news-the-" + str(today) + ".csv"
    write_comp = open(file_comp, 'w')
    # write_the = open(file_the, 'w')
    iter = 1

    for link in link_set:

        try:
            source_code = requests.get(link).text
            soup = BeautifulSoup(source_code, "lxml")

            for paragraph in soup.findAll(['p']):
                write_comp.write(paragraph.text)

            logger.info(str(iter) + " of " + str(len(link_set)))
            iter += 1


        except Exception as e:
            logger.error(e)
            pass

        write_comp.write("\n*****\n")

    # write_the.close()
    write_comp.close()

    return True

##################
# start

# Logging settings
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt='%Y%m%d-%H:%M')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# file
log_file = os.path.dirname(os.path.realpath(__file__)) + "/log/news-bing.log"
fileHandler = logging.FileHandler(log_file)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

# console
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


logger.info("starting " + os.path.basename(__file__))


#####

#body = download_json("tesla")
link_set = get_links()
process_articles(link_set, "tesla")