CREATE TABLE IF NOT EXISTS staging_exchanges (
    Symbol varchar(256),
    Base varchar(256),
	Quote varchar(256),
	ExchangeKey varchar(256),
	WebUrl varchar(65535),
	DocUrl varchar(65535),
	Version varchar(256)
);

CREATE TABLE IF NOT EXISTS staging_tickers (
	TickerId int,
	Symbol varchar(256),
	Buy decimal,
	Sell decimal,
	Opening decimal,
	Low decimal,
	High decimal,
	Last decimal,
	Closing decimal,
	Vol decimal,
	CallTs timestamptz,
	CallDt date,
	ExchangeKey varchar(256)
);

CREATE TABLE IF NOT EXISTS markets (
	Symbol varchar(256),
	Base varchar(256),
	Quote varchar(256),
	CONSTRAINT markets_pkey PRIMARY KEY (Symbol)
);

CREATE TABLE IF NOT EXISTS tickers (
	TickerId int,
	Symbol varchar(256),
	ExchangeKey varchar(256),
	Buy decimal,
	Sell decimal,
	Opening decimal,
	Low decimal,
	High decimal,
	Last decimal,
	Closing decimal,
	Vol decimal,
	CallTs timestamptz,
    CONSTRAINT ticker_pkey PRIMARY KEY (TickerId)
);

CREATE TABLE IF NOT EXISTS exchanges (
	ExchangeKey varchar(256),
	WebUrl varchar(65535),
	DocUrl varchar(65535),
	Version varchar(256)
	CONSTRAINT exchange_pkey PRIMARY KEY (ExchangeKey)
);

CREATE TABLE IF NOT EXISTS time (
    CallTs timestamptz,
    CallDt date,
	second int,
	minute int,
	hour int,
	day int,
	month int,
	year int,
	CONSTRAINT time_pkey PRIMARY KEY (CallTs)
) ;
