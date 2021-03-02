import ccxt
import pandas as pd


def markets():
    markets_list = list()
    for i, exchange_id in enumerate(ccxt.exchanges):
        try:
            markets_dict = dict()
            exchange = getattr(ccxt, exchange_id)()
            markets = exchange.load_markets()
            for val in markets.values():
                markets_dict = dict()
                markets_dict["exchange"] = exchange_id
                markets_dict["symbol"] = val["symbol"]
                markets_dict["base"] = val["base"]
                markets_dict["quote"] = val["quote"]
                markets_list.append(markets_dict)

        except Exception as e:
            markets_list.append(markets_dict)

    markets = pd.DataFrame.from_dict(markets_list, orient="columns")
    markets = markets.drop_duplicates()
    markets.columns = ["exchange", "symbol", "base", "quote"]

    return markets
