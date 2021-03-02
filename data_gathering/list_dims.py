import ccxt


def get_markets(id):
    exchange = getattr(ccxt, id)({
        'enableRateLimit': True,  # required according to the Manual
    })
    return exchange.load_markets()


def exchange_market_matcher(cur_to_check, exchanges):
    exchange_currency_dict = dict()
    currency_exchange_dict = dict()
    for exchange_id in exchanges:
        currencies = [curr for curr in get_markets(exchange_id).keys()]
        exchange_currency_dict[exchange_id] = list(set(cur_to_check).intersection(currencies))
    exchange_list = list()
    for cur in cur_to_check:
        for exc in exchange_currency_dict.keys():
            if cur in exchange_currency_dict[exc]:
                exchange_list.append(exc)
        currency_exchange_dict[cur] = list(set(exchange_list))

    return currency_exchange_dict


def create_currency_list(*args):
    new_currency_list = [j for i in args for j in list(set(i))]
    return list(set(new_currency_list))
