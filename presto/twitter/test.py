import logging
import os

logging.basicConfig(level=logging.INFO)
logging.info("start " + os.path.basename(__file__))
logging.warning('And this, too')