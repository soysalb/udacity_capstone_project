import pandas as pd
from get_markets import *
from get_exchanges import *

markets = markets()
exchanges = exchanges()

exchanges["lowered"] = exchanges.exchange_key.str.lower()
staging_exchange = pd.merge(markets, exchanges, left_on="exchange", right_on="lowered", how="inner")
staging_exchange = staging_exchange.iloc[:, 1:-1]
staging_exc.version = staging_exc.version.fillna("v1")
staging_exchange.to_csv("/Users/berna/PycharmProjects/udacity_capstone/data/staging_exchanges.csv", index=False)
