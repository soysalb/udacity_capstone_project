import pandas as pd
import json
from utilities import *
import boto3

path = "/data"

jsons = get_json_filenames(path)
"""s3 = boto3.resource("s3")
jsons = get_json_filenames_in_s3(s3)"""
data = list()
# for local usage
for file in jsons:
    with open(path + "/" + file) as f:
        r = json.load(f)
    data.append(r)
# s3_c = boto3.client("s3")

"""for file in jsons:
    s3_clientobj = s3_c.get_object(Bucket="udacity-capstone-bucket-berna", Key=file)
    s3_clientdata = s3_clientobj["Body"].read().decode("utf-8")
    s3clientlist = json.loads(s3_clientdata)
    data.append(s3clientlist)"""

staging_ticker_list = list()
for ticker in data:
    for value in ticker.values():
        ticker_dict = dict()
        print(value)
        try:
            ticker_dict["symbol"] = value["symbol"]
            ticker_dict["buy"] = value["bid"]
            ticker_dict["sell"] = value["ask"]
            ticker_dict["open"] = value["open"]
            ticker_dict["low"] = value["low"]
            ticker_dict["high"] = value["high"]
            ticker_dict["last"] = value["last"]
            ticker_dict["close"] = value["close"]
            ticker_dict["vol"] = value["vwap"]
            ticker_dict["call_ts"] = value["timestamp"]
            ticker_dict["call_dt"] = value["datetime"]
            ticker_dict["exchange_key"] = list(ticker.values())[-1]
        except Exception as e:
            pass

        staging_ticker_list.append(ticker_dict)

tickers = pd.DataFrame.from_dict(staging_ticker_list, orient="columns")
tickers.dropna(how="all", inplace=True)
tickers.reset_index(drop=True, inplace=True)
tickers.index = tickers.index + 1
tickers.reset_index(drop=False, inplace=True)
tickers.call_ts = tickers.call_ts.fillna("1614526547105.0")
tickers.call_ts = tickers.call_ts.astype(float)
tickers.call_ts = tickers.call_ts.astype(int)
tickers["call_ts"] = pd.to_datetime(tickers["call_ts"], unit='ms')
tickers["call_dt"] = tickers["call_ts"].apply(lambda x: x.date().strftime("%m/%d/%Y"))
tickers["call_ts"] = tickers.call_ts.astype(str)

tickers.to_csv("/Users/berna/PycharmProjects/udacity_capstone/data/staging_tickers.csv", index=False)
# s3.meta.client.upload_file(Filename="tickers.csv", Bucket="udacity-capstone-bucket-berna", Key="tickers.csv")
