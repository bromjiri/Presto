import myapi
import requests
import settings
import datetime
import os
from bs4 import BeautifulSoup

logger = settings.get_logger(os.path.realpath(__file__))

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
logger.info("starting " + os.path.basename(__file__))


subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]

for subject in subjects:

    if subject == "the":
        body = download_json_category()
    else:
        body = download_json(subject)

    link_set = get_links(body)
    process_articles(link_set, subject)


logger.info("ending " + os.path.basename(__file__))
# end
###################