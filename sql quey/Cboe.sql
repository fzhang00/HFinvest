use Cboe

--DROP TABLE IF exists EquiptyTradingValue_daily;
--CREATE TABLE EquiptyTradingValue_daily(
--	Date		smalldatetime NOT NULL,
--	TradingMarketCentre		varchar(30),

--	TapeA				money,
--	TapeB				money,
--	TapeC				money,
--	Market				money,
--	percentMkt			float,
--	avg5Days			float
--);
--select * from EquiptyTradingValue_daily order by date;


--DROP TABLE IF exists EquiptyVolume_daily;
--CREATE TABLE EquiptyVolume_daily(
--	Date		smalldatetime NOT NULL,
--	OrderBookType			varchar(20),
--	TradingMarketCentre		varchar(30),
--	TapeA				bigint,
--	TapeAMarketShare	float,
--	TapeB				bigint,
--	TapeBMarketShare	float,
--	TapeC				bigint,
--	TapeCMarketShare	float,
--	Market				bigint,
--	percentMkt			float
--);
--select * from EquiptyVolume_daily order by date;



--DROP TABLE IF exists PutCall_ratio_A;
--CREATE TABLE PutCall_ratio_A(
--	Date		smalldatetime NOT NULL,
--	Name		varchar(50),
--	Ratio		float
--	);
--select * from PutCall_ratio_A order by date;

--DROP TABLE IF exists PutCall_ratio_B_Vol_OI;
--CREATE TABLE PutCall_ratio_B_Vol_OI(
--	Date		smalldatetime NOT NULL,
--	Name		varchar(45) not null,
--	OptionType		varchar(8), -- call, put, total
--    Volume		integer,
--    OpenInterest integer
--	);
--select * from PutCall_ratio_B_Vol_OI order by date;





go

