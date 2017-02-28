import os
import logging
from logging.handlers import RotatingFileHandler

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DOWNLOADS = os.path.join(PROJECT_ROOT, "crawler/downloads")

DOWNLOADS_STWITS = os.path.join(PROJECT_ROOT, "crawler/downloads/stwits")
DOWNLOADS_TWITTER = os.path.join(PROJECT_ROOT, "crawler/downloads/twitter")
DOWNLOADS_NEWS = os.path.join(PROJECT_ROOT, "crawler/downloads/news")

DOWNLOADS_GOOGLE = os.path.join(PROJECT_ROOT, "crawler/downloads/news/google")

TRAINER = os.path.join(PROJECT_ROOT, "trainer")
TRAINER_DATA = os.path.join(PROJECT_ROOT, "trainer/data")
TRAINER_TWITTER = os.path.join(PROJECT_ROOT, "trainer/twitter")

PROCESS_SENTIMENT = os.path.join(PROJECT_ROOT, "predictor/data/sentiment")

def get_logger(file_path):
    # Logging settings
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt='%Y%m%d-%H:%M')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # file
    log_file = os.path.dirname(file_path) + "/log/" + os.path.splitext(os.path.basename(file_path))[0] + ".log"
    dir = os.path.dirname(os.path.realpath(log_file))
    os.makedirs(dir, exist_ok=True)
    fileHandler = RotatingFileHandler(log_file, mode='a', maxBytes=5000000)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    # console
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    return logger