# twitter-all.py
# collects ordinary tweets

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import datetime
import presto.sentan.sentan_twitter as s
import logging
import os

from http.client import IncompleteRead
from requests.packages.urllib3.exceptions import ProtocolError

logging.basicConfig(level=logging.INFO, filename="log/twitter-all.log")

ckey = 'PVeCKgGJ4TEDIXcpDxbwyIjDk'
csecret = 'tMSjmo8XwcoMfnAGXTnx0XZoN5CHb4iQK3RXcYqaJhquAhvwpf'
atoken = '4093147763-RX18hJKAMZD3cfADM0LfyRWOi7wBkjbkfdyGtNH'
asecret = 'XNLizhuodme9MdJQw4dTUSrObL1yu38FJuXg1GUaFAo89'


class MyListener(StreamListener):

    def __init__(self, time_limit=60):
        self.switch = True
        self.start_time = time.time()
        self.limit = time_limit

        file_name = "output/all/twitter-all-" + str(datetime.datetime.now().date()) + ".csv"
        self.output = open(file_name, "a")

        super(MyListener, self).__init__()

    def on_status(self, status):

        if time.time() - self.start_time < self.limit:
            self.do_process(status)
            return True
        else:
            self.switch = False
            return False

    def on_error(self, status_code):
        logging.error(status_code)
        pass


    def do_process(self, status):

        try:
            tweet = status.text
            created = status.created_at

            if '@' not in tweet:
                if 'http' not in tweet:


                    sentimen_value, confidence = s.sentiment(tweet)
                    print(sentimen_value, confidence)
                    if confidence * 100 >= 80:
                        self.output.write('"' + str(created) + '","' + tweet + '","' + sentimen_value + '"\n')

        except Exception:
            pass

        # except KeyError:
        #     pass

        # except IncompleteRead:
        #     pass

        # except ProtocolError:
        #     pass

        return True

    def get_switch(self):
        return self.switch

    def close_file(self):
        self.output.close()


#########################################

logging.info("starting " + os.path.basename(__file__))

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
myListener = MyListener(time_limit=900)

while True:
    try:
        twitterStream = Stream(auth, myListener)
        twitterStream.filter(track=["the"], languages=["en"])

        if not myListener.get_switch():
            logging.info("Ending " + os.path.basename(__file__))
            myListener.close_file()
            break

    except Exception as e:
        logging.error(e)
        continue
