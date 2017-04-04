import settings
import csv
import os
import trainer.sentan as st


from datetime import timedelta, date

logger = settings.get_logger(os.path.realpath(__file__))


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)

class Counter:
    def __init__(self):
        self.counter_list = [0.6, 0.8, 1.0]
        self.pos_dict = dict([(res, 0) for res in self.counter_list])
        self.tot_dict = dict([(res, 0) for res in self.counter_list])

    def inc(self, sent, conf):
        for limit in self.counter_list:
            if conf >= limit:
                self.tot_dict[limit] +=1
                if sent == "pos":
                    self.pos_dict[limit] += 1

    def get_percentage(self):
        per_dict = dict()
        for limit in self.counter_list:
            if self.tot_dict[limit] < 10:
                per_dict[limit] = 0
            else:
                per_dict[limit] = self.pos_dict[limit] / self.tot_dict[limit]
                per_dict[limit] = "{:.2f}".format(per_dict[limit] * 100)

        # logger.info("get_percentage")
        # logger.info(self.tot_dict)
        return per_dict

class CounterStwits():
    def __init__(self):

        # initialize output
        output_file = settings.PREDICTOR_SENTIMENT + "/" + source + "/" + source + "-sent-" + subject + ".csv"
        dir = os.path.dirname(os.path.realpath(output_file))
        os.makedirs(dir, exist_ok=True)
        output = open(output_file, "a")
        self.writer = csv.writer(output, delimiter=',')
        self.writer.writerow(["date", "sent0.6", "sent0.8", "sent1.0", "comb0.6",
                        "comb0.6", "comb0.8", "comb1.0", "bull"])

    def init_counter(self):
        self.counter = Counter()
        self.part_counter = Counter()

        self.stwits_bull = 0
        self.stwits_tot = 0

    def bull_inc(self, sent):
        self.stwits_tot += 1
        if sent == "Bullish":
            self.stwits_bull += 1

    def get_percentage_bull(self):
        if self.stwits_tot < 3:
            per_bull = 0
        else:
            per_bull = self.stwits_bull / self.stwits_tot
            per_bull = "{:.2f}".format(per_bull * 100)
        return per_bull

    def get_comb(self):

        for key in self.part_counter.counter_list:
            # logger.info("tot_dict " + str(self.part_counter.tot_dict[key]))
            # logger.info(self.stwits_tot)
            self.part_counter.tot_dict[key] += self.stwits_tot
            self.part_counter.pos_dict[key] += self.stwits_bull
            # logger.info(self.part_counter.tot_dict[key])

        return self.part_counter.get_percentage()


    def count_day(self, day, subject):
        self.init_counter()

        stwits_stock = {"coca-cola": "ko", "mcdonalds": "mcd", "microsoft": "msft", "netflix": "nflx", "nike": "nke",
                        "samsung": "ssnlf", "tesla": "tsla", "compq": "compq", "djia": "djia", "spx": "spx"}
        new_subject = stwits_stock[subject]
        input_file = settings.DOWNLOADS_STWITS_FINAL + "/" + new_subject + "/" + "stwits-" + new_subject + "-" + day + "-fix.csv"

        with open(input_file, "r") as stwi:
            reader = csv.reader(stwi, delimiter=',')
            for row in reader:
                try:
                    sent, conf = st.sent_stwits(row[2].strip())
                    self.counter.inc(sent, conf)
                    if row[1] != "none":
                        self.bull_inc(row[1])
                    else:
                        self.part_counter.inc(sent, conf)
                except Exception as e:
                    logger.error(e)
                    continue

        per_dict = self.counter.get_percentage()
        per_comb_dict = self.get_comb()
        per_bull = self.get_percentage_bull()

        output_list = [per_dict[key] for key in self.counter.counter_list] + \
                      [per_comb_dict[key] for key in self.counter.counter_list] + [per_bull]

        logger.info(output_list)


def count_twitter(day, subject):

    if subject == "coca-cola":
        new_subject = "cola"
    elif subject == "mcdonalds":
        new_subject = "mcdonald"
    else:
        new_subject = subject

    input_file = settings.DOWNLOADS_TWITTER_FINAL + "/" + new_subject + "/" + "twitter-" + new_subject + "-" + day + "-fix.csv"
    counter = Counter()

    with open(input_file, "r") as twi:
        reader = csv.reader(twi, delimiter=',')
        head = [row for row in reader][:twi_max]
        for row in head:
            try:
                sent, conf = st.sent_twitter(row[1].strip())
                counter.inc(sent, conf)
            except Exception as e:
                logger.error(e)
                continue

    per_dict = counter.get_percentage()
    return per_dict


def count_news(day, subject):
    pos = 0
    total = 0

    input_file = settings.DOWNLOADS_NEWS + "/final/" + subject + "/news-" + subject + "-" + day + "-final.csv"
    res_dict_list = ["pos0.6", "total0.6", "pos0.8", "total0.8", "pos1.0", "total1.0"]
    res_dict = dict([(res, 0) for res in res_dict_list])

    with open(input_file, "r") as file:
        for row in file:
            total += 1
            try:
                sent, conf = st.sent_news(row.strip())
            except Exception as e:
                logger.error(e)
                continue

            if (sent == "pos"):
                pos += 1




# def count_sent(day, subject):
#
#     if source == "twitter":
#         per_dict = count_twitter(day, subject)
#     elif source == "stwits":
#         pos, total = count_stwits(day, subject)
#     else:
#         pos, total = count_news(day, subject)
#
#     logger.info(day, per_dict)
#
#     for key in per_dict:
#         output_file = settings.PREDICTOR_SENTIMENT + "/" + source + "/" + source + "-sent-" + subject + "-" + str(key) + ".csv"
#         output = open(output_file, "a")
#         writer = csv.writer(output, delimiter=',')
#         writer.writerow([day, per_dict[key]])



###############
#### start ####
###############

# vars
source = "stwits"
start_date = date(2016, 11, 1)
end_date = date(2017, 3, 31)
twi_max = 5000


# subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]
# subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the", "djia", "compq", "spx"]
subjects = ["coca-cola"]

for subject in subjects:
    logger.info(subject)


    counter_stwits = CounterStwits()

    for single_date in daterange(start_date, end_date):
        day = single_date.strftime("%Y-%m-%d")
        try:
            if source == "twitter":
                count_twitter(day, subject)
            elif source == "stwits":
                counter_stwits.count_day(day, subject)
            else:
                count_news(day, subject)
        except Exception as e:
            logger.error(e)
            continue
