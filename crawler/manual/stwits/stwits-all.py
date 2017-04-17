import requests
import settings
import json
import logging
import os
import datetime

def run_collect(company):

    logger.info(company + " started")

    # files and vars
    today = datetime.date(2017, 3, 31)
    yesterday = today - datetime.timedelta(1)
    two_days_ago = today - datetime.timedelta(2)
    file_name = settings.DOWNLOADS_STWITS + "/" + company + "/stwits-" + company + "-" + str(yesterday) + ".csv"
    output = open(file_name, "a")

    max_id = '78805085'


    for j in range(0,200):

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
        logger.info('max_id: ' + str(max_id))

    logger.debug(json.dumps(req, indent=4, sort_keys=True))

    return


##################
# start

# Logging settings
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt='%Y%m%d-%H:%M')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# file
log_file = os.path.dirname(os.path.realpath(__file__)) + "/log/stwits-all.log"
fileHandler = logging.FileHandler(log_file)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

# console
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


logger.info("starting " + os.path.basename(__file__))


#####

# companies = ["msft", "ko", "mcd", "ssnlf", "nflx", "nke", "tsla", "compq", "spx", "djia"]
companies = ["the"]


for company in companies:
    run_collect(company)
    logger.info(company + " finished")


logger.info("ending " + os.path.basename(__file__))


# end
###################



