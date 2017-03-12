import logging
import os


logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s", datefmt='%Y%m%d-%H:%M')
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

logPath = os.path.dirname(os.path.realpath(__file__))
fileName = "log/twitter-test.log"

fileHandler = logging.FileHandler("{0}/{1}".format(logPath, fileName))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

rootLogger.info("here is debug")
rootLogger.info("this is info!")


#log_file = os.path.dirname(os.path.realpath(__file__)) + "/log/twitter-all.log"
#print(log_file)