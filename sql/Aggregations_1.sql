select year(date) as yr,
month(date) as mo,
avg(gold_inr_per_10g_landed) as avg_price,
min(gold_inr_per_10g_landed) as min_price,
max(gold_inr_per_10g_landed) as max_price
from gold_inr_derived
group by Year(date) , month(date)
order by yr, mo