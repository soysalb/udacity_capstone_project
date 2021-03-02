import ccxt
import pandas as pd


def exchanges():
    exchs_list = list()
    for i, exchange_id in enumerate(ccxt.exchanges):
        try:
            exchs_dict = dict()
            exchange = getattr(ccxt, exchange_id)()
            exchs_dict["exchange_key"] = exchange.name
            exchs_dict["web_url"] = exchange.urls["www"]
            exchs_dict["doc_url"] = exchange.urls["doc"]
            exchs_dict["version"] = exchange.version
            if type(exchs_dict["doc_url"]) is list:
                exchs_dict["doc_url"] = exchs_dict["doc_url"][0]
            exchs_list.append(exchs_dict)
        except Exception as e:
            print(e)
    exchanges = pd.DataFrame.from_dict(exchs_list, orient="columns")
    return exchanges
