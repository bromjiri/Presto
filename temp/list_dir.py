import settings
from os import listdir
from os.path import isfile, join
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

mypath = settings.TRAINER + "/tests/output/stanford"
print(listdir(mypath))

for f in listdir(settings.TRAINER + "/tests/output/stanford"):
    file_path = join(mypath, f)
    if isfile(file_path):
        print(file_path)