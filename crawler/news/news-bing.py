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

    logger.info(subject + " search")

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    file_json = settings.DOWNLOADS + "/news/bing/" + subject + "/news-" + subject + "-" + str(yesterday) + ".json"
    dir = os.path.dirname(os.path.realpath(file_json))
    os.makedirs(dir, exist_ok=True)
    write_json = open(file_json, 'w')

    url = 'https://api.cognitive.microsoft.com/bing/v5.0/news/search'

    params = {
        'q': subject,
        'count': '100',
        'offset': '0',
        'mkt': 'en-us',
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


def download_json_category():

    logger.info("category search")
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    file_json = settings.DOWNLOADS + "/news/bing/the/news-the-" + str(yesterday) + ".json"
    dir = os.path.dirname(os.path.realpath(file_json))
    os.makedirs(dir, exist_ok=True)
    write_json = open(file_json, 'w')

    url = 'https://api.cognitive.microsoft.com/bing/v5.0/news/'

    params = {
        'count': '100',
        'offset': '0',
        'mkt': 'en-us',
        'freshness': 'Day',
        'category': 'Business',
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


def get_links(body):
    # file = settings.DOWNLOADS + "/news/bing/tesla/news-tesla-2016-12-28.json"
    # test = open(file, "r")
    # body = ""
    # for x in test:
    #     body += x
    #
    # body = json.loads(body)

    link_set = set()
    for value in body['value']:
        link_set.add(value['url'])

    return link_set


def process_articles(link_set, subject):

    # files and vars
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    file_comp = settings.DOWNLOADS_NEWS + "/bing/" + subject + "/news-" + subject + "-" + str(yesterday) + ".csv"
    dir = os.path.dirname(os.path.realpath(file_comp))
    os.makedirs(dir, exist_ok=True)
    write_comp = open(file_comp, 'w')
    iter = 1

    for link in link_set:

        try:
            source_code = requests.get(link).text
            soup = BeautifulSoup(source_code, "lxml")

            for paragraph in soup.findAll(['p']):
                write_comp.write(paragraph.text)

            logger.info(subject + " " + str(iter) + " of " + str(len(link_set)))
            iter += 1


        except Exception as e:
            logger.error(e)
            pass

        write_comp.write("\n*****\n")

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

subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]
#subjects = ["the"]


for subject in subjects:

    if subject == "the":
        body = download_json_category()
    else:
        body = download_json(subject)

    link_set = get_links(body)
    process_articles(link_set, subject)