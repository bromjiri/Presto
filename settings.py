import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DOWNLOADS = os.path.join(PROJECT_ROOT, "crawler/downloads")
DOWNLOADS_NEWS = os.path.join(PROJECT_ROOT, "crawler/downloads/news")
DOWNLOADS_STWITS = os.path.join(PROJECT_ROOT, "crawler/downloads/stwits")
DOWNLOADS_TWITTER = os.path.join(PROJECT_ROOT, "crawler/downloads/twitter")

PROCESS_SENTIMENT = os.path.join(PROJECT_ROOT, "predictor/data/sentiment")