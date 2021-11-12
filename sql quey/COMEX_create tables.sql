

-- 95 for energy
--81 equity  =MAX(LEN(A7:A1000))
-- 46 fx
-- 55 interest rate
--76 metal
use Commodity_A1

select * from COMEX_Daily_Volume_OpenInterest_Agriculture order by date desc;
select * from COMEX_Daily_Volume_OpenInterest_Energy order by date desc
select * from COMEX_Daily_Volume_OpenInterest_Equity order by date desc
select * from COMEX_Daily_Volume_OpenInterest_FX order by date desc
select * from COMEX_Daily_Volume_OpenInterest_InterestRate order by date desc
select * from COMEX_Daily_Volume_OpenInterest_Metal order by date desc

--DROP TABLE IF exists COMEX_Daily_Volume_OpenInterest_Metal;
--CREATE TABLE COMEX_Daily_Volume_OpenInterest_Metal(
--	Date	smallDatetime NOT NULL,
--	Name	varchar(100) not null,
--	Type	char(10), 
--	Globex			int,
--	OpenOutCry		int,
--	ClearPort		int,
--	Volume			int,
--	OpenInterest	int,
--	Change			int
--);
--GO
--select * from COMEX_Daily_Volume_OpenInterest_Metal order by date desc

--DROP TABLE IF exists COMEX_Daily_Volume_OpenInterest_InterestRate;
--CREATE TABLE COMEX_Daily_Volume_OpenInterest_InterestRate(
--	Date	smallDatetime NOT NULL,
--	Name	varchar(100) not null,
--	Type	char(10), 
--	Globex			int,
--	OpenOutCry		int,
--	ClearPort		int,
--	Volume			int,
--	OpenInterest	int,
--	Change			int
--);
--GO
--select * from COMEX_Daily_Volume_OpenInterest_InterestRate order by date desc

--DROP TABLE IF exists COMEX_Daily_Volume_OpenInterest_FX;
--CREATE TABLE COMEX_Daily_Volume_OpenInterest_FX(
--	Date	smallDatetime NOT NULL,
--	Name	varchar(100) not null,
--	Type	char(10), 
--	Globex			int,
--	OpenOutCry		int,
--	ClearPort		int,
--	Volume			int,
--	OpenInterest	int,
--	Change			int
--);
--GO
--select * from COMEX_Daily_Volume_OpenInterest_FX order by date desc

--DROP TABLE IF exists COMEX_Daily_Volume_OpenInterest_Equity;
--CREATE TABLE COMEX_Daily_Volume_OpenInterest_Equity(
--	Date	smallDatetime NOT NULL,
--	Name	varchar(100) not null,
--	Type	char(10), 
--	Globex			int,
--	OpenOutCry		int,
--	ClearPort		int,
--	Volume			int,
--	OpenInterest	int,
--	Change			int
--);
--GO
--select * from COMEX_Daily_Volume_OpenInterest_Equity order by date desc

--DROP TABLE IF exists COMEX_Daily_Volume_OpenInterest_Energy;
--CREATE TABLE COMEX_Daily_Volume_OpenInterest_Energy(
--	Date	smallDatetime NOT NULL,
--	Name	varchar(100) not null,
--	Type	char(10), 
--	Globex			int,
--	OpenOutCry		int,
--	ClearPort		int,
--	Volume			int,
--	OpenInterest	int,
--	Change			int
--);
--GO
--select * from COMEX_Daily_Volume_OpenInterest_Energy order by date desc;

--DROP TABLE IF exists COMEX_Daily_Volume_OpenInterest_Agriculture;
--CREATE TABLE COMEX_Daily_Volume_OpenInterest_Agriculture(
--	Date	smallDatetime NOT NULL,
--	Name	varchar(100) not null,
--	Type	char(10), 
--	Globex			int,
--	OpenOutCry		int,
--	ClearPort		int,
--	Volume			int,
--	OpenInterest	int,
--	Change			int
--);
--GO
--select * from COMEX_Daily_Volume_OpenInterest_Agriculture order by date desc;

--DROP TABLE IF exists COMEX_Daily_Report_OpenInterest_LongShortPositon;
--CREATE TABLE COMEX_Daily_Report_OpenInterest_LongShortPositon(
--	"Date" smallDatetime NOT NULL,
--	"Future" char(35) not null,
--	"ForwardMonth" smallDatetime,
--	"Long Qty" int,
--	"Short Qty" int
--);
--GO
--select * from COMEX_Daily_Report_OpenInterest_LongShortPositon order by date desc;



--DROP TABLE IF exists COMEX_Stock;
--CREATE TABLE COMEX_Stock(
--	"Date" date NOT NULL,
--	"Future" char(20) not null,
--	"Registered" float ,
--	"Pledged" float ,
--	"Eligible" float,
--	"Total" float
--);
--GO
--select * from COMEX_Stock order by date desc;


--select * from SHFE_weeklyPriceVolOI
--DROP TABLE IF exists SHFE_weeklyPriceVolOI;
--CREATE TABLE SHFE_weeklyPriceVolOI(
--	"Date"		date NOT NULL,
--	"Species"	char(20) not null,
--	"Open" smallmoney,
--	"High" smallmoney,
--	"Low"  smallmoney,
--	"Close" smallmoney,
--	"PriceDif" smallmoney,
--	"OpenInterest"  int,
--	"OIDif"			int,
--	"PostPrice"	money,
--	"Volume" int,
--	"TurnOver" money
--);


GO
