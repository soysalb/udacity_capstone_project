import asyncio
import ccxt
import ccxt.async_support as ccxta  # noqa: E402
import logging


def sync_client(exchange):
    client = getattr(ccxt, exchange)({
        'enableRateLimit': True,  # this option enables the built-in rate limiter
    })
    tickers = client.fetch_tickers()
    return tickers


async def async_client(exchange):
    client = getattr(ccxta, exchange)({
        'enableRateLimit': True,  # this option enables the built-in rate limiter
    })
    tickers = await client.fetch_tickers()
    await client.close()
    tickers["exchange"] = exchange
    await asyncio.sleep(1)
    return tickers


async def multi_tickers(exchanges):
    try:
        input_coroutines = input_coroutines = [async_client(exchange) for exchange in exchanges]
        tickers = await asyncio.gather(*input_coroutines, return_exceptions=True)
        return tickers
    except Exception as e:
        pass
