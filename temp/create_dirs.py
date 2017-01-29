import os
import settings


for i in range(1,32):
    day = str(i).zfill(2)
    dir = settings.DOWNLOADS_NEWS  + "/google/tesla/2016-12-" + day
    os.makedirs(dir, exist_ok=True)
    print(dir)