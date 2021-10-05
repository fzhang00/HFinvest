use SEC

--DROP TABLE IF exists Stock_Industry_lookup;
--CREATE TABLE Stock_Industry_lookup(
--	NameCH		nvarchar(100),
--	Ticker		varchar(10), 
--	IndustryCH	nvarchar(80),
--	IndustryEng varchar(60)
--	);
--select * from Stock_Industry_lookup order by IndustryCH;

--DROP TABLE IF exists SEC_13F_sina_Stock;
--CREATE TABLE SEC_13F_sina_Stock(
--	Date						smalldatetime NOT NULL, 
--	RankMarketVauleOfHolding	smallint not null,
--	--Name	, 
--	Ticker			varchar(10), 
--	--Industry	,
--	NumOfHolder		smallint,
--	HoldingShareM	float,
--	HoldingShare_QoQPer float,
--	MarketValueOfHolding_100M	smallint,
--	Ratio_InstitutionHolding	float, 
--	Price_QoQPer					float 
--	);
--select * from SEC_13F_sina_Stock order by date;


