
--money	-922,337,203,685,477.5808 to 922,337,203,685,477.5807 8 bytes
--smallmoney	- 214,748.3648 to 214,748.3647

--bigint	-2^63 (-9,223,372,036,854,775,808) to 2^63-1 (9,223,372,036,854,775,807)	8 Bytes
--int	-2^31 (-2,147,483,648) to 2^31-1 (2,147,483,647)	4 Bytes
--smallint	-2^15 (-32,768) to 2^15-1 (32,767)	2 Bytes
--tinyint	0 to 255

use Commodity_A1

--DROP TABLE IF exists LME_Daily_OpenInterest_Option_E;
--CREATE TABLE LME_Daily_OpenInterest_Option_E(
--	"Date"			smalldatetime NOT NULL,
--	"UNDERLYING"	nchar(5) not null,
--	"ContractType"	nchar(18),
--	"SubType"		nchar(5),
--	"ForwadMonth"		smalldatetime, 
--	"Strike"		money,
--	"OpenInterest"	float,
--	"Turnover"		float
--);
--GO
--select * from LME_Daily_OpenInterest_Option_E order by date;

--DROP TABLE IF exists LME_Daily_OpenInterest_Future_E;
--CREATE TABLE LME_Daily_OpenInterest_Future_E(
--	"Date"			smalldatetime NOT NULL,
--	"Underlying"	nchar(5) not null,
--	"ContractType"	nchar(18) ,
--	"ForwardDate"			smalldatetime,
--	"OpenInterest"	float,
--	"Turnover"		float
--);   
--GO
--select * from LME_Daily_OpenInterest_Future_E 
----where not (Underlying = 'ag' or Underlying = 'au')
--order by date;

--insert into LME_Daily_OpenInterest_Future_E values ('2021-05-05','AG','LMEPreciousFuture','2021-06-30', 90.0, 0.0)
--delete from LME_Daily_OpenInterest_Future_E 
--where Date = '2021-05-05' and [Underlying] = 'AG' and [ContractType] = 'LMEPreciousFuture' and [ForwardDate] = '2021-06-30'
--DELETE FROM LME_Daily_OpenInterest_Future_E where Date = '2021-05-06 00:00:00';
--  DELETE FROM LME_Daily_OpenInterest_Future_E 
--  where not (Underlying = 'ag' or Underlying = 'au' or Underlying = 'AH' or Underlying = 'CA')






--DROP TABLE IF exists LME_Daily_Volume;
--CREATE TABLE LME_Daily_Volume(
--	"Date"		date NOT NULL,
--	"Product"		nchar(5) not null,	
--	"Description"	nchar(45),
--	"Volume" int
--);
--GO
--select * from LME_Daily_Volume order by date;


--DROP TABLE IF exists LME_weeklyTraderReport_Silver;
--CREATE TABLE LME_weeklyTraderReport_Silver(
--	"Date"		date NOT NULL,
--	"Agent"		nchar(40) not null,	
--	"Position"	nchar(10),
--	"RiskReducing" float,
--	"Other"  float,
--	"Total" float
--);
--GO
--select * from LME_weeklyTraderReport_Silver order by date;


--DROP TABLE IF exists LME_weeklyTraderReport_Gold;
--CREATE TABLE LME_weeklyTraderReport_Gold(
--	"Date"		date NOT NULL,
--	"Agent"		nchar(40) not null,	
--	"Position"	nchar(10),
--	"RiskReducing" float,
--	"Other"  float,
--	"Total" float
--);
--GO
--select * from LME_weeklyTraderReport_Gold order by date;


--DROP TABLE IF exists LME_weeklyTraderReport_AL;
--CREATE TABLE LME_weeklyTraderReport_AL(
--	"Date"		date NOT NULL,
--	"Agent"		nchar(40) not null,	
--	"Position"	nchar(10),
--	"RiskReducing" float,
--	"Other"  float,
--	"Total" float
--);
--GO
--select * from LME_weeklyTraderReport_AL order by date;


--DROP TABLE IF exists LME_weeklyTraderReport_CA;
--CREATE TABLE LME_weeklyTraderReport_CA(
--	"Date"		date NOT NULL,
--	"Agent"		nchar(40) not null,	
--	"Position"	nchar(10),
--	"RiskReducing" float,
--	"Other"  float,
--	"Total" float
--);
--GO
--select * from LME_weeklyTraderReport_CA;
--Risk Reducing directly related to commercial activities
--Operators with compliance obligations under Directive 2003/87/EC


--DROP TABLE IF exists LME_precious_VolOpenInterest;
--CREATE TABLE LME_precious_VolOpenInterest(
--	"Date"		date NOT NULL,
--	"Future"	nchar(20) not null,	
--	"Volume"	int,
--	"OpenInterest"  int
--);
--GO
--select * from LME_precious_VolOpenInterest

--DROP TABLE IF exists LME_precious_price;
--CREATE TABLE LME_precious_price(
--	"Date"		date NOT NULL,
--	"Future"	nchar(20) not null,
--	"Spot"  smallmoney,
--	"Month1" smallmoney,
--	"Month6" smallmoney,
--	"Month12" smallmoney,
--	"Month24" smallmoney
--);
--GO
--select * from LME_precious_price


--DROP TABLE IF exists LME_baseMetal_price;
--CREATE TABLE LME_baseMetal_price(
--	"Date"		date NOT NULL,
--	"Contract"	nchar(20) not null,
--	"CashBuyer" smallmoney,
--	"CashSellerSettlement" smallmoney,
--	"Month3_Buyer"  smallmoney,
--	"Month3_Seller" smallmoney,
--	"Month15_Buyer" smallmoney,
--	"Month15_Seller" smallmoney,
--	"Dec1_Buyer"	smallmoney,
--	"Dec1_Seller"	smallmoney,
--);
--GO
--select * from LME_baseMetal_price


--DROP TABLE IF exists LME_baseMetal_stock;
--CREATE TABLE LME_baseMetal_Stock(
--	"Date" date NOT NULL,
--	"Future" nchar(20) not null,
--	"OpeningStock" int ,
--	"LiveWarrants" int ,
--	"CancelledWarrants" int 
--);
--GO
--select * from LME_baseMetal_Stock







 



