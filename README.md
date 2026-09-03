# Gold Price (INR) Decomposition Dashboard

**Live dashboard:** https://goldinranalytics-w5jdwgnvexyqbn4uaw2wcg.streamlit.app/ 

**Repo:** https://github.com/SarThak191119/Gold_INR_Analytics

## What this project answers

Gold prices in India move for three  main reasons: the global gold price (in USD), the USD/INR exchange rate, and the government's import duty policy. Any trend of gold prices can be broadly broken down into these 3 factors.

Concretely, it quantitatively shows on any given day, how much of the change in the Indian gold price is affected by these factors.

## Data Sources

The global gold prices and forex prices are pulled from Yahoo
Finance via 'yfinance' :
| Series | Ticker | Notes |
|---|---|---|
| Gold futures (USD/oz) | `GC=F` | Daily OHLCV (Open, High, Low, Close, and Volume), 2004–present |
| USD/INR exchange rate | `INR=X` | Daily close |
| Import duty on gold | manually compiled | ~8 rate changes since 2013, sourced from public Union Budget announcements [Source:Financial Express](https://www.financialexpress.com/policy/economy/why-was-the-import-duty-on-gold-raised/4240070/) |

The INR price of gold is derived and is the price of 10g as used conventionally (3.11035 is the conversion factor from ounces to 10g).  

```
gold_inr_per_10g_global = gold_usd_oz × usd_inr_rate ÷ 3.11035
gold_inr_per_10g_landed = gold_inr_per_10g_global × (1 + duty_pct / 100)
```
## Architecture

```
Yahoo Finance (yfinance)
        │
        ▼
  fetch_data.py  →  SQL Server (SQLAlchemy models)
        │               │
        │               ├── gold_prices
        │               ├── usd_inr_rate
        │               └── import_duty
        │               │
        │               ▼
        │         gold_inr_derived (SQL view — joins all three,
        │         with an as-of match for the duty rate in effect
        │         on each date)
        │               │
        ▼               ▼
  export_sql_snapshot.py  →  data_export/*.csv
                                    │
                                    ▼
                          dashboard/app.py (Streamlit)
```

The dashboard reads from an **exported CSV snapshot**, not a live query against SQL server. The full pipeline, schema and analysis queries for a SQL server integration though are all in this repo and can be run against a private SQL server instance to reproduce or refresh the data. 

Requires a running SQL Server instance with ODBC Driver 17 installed.

## Tech stack

Python, SQL Server, SQLAlchemy, pandas, Streamlit, Plotly, yfinance

## Caveats

-  Even though the first panel says import duty is 0% what it actually means is that before 2012 the tax was not *ad valorem* or a percentage of the value of the gold but instead was a flat Rs 300 for 10g. 

- `GC=F` is the global futures price and not India's actual spot price, so the price per 10g is a derived estimate, not an official quoted rate. This helps the decompisition possible. A future direction might be to compare with India's officially reported gold prices so as to further complement this study.

- Yahoo finance sources data from 2004 to present date. On further investigation ~386 rows  (concentrated in 2004-2011) were found to have discrepancies (close price fell outside high/low range) which are flagged in the database with the (`data_quality_flag`), not deleted. These are mostly concentrated between 2004-2011 and due to the shift towards continous elecrtonic (Globex) trading, before which settlement prices could reasonably diverge from the intraday trading range.  

## Reproducing the pipeline locally

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in your own SQL Server details
python fetch_data.py
python main.py
python export_sql_snapshot.py
streamlit run dashboard/app.py
```


