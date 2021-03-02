import json
import configparser
from os import listdir
from os.path import isfile, join

config = configparser.ConfigParser()
config.read("/Users/berna/PycharmProjects/udacity_capstone/config.ini")
data_path = "/data/"


def dump_data(tickers, now):
    try:
        for i in range(len(tickers)):
            with open(f"{data_path}{tickers[i]['exchange']}{now}.json", "w") as json_file:
                json.dump(tickers[i], json_file)
    except Exception as e:
        pass


def dump_data_to_s3(s3, tickers, now):
    try:
        now = now.strftime("%Y%m%d%H%M%S")
        for i in range(len(tickers)):
            data = tickers[i]
            obj = s3.Object('udacity-capstone-bucket-berna', f"{now}{data['exchange']}.json")
            obj.put(Body=json.dumps(data))

    except Exception as e:
        pass


def get_json_filenames(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) if "json" in f]

    return onlyfiles


def get_json_filenames_in_s3(s3):
    bucket = s3.Bucket("udacity-capstone-bucket-berna")
    files = [json_file.key for json_file in bucket.objects.all()]
    return files[:3501]
