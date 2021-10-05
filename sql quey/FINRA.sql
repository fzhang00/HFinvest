

-- 95 for energy
--81 equity  =MAX(LEN(A7:A1000))
-- 46 fx
-- 55 interest rate
--76 metal
use FINRA

--DROP TABLE IF exists FINRA_monthly_Margin_Stast;
--CREATE TABLE FINRA_monthly_Margin_Stast(
--	"Date"		smallDatetime NOT NULL,
--	"DebitBalances CustomerSecuritiesMarginAccount" int,
--	"FreeCreditBalances CustomerCashAccount" int,
--	"FreeCreditBalances CustomerSecuritiesMarginAccount" int		
--);
--GO
select * from FINRA_monthly_Margin_Stast order by Date desc


		


