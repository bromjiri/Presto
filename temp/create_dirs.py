import os
import settings


for i in range(1,31):
    day = str(i).zfill(2)
    dir = settings.GOOGLE_HTML  + "/netflix/2016-11-" + day
    os.makedirs(dir, exist_ok=True)
    print(dir)