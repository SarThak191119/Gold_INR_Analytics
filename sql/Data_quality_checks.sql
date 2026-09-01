use GOLDTrackerDB
go

select top 50 * from dbo.usdinr_rate

select top 50 * from dbo.gold_prices

select count(*) from gold_prices
SELECT COUNT(*) FROM usdinr_rate;
SELECT TOP 5 * FROM usdinr_rate ORDER BY date DESC;