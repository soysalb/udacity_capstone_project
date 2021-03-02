class SqlQueries:
    tickers_table_insert = ("""
        SELECT  TickerId,
                Symbol,
                ExchangeKey,
                Buy,
                Sell,
                Open,
                Low,
                High,
                Last,
                Close,
                Vol,
                CallTs timestamptz,
        FROM    staging_tickers
        WHERE   TickerId is not null
    """)

    markets_table_insert = ("""
        SELECT  distinct Symbol,
                Base,
                Quote
        FROM    staging_tickers tickers,
                staging_exchanges exchanges
        WHERE   tickers.Symbol = exchanges.Symbol
                Symbol is not null
    """)

    exchanges_table_insert = ("""
        SELECT 	distinct ExchangeKey,
                WebUrl,
                DocUrl,
                Version
        FROM    staging_tickers tickers, 
                staging_exchanges exchanges
        WHERE   tickers.ExchangeKey = exchanges.ExchangeKey and
                ExchangeKey is not null
    """)

    time_table_insert = ("""
        SELECT distinct CallTs,
               CallDt,
               extract(second from CallTs), 
               extract(minute from CallTs), 
               extract(hour from CallTs), 
               extract(day from CallTs), 
               extract(month from CallTs), 
               extract(year from CallTs) 
        FROM   tickers
        WHERE  CallTs is not null
    """)
