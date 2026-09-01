
USE GOLDTrackerDB;
GO
SELECT date, COUNT(*) AS cnt
FROM gold_prices
GROUP BY DATE 
HAVING COUNT(*)>1
go

SELECT TOP 50 * FROM gold_prices
go
select date from gold_prices
go
SELECT 
	SUM(CASE WHEN open_price is NULL THEN 1 else 0 end) as  null_open,
	SUM(CASE WHEN high_price is NULL then 1 else 0 end) as  null_high,
	SUM(CASE WHEN low_price is NULL then 1 else 0 end) as  null_low,
	SUM(CASE WHEN close_price is NULL then 1 else 0 end) as  null_close
FROM gold_prices;
go

SELECT date, open_price, high_price, low_price, close_price
from gold_prices
where high_price<low_price
or  close_price>high_price
or close_price<low_price
or open_price> high_price
or open_price <low_price
or close_price <=0 
or open_price <=0;
go

SELECT date, high_price,low_price
from gold_prices
where high_price<low_price
go

SELECT date, high_price,close_price
from gold_prices
where high_price<close_price
go

SELECT date, high_price,low_price
from gold_prices
where low_price>close_price
go

SELECT DAY(date) as day_of_month, COUNT(*) as violation_count
FROM gold_prices
WHERE high_price < low_price OR close_price > high_price
   OR close_price < low_price OR open_price > high_price
   OR open_price < low_price OR close_price <= 0 OR open_price <= 0
GROUP BY DAY(date)
ORDER BY violation_count DESC;
go

SELECT YEAR(date) as yr, COUNT(*) as violation_count
FROM gold_prices
WHERE high_price < low_price OR close_price > high_price
   OR close_price < low_price OR open_price > high_price
   OR open_price < low_price OR close_price <= 0 OR open_price <= 0
GROUP BY YEAR(date)
ORDER BY yr;
go

ALTER TABLE gold_prices ADD data_quality_flag BIT NOT NULL DEFAULT 0;
go

UPDATE gold_prices
SET data_quality_flag = 1
WHERE high_price < low_price
   OR close_price > high_price
   OR close_price < low_price
   OR open_price > high_price
   OR open_price < low_price
   OR close_price <= 0
   OR open_price <= 0;
go

SELECT data_quality_flag, COUNT(*) FROM gold_prices GROUP BY data_quality_flag;
go