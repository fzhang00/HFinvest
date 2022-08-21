use [SP500_Ratios]

--DROP TABLE IF exists SP500_ClosePrice_PerSales;
--CREATE TABLE SP500_ClosePrice_PerSales(
--	Date  date NOT NULL,	"PricePerSales" float, YOY float  );
select * from SP500_ClosePrice_PerSales order by [Date] desc;

--DROP TABLE IF exists SP500_SalesPerShare_Estimate;
--CREATE TABLE SP500_SalesPerShare_Estimate(
--	Date  date NOT NULL,	Sector varchar(35), "SalesPerShare_Estimate" float, YOY float  );
select * from SP500_SalesPerShare_Estimate --where Sector = 'Materials' 
order by [Date] desc, Sector;

--DROP TABLE IF exists SP500_OperatingMargin_Estimate;
--CREATE TABLE SP500_OperatingMargin_Estimate(
--	Date  date NOT NULL,	Sector varchar(35), "OperatingMargin_Estimate" float, YOY float  );
select * from SP500_OperatingMargin_Estimate --where Sector = 'Materials' 
order by [Date] desc, Sector;

--DROP TABLE IF exists SP500_EPS_Reported;
--CREATE TABLE SP500_EPS_Reported(
--	Date  date NOT NULL,	Sector varchar(35), "EPS_Reported" float, YOY float  );
select * from SP500_EPS_Reported --where Sector = 'Materials' 
order by [Date] desc, Sector;


--DROP TABLE IF exists SP500_OperatingEPS_EstimateTTM;
--CREATE TABLE SP500_OperatingEPS_EstimateTTM(
--	Date  date NOT NULL,	Sector varchar(35), "EPS_EstimateTTM" float, YOY float  );
select * from SP500_OperatingEPS_EstimateTTM --where Sector = 'Materials' 
order by [Date] desc, Sector;

--DROP TABLE IF exists SP500_Sector_Industry_MarketCap;
--CREATE TABLE SP500_Sector_Industry_MarketCap(
--	Date  date NOT NULL,
--	Sector varchar(35), Industry varchar(60), 
--	"MarketCap(B)" float  );
select * from SP500_Sector_Industry_MarketCap order by [Date] desc;

--DROP TABLE IF exists SP500_Sector_Weight;
--CREATE TABLE SP500_Sector_Weight(
--	Date  date NOT NULL,
--	Sector varchar(35),
--	WeightPercent float);
select * from [SP500_Ratios].[dbo].[SP500_Sector_Weight] order by [Date] desc;

	--CommunicationServices float, ConsumerDiscretionary float, 	ConsumerStaples float, 
	--Energy float,			Financials float,			HealthCare float,
	--Industrials float, InformationTechnology float,		Materials float,	 			
	--Utilities float,	RealEstate float

--DROP TABLE IF exists SP500_Sector_PriceVolume;
--CREATE TABLE SP500_Sector_PriceVolume(
--	Date  date NOT NULL,
--	Sector varchar(10),
--	ClosePrice float,
--	Volume float);
select * from SP500_Sector_PriceVolume order by date desc;


--DROP TABLE IF exists SP500_Ratios_PE_shiller;
--CREATE TABLE SP500_Ratios_PE_shiller(
--	Date	date NOT NULL, 
--	PEshiller	float not null	);
select * from SP500_Ratios_PE_shiller order by date desc;

--DROP TABLE IF exists SP500_Ratios_PE_TTM;
--CREATE TABLE SP500_Ratios_PE_TTM(
--	Date	date NOT NULL, 
--	PE	float not null	);
select * from SP500_Ratios_PE_TTM order by date desc;

--DROP TABLE IF exists SP500_ClosePrice;
--CREATE TABLE SP500_ClosePrice(
--	Date	date NOT NULL, 
--	ClosePrice	float not null	);
select * from SP500_ClosePrice order by date desc;

--CREATE TABLE SP500_Ratios_daily_PE_sector_shillerPE(
--	Date , smalldatetime,
--	Sector, char(22),
--	ShillerPE , float,
--	RegulaPE, float);
select * from SP500_Ratios_daily_PE_sector_shillerPE --where [Sector] like 'SP500%'
order by date desc;

go

-- not used  ----------------
--DROP TABLE IF exists SP500_Volume_Sector;
--CREATE TABLE SP500_Volume_Sector(
--	Date  date NOT NULL,
--	CommunicationServices float, ConsumerDiscretionary float, 	ConsumerStaples float, 
--	Energy float,			Financials float,			HealthCare float,
--	Industrials float, InformationTechnology float,		Materials float,	 			
--	Utilities float,	RealEstate float,);
--select * from SP500_Volume_Sector order by date desc;

--DROP TABLE IF exists SP500_ClosePrice_Sector;
--CREATE TABLE SP500_ClosePrice_Sector(
--	Date  date NOT NULL,
--	CommunicationServices float, ConsumerDiscretionary float, 	ConsumerStaples float, 
--	Energy float,			Financials float,			HealthCare float,
--	Industrials float, InformationTechnology float,		Materials float,	 			
--	Utilities float,	RealEstate float,);
--select * from SP500_ClosePrice_Sector order by date desc;