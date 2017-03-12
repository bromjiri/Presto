import re

# input
date = "2016-11-11"


output_file = date + "/links.txt"
write_output = open(output_file, "a")

# bbc
journal = "bbc"
for i in range(1, 4):
    file = date + "/" + journal + "/" + journal + str(i) + ".html"
    print(file)
    with open(file, "r") as f:
        for line in f:
            # print(line)
            matches = re.findall(r"http://www.bbc.co.uk/news/[A-Za-z0-9\-]*", line)
            if matches:
                unique = set(matches)
                for u in unique:
                    write_output.write(u + "\n")

# theguardian
journal = "theguardian"
for i in range(1, 4):
    file = date + "/" + journal + "/" + journal + str(i) + ".html"
    print(file)
    with open(file, "r") as f:
        for line in f:
            # print(line)
            matches = re.findall(r"https://www.theguardian.com[A-Za-z0-9\-/]*", line)
            if matches:
                unique = set(matches)
                for u in unique:
                    write_output.write(u + "\n")

# cnbc
journal = "cnbc"
for i in range(1, 4):
    file = date + "/" + journal + "/" + journal + str(i) + ".html"
    print(file)
    try:
        with open(file, "r") as f:
            for line in f:
                # print(line)
                matches = re.findall(r"http://www.cnbc.com.*?html", line)
                if matches:
                    unique = set(matches)
                    for u in unique:
                        write_output.write(u + "\n")
    except Exception as e:
        continue



# latimes
journal = "latimes"
for i in range(1, 4):
    file = date + "/" + journal + "/" + journal + str(i) + ".html"
    print(file)
    with open(file, "r") as f:
        for line in f:
            # print(line)
            matches = re.findall(r"http://www.latimes.com.*?html", line)
            if matches:
                unique = set(matches)
                for u in unique:
                    write_output.write(u + "\n")



# nytimes
journal = "nytimes"
for i in range(1, 4):
    file = date + "/" + journal + "/" + journal + str(i) + ".html"
    print(file)
    with open(file, "r") as f:
        for line in f:
            # print(line)
            matches = re.findall(r"http://www.nytimes.com.*?html", line)
            if matches:
                unique = set(matches)
                for u in unique:
                    write_output.write(u + "\n")




