import requests
import settings
import json
import logging
import os
import datetime

logger = settings.get_logger(os.path.realpath(__file__))

def run_collect(company):

    logger.info(company + " started")

    # files and vars
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    two_days_ago = today - datetime.timedelta(2)
    file_name = settings.DOWNLOADS_STWITS + "/" + company + "/stwits-" + company + "-" + str(yesterday) + ".csv"
    dir = os.path.dirname(os.path.realpath(file_name))
    os.makedirs(dir, exist_ok=True)
    output = open(file_name, "a")

    max_id = '99999999'


    for j in range(0,100):

        logger.info("processing: " + str(j) + " of 100")

        if(company == "the"):
            url = 'https://api.stocktwits.com/api/2/streams/suggested.json?max=' + str(max_id)
        else:
            url = 'https://api.stocktwits.com/api/2/streams/symbol/' + company + '.json?max=' + str(max_id)

        req = requests.get(url).json()

        for i in range(0,30):

            if (req['messages'][i]['entities']['sentiment'] is not None):
                sentiment = req['messages'][i]['entities']['sentiment']['basic']
            else:
                sentiment = "none"
            created_at = req['messages'][i]['created_at']
            text = req['messages'][i]['body']


            # keep yesterday only
            if str(created_at)[0:10] == str(two_days_ago):
                return

            logger.debug(created_at + ', ' + sentiment + ', ' + text)
            output.write('"' + created_at + '","' + sentiment + '","' + text + '"\n')

        max_id = req['cursor']['max']
        logger.debug('max_id: ' + str(max_id))

    logger.debug(json.dumps(req, indent=4, sort_keys=True))

    return


##################
# start
logger.info("starting " + os.path.basename(__file__))


companies = ["msft", "ko", "mcd", "ssnlf", "nflx", "nke", "tsla", "compq", "spx", "djia", "the"]
#companies = ["msft"]

for company in companies:
    run_collect(company)
    logger.info(company + " finished")


logger.info("ending " + os.path.basename(__file__))
# end
###################



