import statistics


class Statistic:

    def __init__(self, source, subject, precision, method, binning):

        self.source = source
        self.subject = subject
        self.precision = precision
        self.method = method
        self.binning = binning

        self.skl_dict = dict()
        self.skl_dict['mnb'] = 0
        self.skl_dict['bnb'] = 0
        self.skl_dict['lr'] = 0
        self.skl_dict['lsvc'] = 0
        self.skl_dict['nsvc'] = 0
        self.skl_dict['voted'] = 0

        self.nltk_dict = dict()
        self.nltk_dict['accuracy'] = 0
        self.nltk_dict['pos_prec'] = 0
        self.nltk_dict['neg_prec'] = 0
        self.nltk_dict['pos_rec'] = 0
        self.nltk_dict['neg_rec'] = 0
        self.nltk_dict['d1'] = 0
        self.nltk_dict['d2'] = 0
        self.nltk_dict['d3'] = 0

        self.lr_dict = dict()
        self.lr_dict['accuracy'] = 0
        self.lr_dict['pos_prec'] = 0
        self.lr_dict['neg_prec'] = 0
        self.lr_dict['pos_rec'] = 0
        self.lr_dict['neg_rec'] = 0

        self.voted_list = list()

    def add_skl(self, new_dict):
        self.skl_dict['mnb'] += new_dict['mnb']
        self.skl_dict['bnb'] += new_dict['bnb']
        self.skl_dict['lr'] += new_dict['lr']
        self.skl_dict['lsvc'] += new_dict['lsvc']
        self.skl_dict['nsvc'] += new_dict['nsvc']
        self.skl_dict['voted'] += new_dict['voted']

        self.voted_list.append(new_dict['voted'])

    def add_nltk(self, new_dict):
        self.nltk_dict['accuracy'] += new_dict['accuracy']
        self.nltk_dict['pos_prec'] += new_dict['pos_prec']
        self.nltk_dict['neg_prec'] += new_dict['neg_prec']
        self.nltk_dict['pos_rec'] += new_dict['pos_rec']
        self.nltk_dict['neg_rec'] += new_dict['neg_rec']
        self.nltk_dict[new_dict['most1']] += 3
        self.nltk_dict[new_dict['most2']] += 2
        self.nltk_dict[new_dict['most3']] += 1

    def add_lr(self, new_dict):
        self.lr_dict['accuracy'] += new_dict['accuracy']
        self.lr_dict['pos_prec'] += new_dict['pos_prec']
        self.lr_dict['neg_prec'] += new_dict['neg_prec']
        self.lr_dict['pos_rec'] += new_dict['pos_rec']
        self.lr_dict['neg_rec'] += new_dict['neg_rec']

    def mean_skl(self, cycles):
        self.skl_mean = dict()
        self.skl_mean['mnb'] = self.skl_dict['mnb']/cycles
        self.skl_mean['bnb'] = self.skl_dict['bnb']/cycles
        self.skl_mean['lr'] = self.skl_dict['lr']/cycles
        self.skl_mean['lsvc'] = self.skl_dict['lsvc']/cycles
        self.skl_mean['nsvc'] = self.skl_dict['nsvc']/cycles
        self.skl_mean['voted'] = self.skl_dict['voted']/cycles

    def mean_nltk(self, cycles):
        self.nltk_mean = dict()
        self.nltk_mean['accuracy'] = self.nltk_dict['accuracy']/cycles
        self.nltk_mean['pos_prec'] = self.nltk_dict['pos_prec']/cycles
        self.nltk_mean['neg_prec'] = self.nltk_dict['neg_prec']/cycles
        self.nltk_mean['pos_rec'] = self.nltk_dict['pos_rec']/cycles
        self.nltk_mean['neg_rec'] = self.nltk_dict['neg_rec']/cycles
        self.nltk_mean['d1'] = self.nltk_dict['d1']
        self.nltk_mean['d2'] = self.nltk_dict['d2']
        self.nltk_mean['d3'] = self.nltk_dict['d3']

    def mean_lr(self, cycles):
        self.lr_mean = dict()
        self.lr_mean['accuracy'] = self.lr_dict['accuracy']/cycles
        self.lr_mean['pos_prec'] = self.lr_dict['pos_prec'] / cycles
        self.lr_mean['neg_prec'] = self.lr_dict['neg_prec'] / cycles
        self.lr_mean['pos_rec'] = self.lr_dict['pos_rec'] / cycles
        self.lr_mean['neg_rec'] = self.lr_dict['neg_rec'] / cycles

    def print_nltk(self):
        print("\n" + self.source + ", " + self.subject + ", " + self.precision + ", " + self.method + ":\n"
              + "accuracy: " + str(round(self.nltk_mean["accuracy"], 1))
              + ", pos_prec: " + str(round(self.nltk_mean["pos_prec"], 1))
              + ", neg_prec: " + str(round(self.nltk_mean["neg_prec"], 1))
              + ", pos_rec: " + str(round(self.nltk_mean["pos_rec"], 1))
              + ", neg_rec: " + str(round(self.nltk_mean["neg_rec"], 1))
              + ", d1: " + str(self.nltk_mean["d1"])
              + ", d2: " + str(self.nltk_mean["d2"])
              + ", d3: " + str(self.nltk_mean["d3"]))

    def write_nltk(self, filename):
        f = open(filename, 'a')
        f.write(self.precision + ", " + self.binning + ", "
              + str(round(self.nltk_mean["accuracy"], 1)) + ", "
              + str(round(self.nltk_mean["pos_prec"], 1)) + ", "
              + str(round(self.nltk_mean["neg_prec"], 1)) + ", "
              + str(round(self.nltk_mean["pos_rec"], 1)) + ", "
              + str(round(self.nltk_mean["neg_rec"], 1)) + ", "
              + str(self.nltk_mean["d1"]) + ", "
              + str(self.nltk_mean["d2"]) + ", "
              + str(self.nltk_mean["d3"]) + "\n")
        f.close()

    def print_skl(self):
        # print(self.source + ", " + self.subject + ", " + self.precision + ", " + self.method + ":\n")
        print("mnb: " + str(round(self.skl_mean["mnb"], 1))
              + ", bnb: " + str(round(self.skl_mean["bnb"], 1))
              + ", lr: " + str(round(self.skl_mean["lr"], 1))
              + ", lsvc: " + str(round(self.skl_mean["lsvc"], 1))
              + ", nsvc: " + str(round(self.skl_mean["nsvc"], 1))
              + ", voted: " + str(round(self.skl_mean["voted"], 1)))

    def write_skl(self, filename):
        f = open(filename, 'a')
        f.write(self.precision + ", " + self.binning + ", "
                + str(round(self.skl_mean["mnb"], 1)) + ", "
                + str(round(self.skl_mean["bnb"], 1)) + ", "
                + str(round(self.skl_mean["lr"], 1)) + ", "
                + str(round(self.skl_mean["lsvc"], 1)) + ", "
                + str(round(self.skl_mean["nsvc"], 1)) + ", "
                + str(round(self.skl_mean["voted"], 1)) + "\n")
        f.close()

    def print_lr(self):
        print("\n" + self.source + ", " + self.subject + ", " + self.precision + ", " + self.method + ":")
        print("accuracy: " + str(round(self.lr_mean["accuracy"], 1))
              + ", pos_prec: " + str(round(self.lr_mean["pos_prec"], 1))
              + ", neg_prec: " + str(round(self.lr_mean["neg_prec"], 1))
              + ", pos_rec: " + str(round(self.lr_mean["pos_rec"], 1))
              + ", neg_rec: " + str(round(self.lr_mean["neg_rec"], 1)))

    def write_lr(self, filename):
        f = open(filename, 'a')
        f.write(self.precision + ", " + self.binning + ", "
                + str(round(self.lr_mean["accuracy"], 1)) + ", "
                + str(round(self.lr_mean["pos_prec"], 1)) + ", "
                + str(round(self.lr_mean["neg_prec"], 1)) + ", "
                + str(round(self.lr_mean["pos_rec"], 1)) + ", "
                + str(round(self.lr_mean["neg_rec"], 1)) + "\n")
        f.close()

    def print_stddev(self):
        print("std dev: " + str(statistics.stdev(self.voted_list)))