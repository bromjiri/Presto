# download twitter data

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import presto.sentan.sentan_twitter as s

from http.client import IncompleteRead
from requests.packages.urllib3.exceptions import ProtocolError


ckey = 'PVeCKgGJ4TEDIXcpDxbwyIjDk'
csecret = 'tMSjmo8XwcoMfnAGXTnx0XZoN5CHb4iQK3RXcYqaJhquAhvwpf'
atoken = '4093147763-RX18hJKAMZD3cfADM0LfyRWOi7wBkjbkfdyGtNH'
asecret = 'XNLizhuodme9MdJQw4dTUSrObL1yu38FJuXg1GUaFAo89'


class MyListener(StreamListener):

    def __init__(self, time_limit=60):
        self.switch = True
        self.start_time = time.time()
        self.limit = time_limit
        super(MyListener, self).__init__()

    def on_status(self, status):

        if time.time() - self.start_time < self.limit:
            self.do_process(status)
            return True
        else:
            self.switch = False
            return False

    def on_error(self, status_code):
        print(status_code)

    @staticmethod
    def do_process(self, status):

        try:
            tweet = status.text

            #if 'afsagasg' not in tweet:


            sentimen_value, confidence = s.sentiment(tweet)
            print(tweet, sentimen_value, confidence)

            # if confidence * 100 >= 80:
            #     output = open("twitter-out.txt", "a")
            #     output.write(sentimen_value)
            #     output.write('\n')
            #     output.close()

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


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
myListener = MyListener(time_limit=600)

while True:
    try:
        twitterStream = Stream(auth, myListener)
        twitterStream.filter(track=["the"], languages=["en"])

        if not myListener.get_switch():
            print("break")
            break

    except Exception:
        # Oh well, reconnect and keep trucking
        continue
