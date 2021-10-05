/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [Date]      ,[Future]
      ,[OpeningStock]      ,[LiveWarrants]      ,[CancelledWarrants]
  FROM [Commodity_A1].[dbo].[LME_baseMetal_Stock] order by date desc


/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [Date]      ,[Contract]      
	,[3-Month]      ,[Month1]      ,[Month2]      ,[Month3]      ,[Month4]      ,[Month5]      ,[Month6]
  FROM [Commodity_A1].[dbo].[LME_baseMetal_ColsePrice2021] order by date desc

SELECT TOP (1000) [Date]
    ,[Contract]      ,[CashBid]      ,[CashOffer]
    ,[Month3_Bid]      ,[Month3_Offer]    ,[DecBid_1]      ,[DecOffer_1]      ,[DecBid_2]      ,[DecOffer_2]      ,[DecBid_3]      ,[DecOffer_3]
FROM [Commodity_A1].[dbo].[LME_baseMetal_OfficialPrice2021] order by date desc

  SELECT TOP (1000) [Date]      ,[Contract]      ,[Spot]
      ,[Month1]      ,[Month2]      ,[Month3]      ,[Month4]      ,[Month5]      ,[Month6]
      ,[Month7]      ,[Month8]      ,[Month9]      ,[Month10]      ,[Month11]     ,[Month12]
      ,[Month13]      ,[Month14]      ,[Month15]      ,[Month16]      ,[Month17]      ,[Month18]
      ,[Month19]      ,[Month20]      ,[Month21]      ,[Month22]      ,[Month23]      ,[Month24]
  FROM [Commodity_A1].[dbo].[LME_precious_steel_price2021] order by date desc

SELECT TOP (1000) [Name]      ,[Date]      ,[Price]
  FROM [Commodity_A1].[dbo].[LME_Lithium_ColsePrice2021]