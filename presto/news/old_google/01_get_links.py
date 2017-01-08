import settings
import re


# for line in input:
#     matches = re.findall(r"http[:A-Za-z0-9\-\/\._]+microsoft[:A-Za-z0-9\-\/\._]+", line)
#     if matches:
#         unique = set(matches)
#         for u in unique:
#             print(u)


def get_links(date, subject):

    input_file = settings.GOOGLE_HTML + "/" + subject + "/" + date + "/" + subject + " location_USA - Google Search.html"
    output_file = settings.GOOGLE_HTML + "/" + subject + "/" + date + "/" + subject + "_old_links_" + date + ".txt"
    html_page = open(input_file, 'r')
    output = open(output_file, 'w')

    a_set = set()
    for line in html_page:
        match = re.findall(r"<a.*?<\/a>", line)
        if match:
            unique = set(match)
            for u in unique:
                a_set.add(u)

    all_link_set = set()
    for line in a_set:
        match = re.findall(r"http[:A-Za-z0-9\-\/\._]+", line)
        if match:
            unique = set(match)
            for u in unique:
                all_link_set.add(u)

    link_count = 0
    link_set = set()
    for link in all_link_set:
        if not ("google" in link or "youtube" in link or "blogger" in link):
            link_set.add(link)
            link_count+=1
            output.write(link + "\n")

    return link_count


year = "2016"
month = "12"
first_day = 1
last_day = 31
#subjects = ["coca-cola", "mcdonalds", "microsoft", "netflix", "nike", "samsung", "tesla", "the"]
subjects = ["coca-cola"]

for subject in subjects:
    for i in range(first_day, last_day+1):
        day = str(i).zfill(2)
        date = year + "-" + month + "-" + day
        link_count = get_links(date, subject)
        print(date + ": " + str(link_count) + " links")

