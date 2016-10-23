# twitter-comp.py
# collects tweets for the specified companies

from tweepy import OAuthHandler
from tweepy import API
from time import sleep
import datetime
import presto.sentan.sentan_twitter as s
import logging
import os


def run_collect(company):

    logger.info(company + " started")

    # files and vars
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    two_days_ago = today - datetime.timedelta(2)
    file_name = os.path.dirname(os.path.realpath(__file__)) + "/output/all/twitter-all-" + str(yesterday) + ".csv"
    output = open(file_name, "a")
    good = 0

    max_id = 999999999999999999

    # collect max 44 000
    for page in range(0, 440):

        logger.info("processing: " + str(page) + " of 440")

        try:
            tweets = api.search(q=company, lang="en", count=100, max_id=max_id, until=today)
        except Exception as e:
            logger.error(e)
            continue

        for tweet in tweets:

            # keep yesterday only
            if str(tweet.created_at)[0:10] == str(two_days_ago):
                return

            # clean data and save
            if '@' not in tweet.text:
                if 'http' not in tweet.text:
                    sentiment_value, confidence = s.sentiment(tweet.text)
                    if confidence * 100 >= 80:
                        logger.debug(str(tweet.created_at) + ', ' + tweet.text + ', ' + sentiment_value)
                        output.write('"' + str(tweet.created_at) + '","' + tweet.text + '","' + sentiment_value + '"\n')
                        good += 1

        max_id = tweet.id

    return


##################
# start

# Logging settings
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt='%Y%m%d-%H:%M')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# file
log_file = os.path.dirname(os.path.realpath(__file__)) + "/log/twitter-all.log"
fileHandler = logging.FileHandler(log_file)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

# console
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


logger.info("starting " + os.path.basename(__file__))


#####


# Auth settings
ckey = 'PVeCKgGJ4TEDIXcpDxbwyIjDk'
csecret = 'tMSjmo8XwcoMfnAGXTnx0XZoN5CHb4iQK3RXcYqaJhquAhvwpf'
atoken = '4093147763-RX18hJKAMZD3cfADM0LfyRWOi7wBkjbkfdyGtNH'
asecret = 'XNLizhuodme9MdJQw4dTUSrObL1yu38FJuXg1GUaFAo89'

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = API(auth)


#####


#companies = ["microsoft", "cola", "mcdonald", "samsung", "netflix", "nike", "tesla"]
companies = ["the"]


for company in companies:
    run_collect(company)
    #logger.info(company + " finished")
    #sleep(900)

logger.info("ending " + os.path.basename(__file__))


# end
###################


