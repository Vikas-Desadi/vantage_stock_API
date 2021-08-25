import time
import requests
from constants import SLEEP_FOR

count = 0
def hit_daily_url(url, data):
    global count
    count += 1
    if count%5 == 0:
        time.sleep(SLEEP_FOR)
    resp = requests.get(url, data)
    return resp

