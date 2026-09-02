import pandas as pd
from sqlalchemy import create_engine, text
from config import CONNECTION_STRING
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "data_export")

os.makedirs(OUT_DIR, exist_ok=True)

engine=create_engine(CONNECTION_STRING)

QUERIES={
    "gold_inr_derived": """
    SELECT * FROM gold_inr_derived ORDER by date
""",

    "decomposition": """
        with base as (
            select date, gold_usd_oz, usdinr_rate,duty_pct,gold_inr_per_10g_landed
            from gold_inr_derived),
        with_lag as (
            select date, gold_usd_oz, usdinr_rate, duty_pct, gold_inr_per_10g_landed,
            lag(gold_usd_oz) over (order by date) as prev_gold_usd_oz,
            lag(usdinr_rate) over (order by date) as prev_usdinr_rate,
            lag(duty_pct) over (order by date) as prev_duty_pct,
            lag(gold_inr_per_10g_landed) over (order by date) as prev_landed_price
            from base)

    select date, gold_inr_per_10g_landed,
        round((gold_inr_per_10g_landed/Nullif(prev_landed_price,0)-1)*100,4) as gold_inr_change,
        round((gold_usd_oz/Nullif(prev_gold_usd_oz,0)-1)*100,4) as gold_usd_change,
        round((usdinr_rate/Nullif(prev_usdinr_rate,0)-1)*100,2) as usdinr_change,
        round((duty_pct-prev_duty_pct),4) as duty_change_pp
        from with_lag
        where prev_landed_price is not null
        order by date
        """,
    "window_function":"""
        with daily_returns as (
        select date, gold_inr_per_10g_landed, (gold_inr_per_10g_landed/nullif(lag(gold_inr_per_10g_landed) over (order by date),0)-1)*100 as daily_pct_change
        from gold_inr_derived)
        select date, gold_inr_per_10g_landed,
        avg(gold_inr_per_10g_landed) over (order by date rows between 6 preceding and current row) as moving_avg_7d,
        avg(gold_inr_per_10g_landed) over (order by date rows between 29 preceding and current row) as moving_avg_30d,
        round((gold_inr_per_10g_landed/nullif(lag(gold_inr_per_10g_landed,365) over (order by date),0)-1)*100,2) as year_on_year_pct_change,
        stdev(daily_pct_change) over (order by date rows between 29 preceding and current row) as day_30_rolling_volatility
        from daily_returns
        order by date""",
    "monthly_aggregation":"""
        select 
        year(date) as yr, month(date) as mo,
        avg(gold_inr_per_10g_landed) as avg_price,
        min(gold_inr_per_10g_landed) as min_price,
        max(gold_inr_per_10g_landed) as max_price
        from gold_inr_derived
        group by year(date), month(date)
        order by yr, mo""",
        "import_duty":"""
        select effective_date, duty_pct, notes from import_duty 
        order by effective_date
        """}

for name, query in QUERIES.items():
    print(f"Exporting {name} ...")
    df=pd.read_sql(text(query), engine)
    out_path=os.path.join(OUT_DIR,f"{name}.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} rows to {out_path}")

    print("Complete.")