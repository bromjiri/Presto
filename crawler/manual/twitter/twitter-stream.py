# twitter-all.py
# collects ordinary tweets

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import datetime
import crawler.sentan.sentan_twitter as s
import logging
import os


class MyListener(StreamListener):

    def __init__(self, time_limit=60):
        self.switch = True
        self.start_time = time.time()
        self.limit = time_limit

        file_name = os.path.dirname(os.path.realpath(__file__)) + "/output/all/twitter-all-" + str(datetime.datetime.now().date()) + ".csv"
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
        logger.error(status_code)
        pass


    def do_process(self, status):

        try:
            if '@' not in status.text:
                if 'http' not in status.text:

                    sentiment_value, confidence = s.sentiment(status.text)
                    if confidence * 100 >= 80:
                        self.output.write('"' + str(status.created) + '","' + status.text + '","' + sentiment_value + '"\n')
                        logger.debug(str(status.created_at) + ', ' + status.text + ', ' + sentiment_value)

        except Exception:
            pass


        return True

    def get_switch(self):
        return self.switch

    def close_file(self):
        self.output.close()


##################
# start

# Logging settings
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt='%Y%m%d-%H:%M')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# file
log_file = os.path.dirname(os.path.realpath(__file__)) + "/log/twitter-comp.log"
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
myListener = MyListener(time_limit=900)


#####

while True:
    try:
        twitterStream = Stream(auth, myListener)
        twitterStream.filter(track=["the"], languages=["en"])

        if not myListener.get_switch():
            logging.info("Ending " + os.path.basename(__file__))
            print("Ending " + os.path.basename(__file__))
            myListener.close_file()
            break

    except Exception as e:
        logger.error(e)
        continue


logger.info("ending " + os.path.basename(__file__))

# end
###################