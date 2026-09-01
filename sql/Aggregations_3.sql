with dail_pct_returns as
(select date, gold_inr_per_10g_landed,
(gold_inr_per_10g_landed/nullif(lag(gold_inr_per_10g_landed) over (order by date),0)-1)*100 as daily_pct_change
from gold_inr_derived)
select month(date) as month_number,
datename(month,date) as month_name,
avg(daily_pct_change) as avg_percent_price_m,
avg(gold_inr_per_10g_landed) as avg_price_m
from dail_pct_returns
group by month(date), datename(month,date)
order by month_number

