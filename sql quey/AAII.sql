
use [Sentiment]


--DROP TABLE IF exists AAII_SentimentSurvey;
--CREATE TABLE AAII_SentimentSurvey(
--	Date  date NOT NULL,
--	Bullish	float , Neutral	float ,	Bearish  float  );
select * from AAII_SentimentSurvey order by [Date] desc;



go

