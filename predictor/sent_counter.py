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
            if self.tot_dict[limit] < 1:
                per_dict[limit] = 50
            else:
                per_dict[limit] = self.pos_dict[limit] / self.tot_dict[limit]
                per_dict[limit] = "{:.2f}".format(per_dict[limit] * 100)

        return per_dict


def get_writer(source, subject):
    output_file = settings.PREDICTOR_SENTIMENT + "/" + source + "/" + source + "-sent-" + subject + ".csv"
    dir = os.path.dirname(os.path.realpath(output_file))
    os.makedirs(dir, exist_ok=True)
    output = open(output_file, "a")
    return csv.writer(output, delimiter=',')

class CounterStwits():
    def __init__(self, subject):

        self.subject = subject
        # initialize output
        self.writer = get_writer("stwits", subject)
        self.writer.writerow(["Date", "Sent0.6", "Tot0.6", "Sent0.8", "Tot0.8", "Sent1.0", "Tot1.0"])
        self.comb_writer = get_writer("stwits-comb", subject)
        self.comb_writer.writerow(["Date", "Sent0.6", "Tot0.6", "Sent0.8", "Tot0.8", "Sent1.0", "Tot1.0", "Bull", "Tot_bull"])

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
        if self.stwits_tot < 1:
            per_bull = -1
        else:
            per_bull = self.stwits_bull / self.stwits_tot
            per_bull = "{:.2f}".format(per_bull * 100)
        return per_bull

    def add_bull(self, part_counter):

        for key in part_counter.counter_list:
            # logger.info("tot_dict " + str(self.part_counter.tot_dict[key]))
            # logger.info(self.stwits_tot)
            part_counter.tot_dict[key] += self.stwits_tot
            part_counter.pos_dict[key] += self.stwits_bull
            # logger.info(self.part_counter.tot_dict[key])

    def count_day(self, day):
        self.init_counter()

        stwits_stock = {"coca-cola": "ko", "mcdonalds": "mcd", "microsoft": "msft", "netflix": "nflx", "nike": "nke",
                        "samsung": "ssnlf", "tesla": "tsla", "compq": "compq", "djia": "djia", "spx": "spx", "the": "the"}
        new_subject = stwits_stock[self.subject]
        input_file = settings.DOWNLOADS_STWITS_FINAL + "/" + new_subject + "/" + "stwits-" + new_subject + "-" + day + "-fix.csv"
        try:
            with open(input_file, "r") as stwi:
                reader = csv.reader(stwi, delimiter=',')
                for row in reader:
                    try:
                        # all lines
                        sent, conf = st.sent_stwits(row[2].strip())
                        self.counter.inc(sent, conf)

                        # explicit sentiment
                        if row[1] != "none":
                            self.bull_inc(row[1])

                        # non explicit sentiment
                        else:
                            self.part_counter.inc(sent, conf)

                    except Exception as e:
                        logger.error(e)
                        continue
        except Exception as e:
            logger.error(day + " : " + e)

        # without bull
        per_dict = self.counter.get_percentage()
        tot_dict = self.counter.tot_dict.copy()

        # include bull
        self.add_bull(self.part_counter)
        per_comb_dict = self.part_counter.get_percentage()
        tot_comb_dict = self.part_counter.tot_dict.copy()
        per_bull = self.get_percentage_bull()
        tot_bull = self.stwits_tot

        # prepare output
        writer_line = [day]
        comb_writer_line = [day]
        for key in self.counter.counter_list:
            writer_line.append(per_dict[key])
            writer_line.append(tot_dict[key])

            comb_writer_line.append(per_comb_dict[key])
            comb_writer_line.append(tot_comb_dict[key])

        comb_writer_line.append(per_bull)
        comb_writer_line.append(tot_bull)

        # write output
        logger.info(day)
        self.writer.writerow(writer_line)
        self.comb_writer.writerow(comb_writer_line)


class CounterTwitter():
    def __init__(self, subject):

        self.subject = subject
        # initialize output
        self.writer = get_writer("twitter", subject)
        self.writer.writerow(["Date", "Sent0.6", "Tot0.6", "Sent0.8", "Tot0.8", "Sent1.0", "Tot1.0"])

    def init_counter(self):
        self.counter = Counter()

    def count_day(self, day):
        self.init_counter()

        if subject == "coca-cola":
            new_subject = "cola"
        elif subject == "mcdonalds":
            new_subject = "mcdonald"
        else:
            new_subject = subject

        input_file = settings.DOWNLOADS_TWITTER_FINAL + "/" + new_subject + "/" + "twitter-" + new_subject + "-" + day + "-fix.csv"
        with open(input_file, "r") as twi:
            reader = csv.reader(twi, delimiter=',')
            head = [row for row in reader][:twi_max]
            for row in head:
                try:
                    # all lines
                    sent, conf = st.sent_twitter(row[0].strip())
                    # print(sent, conf, row[0].strip())
                    self.counter.inc(sent, conf)
                except Exception as e:
                    logger.error(e)
                    continue

        per_dict = self.counter.get_percentage()
        tot_dict = self.counter.tot_dict.copy()

        # prepare output
        writer_line = [day]
        for key in self.counter.counter_list:
            writer_line.append(per_dict[key])
            writer_line.append(tot_dict[key])

        # write output
        logger.info(day)
        self.writer.writerow(writer_line)


class CounterNews():
    def __init__(self, subject):

        self.subject = subject
        # initialize output
        self.writer = get_writer("news", subject)
        self.writer.writerow(["Date", "Sent0.6", "Tot0.6", "Sent0.8", "Tot0.8", "Sent1.0", "Tot1.0"])

    def init_counter(self):
        self.counter = Counter()

    def count_day(self, day):
        self.init_counter()

        new_subject = self.subject
        input_file = settings.DOWNLOADS_NEWS_FINAL + "/" + new_subject + "/" + "news-" + new_subject + "-" + day + "-final.csv"
        with open(input_file, "r") as input:
            for row in input:
                try:
                    sent, conf = st.sent_news(row.strip())
                    # print(sent, conf, row[1].strip())
                    self.counter.inc(sent, conf)
                except Exception as e:
                    logger.error(e)
                    continue

        per_dict = self.counter.get_percentage()
        tot_dict = self.counter.tot_dict.copy()

        # prepare output
        writer_line = [day]
        for key in self.counter.counter_list:
            writer_line.append(per_dict[key])
            writer_line.append(tot_dict[key])

        # write output
        logger.info(day)
        self.writer.writerow(writer_line)


###############
#### start ####
###############

# vars
source = "stwits"
start_date = date(2017, 5, 1)
end_date = date(2017, 8, 31)
twi_max = 20000


subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla"]
# subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the", "djia", "compq", "spx"]
# subjects = ["netflix", "nike", "samsung", "tesla", "the"] # twitter
# subjects = ["tesla"]

for subject in subjects:
    logger.info(subject)

    if source == "twitter":
        counter = CounterTwitter(subject)
    elif source == "stwits":
        counter = CounterStwits(subject)
    else:
        counter = CounterNews(subject)


    for single_date in daterange(start_date, end_date):
        day = single_date.strftime("%Y-%m-%d")
        try:
            counter.count_day(day)

        except Exception as e:
            logger.error(e)
            continue
