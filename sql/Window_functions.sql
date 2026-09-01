with daily_returns as (
select date, gold_inr_per_10g_landed,(gold_inr_per_10g_landed/nullif(lag(gold_inr_per_10g_landed)over (order by date),0)-1)*100 as daily_pct_change
from gold_inr_derived)
select date,
gold_inr_per_10g_landed,
avg(gold_inr_per_10g_landed) over (order by date ROWS between 6 preceding and current ROW)
as moving_avg_7d,
avg(gold_inr_per_10g_landed) over (order by date ROWS between 29 preceding and current ROW) as moving_avg_30d,
round((gold_inr_per_10g_landed/nullif(lag(gold_inr_per_10g_landed,365) over (order by date),0)-1)*100,2) as year_on_y_pct_change,
stdev(daily_pct_change) over (order by date rows between 29 preceding and current row) as day_30_rolling_volatility
from daily_returns
order by date