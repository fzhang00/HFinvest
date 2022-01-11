use Cboe
--SELECT *  FROM [Cboe].[dbo].Option_CboeSum_daily order by date
--SELECT *  FROM [Cboe].[dbo].Option_CboeIndex_daily order by date
--SELECT *  FROM [Cboe].[dbo].Option_CboeExchangeTradeProduct_daily order by date
--SELECT *  FROM [Cboe].[dbo].Option_CboeEquity_daily order by date
--SELECT *  FROM [Cboe].[dbo].Option_CboeVOLATILITYINDEX_daily order by date
--SELECT *  FROM [Cboe].[dbo].Option_CboeSPX_daily order by date
--SELECT *  FROM [Cboe].[dbo].Option_CboeOEX_daily order by date
--SELECT *  FROM [Cboe].[dbo].Option_CboeMRUT_daily order by date
--SELECT *  FROM [Cboe].[dbo].Option_USmarket_TradingSummary_ValueVolume_daily order by date, [Market Participant]
select * from Option_Cboe_MostActiveVolume_daily order by dateTime desc, volume


--DROP TABLE IF exists Option_Cboe_MostActiveVolume_daily;
--CREATE TABLE Option_Cboe_MostActiveVolume_daily(
--	DateTime		smalldatetime NOT NULL,
--	Type		varchar(30),
--	CallPut		varchar(6),
--	Symbol		varchar(15),
--	Expires		date,
--	StrikePrice float, 	
--	Volume	 float );
--select * from Option_Cboe_MostActiveVolume_daily;

--DROP TABLE IF exists Option_USmarket_TradingSummary_ValueVolume_daily;
--CREATE TABLE Option_USmarket_TradingSummary_ValueVolume_daily(
--	Date		date NOT NULL,
--	"Market Participant"		varchar(50),

--	"Equity Option Contracts"	 float,	"Equity Option Trade Count"	 float,	"Equity Option Notional"	 float,

--	"Index/Other Option Contracts"	 float,	"Index/Other Option Trade Count"  float,	"Index/Other Option Notional"	 float,

--	"Total Option Contracts"	 float,	"Total Trade Count"	 float,	"Total Option Notional"  float );  
--select * from Option_USmarket_TradingSummary_ValueVolume_daily;


--DROP TABLE IF exists Option_CboeMRUT_daily;
--CREATE TABLE Option_CboeMRUT_daily(
--	Date		date NOT NULL,
--	MRUT		varchar(20),
--	Call float,
--	Put float,
--	Total float );
--select * from Option_CboeMRUT_daily;

--DROP TABLE IF exists Option_CboeOEX_daily;
--CREATE TABLE Option_CboeOEX_daily(
--	Date		date NOT NULL,
--	OEX		varchar(20),
--	Call float,
--	Put float,
--	Total float );
--select * from Option_CboeOEX_daily;

--DROP TABLE IF exists Option_CboeSPX_daily;
--CREATE TABLE Option_CboeSPX_daily(
--	Date		date NOT NULL,
--	SPX		varchar(20),
--	Call float,
--	Put float,
--	Total float );
--select * from Option_CboeSPX_daily;

--DROP TABLE IF exists Option_CboeVOLATILITYINDEX_daily;
--CREATE TABLE Option_CboeVOLATILITYINDEX_daily(
--	Date		date NOT NULL,
--	VIX		varchar(20),
--	Call float,
--	Put float,
--	Total float );
--select * from Option_CboeVOLATILITYINDEX_daily;

--DROP TABLE IF exists Option_CboeEquity_daily;
--CREATE TABLE Option_CboeEquity_daily(
--	Date		date NOT NULL,
--	Equity		varchar(20),
--	Call float,
--	Put float,
--	Total float );
--select * from Option_CboeEquity_daily;

--DROP TABLE IF exists Option_CboeExchangeTradeProduct_daily;
--CREATE TABLE Option_CboeExchangeTradeProduct_daily(
--	Date		date NOT NULL,
--	ETP		varchar(20),
--	Call float,
--	Put float,
--	Total float );
--select * from Option_CboeExchangeTradeProduct_daily;

--DROP TABLE IF exists Option_CboeIndex_daily;
--CREATE TABLE Option_CboeIndex_daily(
--	Date		date NOT NULL,
--	IndexOptions		varchar(20),
--	Call float,
--	Put float,
--	Total float );
--select * from Option_CboeIndex_daily;

--DROP TABLE IF exists Option_CboeSum_daily;
--CREATE TABLE Option_CboeSum_daily(
--	Date		date NOT NULL,
--	SumOfAllProduct		varchar(20),
--	Call float,
--	Put float,
--	Total float
--);
--select * from Option_CboeSum_daily;


--DROP TABLE IF exists EquiptyTrading_ValueVolume_daily;
--CREATE TABLE EquiptyTrading_ValueVolume_daily(
--	"Date"		date NOT NULL,
--	"Market Participant"		varchar(50),

--	"Tape A Shares"		float,
--	"Tape B Shares"		float,
--	"Tape C Shares"		float,
--	"Total Shares"		float,

--	"Tape A Notional"	money,
--	"Tape B Notional"	money,
--	"Tape C Notional"	money,
--	"Total Notional"	money,

--	"Tape A Trade Count"	float,
--	"Tape B Trade Count"	float,
--	"Tape C Trade Count"	float,
--	"Total Trade Count"		float,
	
--	"Total sharePerCount"	float,
--	"Total notionalPerCount" float);
--select * from EquiptyTrading_ValueVolume_daily order by date;

---------------------------------------------------------------------


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

