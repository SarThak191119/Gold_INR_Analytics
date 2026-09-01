use GOLDTrackerDB
go

with base as (
select date, gold_usd_oz, usdinr_rate, duty_pct, gold_inr_per_10g_landed
from gold_inr_derived),
with_lag as (
select date,gold_usd_oz,usdinr_rate, duty_pct, gold_inr_per_10g_landed,
lag(gold_usd_oz) over(order by date) as prev_gold_usd_oz,
lag(usdinr_rate) over(order by date) as prev_usdinr_rate,
lag(duty_pct) over(order by date) as prev_duty_pct,
lag(gold_inr_per_10g_landed) over(order by date) as prev_landed_price
from base
)
select date,gold_inr_per_10g_landed,
round((gold_inr_per_10g_landed/Nullif(prev_landed_price,0)-1)*100,4) as gold_inr_change,
round((gold_usd_oz/Nullif(prev_gold_usd_oz,0)-1)*100,4) as gold_usd_change,
round((usdinr_rate/Nullif(prev_usdinr_rate,0)-1)*100,2) as usd_inr_change,
round((duty_pct-prev_duty_pct),4) as duty_change_pp
from with_lag
where prev_landed_price IS NOT NULL
Order by date

