import settings


file_name = settings.DOWNLOADS_TWITTER + "/the/twitter-the-2016-11-15-fix.csv"


file = open(file_name, 'r')
file_list = file.readlines()
# file_list = list()
# for line in file:
#     file_list.append(line)

print(file_list)
print(len(file_list))

unique_list = list(set(file_list))

print(len(unique_list))



text = "\"hello how are you\"\n"

print(text[-2])

if(text.strip()[-1] == "\""):
    print(True)

print("xxx")