from get_tickers_from_exchanges import *
import datetime
import time
import asyncio
from utilities import *
import boto3

exchanges = ["binance", "bittrex", "kucoin", "aax", "acx", "aofex", "bequant", "bibox", "bigone", "binanceus"]


def run_local():
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    tickers = asyncio.get_event_loop().run_until_complete(multi_tickers(exchanges))
    dump_data(tickers, now)
    # time.sleep(2)
    print("Check data directory")


"""
s3 = boto3.resource("s3")
for i in range(2):
    now = datetime.datetime.now()
    tickers = asyncio.get_event_loop().run_until_complete(multi_tickers(exchanges))
    dump_data_to_s3(s3, tickers, now)"""
i = 0
while (True):
    i = i + 1
    run_local()
    print(i)
    if i % 30 == 0:
        time.sleep(2)
