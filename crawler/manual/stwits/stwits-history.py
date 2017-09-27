import requests
import settings
import json
import logging
import os
import datetime
from time import sleep

logger = settings.get_logger(os.path.realpath(__file__))

def run_collect(company, total_req):

    logger.info(company + " started")

    # files and vars
    # today = datetime.date.today()
    # yesterday = today - datetime.timedelta(1)
    # two_days_ago = today - datetime.timedelta(2)
    # file_name = settings.DOWNLOADS_STWITS + "/" + company + "/stwits-" + company + "-" + str(yesterday) + ".csv"
    # dir = os.path.dirname(os.path.realpath(file_name))
    # os.makedirs(dir, exist_ok=True)
    # output = open(file_name, "a")

    max_id = '92399116'
    previous_date = datetime.date.today()

    for j in range(0,10000):
        total_req +=1
        if total_req == 200:
            sleep(3600)
            total_req = 1

        logger.info(company + ": " + str(j))

        if(company == "the"):
            url = 'https://api.stocktwits.com/api/2/streams/suggested.json?max=' + str(max_id)
        else:
            url = 'https://api.stocktwits.com/api/2/streams/symbol/' + company + '.json?max=' + str(max_id)
        try:
            req = requests.get(url).json()
        except Exception as e:
            print(e)
            sleep(3600)

        if req['response']['status'] == 429:
            logger.error("sleeping 429")
            sleep(3600)
            continue

        for i in range(0,30):

            try:
                if (req['messages'][i]['entities']['sentiment'] is not None):
                    sentiment = req['messages'][i]['entities']['sentiment']['basic']
                else:
                    sentiment = "none"
                created_at = req['messages'][i]['created_at']
                text = req['messages'][i]['body']
            except Exception as e:
                print(e)
                continue

            created_date = str(created_at)[0:10]
            if created_date != previous_date:
                previous_date = created_date
                logger.info("date: " + previous_date)

            if "2017-04" in created_date:
                return total_req

            file_name = settings.DOWNLOADS_STWITS + "/" + company + "/stwits-" + company + "-" + created_date + "-hist.csv"
            output = open(file_name, "a")
            logger.debug(created_at + ', ' + sentiment + ', ' + text)
            output.write('"' + created_at + '","' + sentiment + '","' + text + '"\n')

        max_id = req['cursor']['max']
        logger.info("max_id: " + str(max_id))

    # logger.debug(json.dumps(req, indent=4, sort_keys=True))

    return total_req


##################
# start
logger.info("starting " + os.path.basename(__file__))


# companies = ["msft", "ko", "mcd", "ssnlf", "nflx", "nke", "tsla", "compq", "spx", "djia", "the"]
companies = ["the"]


total_req = 1

for company in companies:
    total_req = run_collect(company, total_req)
    logger.info(company + " finished")


logger.info("ending " + os.path.basename(__file__))
# end
###################



