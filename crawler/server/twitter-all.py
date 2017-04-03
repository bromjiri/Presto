# twitter-comp.py
# collects tweets for the specified companies

from tweepy import OAuthHandler
from tweepy import API
import settings
from time import sleep
import datetime
import os
import myapi

logger = settings.get_logger(os.path.realpath(__file__))

def run_collect(company, max_id):

    logger.info(company + " started")

    # files and vars
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    two_days_ago = today - datetime.timedelta(2)
    file_name = settings.DOWNLOADS_TWITTER + "/" + company + "/twitter-" + company + "-" + str(yesterday) + ".csv"
    dir = os.path.dirname(os.path.realpath(file_name))
    os.makedirs(dir, exist_ok=True)
    output = open(file_name, "a")

    # collect max 18 000
    for page in range(0, 180):

        logger.info("processing: " + str(page) + " of 180")

        try:
            tweets = api.search(q=company, lang="en", count=100, max_id=max_id, until=today)
        except Exception as e:
            logger.error(e)
            continue

        for tweet in tweets:

            # keep yesterday only
            if str(tweet.created_at)[0:10] == str(two_days_ago):
                return 0

            # clean data and save
            logger.debug(str(tweet.created_at) + ', ' + tweet.text)
            output.write('"' + str(tweet.created_at) + '","' + tweet.text + '"\n')

        max_id = tweet.id

    return max_id


def run_company(company):

    max_id = 999999999999999999

    for i in range(0,1):
        logger.info(company + " cycle: " + str(i))
        max_id = run_collect(company, max_id)
        if(max_id == 0):
            logger.info(company + " reached yesterday")
            sleep(900)
            return
        sleep(900)
    return


##################
# start
logger.info("starting " + os.path.basename(__file__))


# Auth settings
auth = OAuthHandler(myapi.CKEY, myapi.CSECRET)
auth.set_access_token(myapi.ATOKEN, myapi.ASECRET)
api = API(auth)


companies = ["cola", "mcdonald", "microsoft",  "netflix", "nike", "samsung", "tesla", "the"]

for company in companies:
    run_company(company)
    logger.info(company + " finished")

logger.info("ending " + os.path.basename(__file__))


# end
###################


