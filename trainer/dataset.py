import settings

kaggle_path = settings.TRAINER_DATA + "/kaggle_full.txt"
marino_path = settings.TRAINER_DATA + "/marino_full.arff"
sanders_path = settings.TRAINER_DATA + "/sanders_full.csv"
stanford_neg = settings.TRAINER_DATA + "/stanford_neg_2000.csv"
stanford_neg = settings.TRAINER_DATA + "/stanford_neg_2000.csv"



class Dataset:

    content = list()


    def __init__(self, source = None):
        source = str(source)

        if(source == None):
            pass

        if(source == "kaggle"):
            self.content = self.read_kaggle()

    def do_pos(self, allowed_types):
        for line in self.content:
            line[0] = "test"

    def get_grams(self):
        pass

    def print_content(self):
        for line in self.content:
            print(line)

    def read_kaggle(self):
        kaggle = open(kaggle_path)
        content = list()
        for line in kaggle:
            parts = line.split('\t')
            if(parts[0] == "1"):
                category = "4"
            else:
                category = "0"
            content.append([parts[1].strip(), category])
        return content



if __name__ == '__main__':
    kaggle_set = Dataset("kaggle")
    kaggle_set.print_content()

    kaggle_set.do_pos(["J", "V"])
    kaggle_set.print_content()
