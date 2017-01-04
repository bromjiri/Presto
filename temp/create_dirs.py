import os
import settings


for i in range(2,32):
    day = str(i).zfill(2)
    dir = settings.GOOGLE_HTML  + "/microsoft/2016-12-" + day
    os.makedirs(dir, exist_ok=True)
    print(dir)