select year(date) as y,
avg(gold_inr_per_10g_landed) as avg_price_y,
max(gold_inr_per_10g_landed) as max_price_y,
min(gold_inr_per_10g_landed) as min_price_y,
count(*) as trading_days
from gold_inr_derived
group by year(date)
order by y