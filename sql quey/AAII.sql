
use [Sentiment]

--DROP TABLE IF exists Michigan_ConsumerSurvey;
--CREATE TABLE Michigan_ConsumerSurvey(
--	Date  date NOT NULL,
--	Survey	varchar(35) , Result  float  );
select * from Michigan_ConsumerSurvey order by [Date] desc;

--DROP TABLE IF exists AAII_SentimentSurvey;
--CREATE TABLE AAII_SentimentSurvey(
--	Date  date NOT NULL, Bullish float , Neutral float ,Bearish float, Total float,
--	Bull8weekavg float,	Bull_BearSpread float, 
--	Bullavg float, Bullavg_DevP float, Bullavg_DevN float,
--	sp500High float, sp500Low float, sp500Close float	
--	);
select * from AAII_SentimentSurvey order by [Date] desc;



go

