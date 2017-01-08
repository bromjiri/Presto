from textblob import TextBlob

test = TextBlob("after identifying the covered locations, microsoft merely encouraged buyers to get help if they encounter problems or just contribute to the ongoing hololens conversation")

print(test.sentiment)