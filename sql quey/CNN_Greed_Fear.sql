use Fear_Greed
select * from Fear_Greed_CNN order by date desc;

select * from NYSE_52weekHighsLows order by date desc;
select * from McClellanVolSummationIndex order by date desc;
select * from PutCallRatio5MA order by date desc;
select * from Difference20DayStockBondReturns order by date desc;
select * from YieldSpreadJunkInvestment order by date desc;
-- no data
--SP500and125dayMA
--VIXand50dayMA
select * from SP500and125dayMA order by date desc;
select * from VIXand50dayMA order by date desc;

--DROP TABLE IF exists SP500and125dayMA;
--CREATE TABLE SP500and125dayMA(
--	Date					    smalldatetime NOT NULL, 
--	SP500and125dayMA	float not null	);
--select * from SP500and125dayMA order by date desc;

--DROP TABLE IF exists VIXand50dayMA;
--CREATE TABLE VIXand50dayMA(
--	Date					    smalldatetime NOT NULL, 
--	VIXand50dayMA	float not null	);
--select * from VIXand50dayMA order by date desc;


--DROP TABLE IF exists NYSE_52weekHighsLows;
--CREATE TABLE NYSE_52weekHighsLows(
--	Date					    smalldatetime NOT NULL, 
--	NYSE_52weekHighsLows	float not null	);
--select * from NYSE_52weekHighsLows order by date desc;

--DROP TABLE IF exists McClellanVolSummationIndex;
--CREATE TABLE McClellanVolSummationIndex(
--	Date					    smalldatetime NOT NULL, 
--	McClellanVolSummationIndex	float not null	);
--select * from McClellanVolSummationIndex order by date desc;

--DROP TABLE IF exists PutCallRatio5MA;
--CREATE TABLE PutCallRatio5MA(
--	Date					    smalldatetime NOT NULL, 
--	PutCallRatio5MA	float not null	);
--select * from PutCallRatio5MA order by date desc;

--DROP TABLE IF exists Difference20DayStockBondReturns;
--CREATE TABLE Difference20DayStockBondReturns(
--	Date					    smalldatetime NOT NULL, 
--	Difference20DayStockBondReturns	float not null	);
--select * from Difference20DayStockBondReturns order by date desc;

--DROP TABLE IF exists YieldSpreadJunkInvestment;
--CREATE TABLE YieldSpreadJunkInvestment(
--	Date					    smalldatetime NOT NULL, 
--	YieldSpreadJunkInvestment	float not null	);
--select * from YieldSpreadJunkInvestment order by date desc;

--DROP TABLE IF exists Fear_Greed_CNN;
--CREATE TABLE Fear_Greed_CNN(
--	Date						smalldatetime NOT NULL, 
--	Fear_Greed_CNN	float not null
--	--Name	, 
--	--Ticker			varchar(10), 
--	----Industry	,
--	--NumOfHolder		smallint,
--	--HoldingShareM	float,
--	--HoldingShare_QoQPer float,
--	--MarketValueOfHolding_100M	smallint,
--	--Ratio_InstitutionHolding	float, 
--	--Price_QoQPer					float 
--	);
--select * from Fear_Greed_CNN order by date desc;
--go
