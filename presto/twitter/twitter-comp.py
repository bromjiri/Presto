# twitter-comp.py
# collects tweets for the specified companies

from tweepy import OAuthHandler
from tweepy import API
from time import sleep
import datetime
import presto.sentan.sentan_twitter as s
import logging
import os

logging.basicConfig(level=logging.INFO, filename="log/twitter-comp.log")


def run_collect(company):

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    two_days_ago = today - datetime.timedelta(2)
    file_name = "output/" + company +"/twitter-" + company + "-" + str(yesterday) + ".csv"
    all = 0
    good = 0

    max_id = 999999999999999999

    # change !!!
    for page in range(0, 440):

        tweets = api.search(q=company, lang="en", count=100, max_id=max_id, until=today)
        output = open(file_name, "a")

        for tweet in tweets:

            text = tweet.text
            created_at = tweet.created_at

            if str(created_at)[0:10] == str(two_days_ago):
                return

            if '@' not in tweet.text:
                if 'http' not in tweet.text:
                    sentimen_value, confidence = s.sentiment(tweet.text)
                    logging.debug(tweet.created_at, tweet.text, sentimen_value, confidence)
                    if confidence * 100 >= 80:
                        output.write('"' + str(created_at) + '","' + text + '","' + sentimen_value + '"\n')
                        good += 1

            all += 1

        max_id = tweet.id


    return


############################


logging.info("starting " + os.path.basename(__file__))

ckey = 'PVeCKgGJ4TEDIXcpDxbwyIjDk'
csecret = 'tMSjmo8XwcoMfnAGXTnx0XZoN5CHb4iQK3RXcYqaJhquAhvwpf'
atoken = '4093147763-RX18hJKAMZD3cfADM0LfyRWOi7wBkjbkfdyGtNH'
asecret = 'XNLizhuodme9MdJQw4dTUSrObL1yu38FJuXg1GUaFAo89'

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = API(auth)


companies = ["microsoft", "cola", "mcdonald", "samsung", "netflix", "nike", "tesla"]
#companies = ["novosibirsk", "krasnoyarsk"]


for company in companies:
    run_collect(company)
    logging.info("finished " + company)
    sleep(900)

logging.info("ending " + os.path.basename(__file__))


