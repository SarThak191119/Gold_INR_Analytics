# Gold Price (INR) Decomposition Dashboard

**Live dashboard:** https://goldinranalytics-w5jdwgnvexyqbn4uaw2wcg.streamlit.app/ 
**Repo:** https://github.com/SarThak191119/Gold_INR_Analytics

What this project answers

Gold prices in India move for three  main reasons: the global gold price (in USD), the USD/INR exchange rate, and the government's import duty policy. Any trend of gold prices can be broadly broken down into these 3 factors.

Concretely, it quantitatively shows on any given day, how much of the change in the Indian gold price is affected by these factors.

## Data Sources

The global gold prices and forex prices are pulled from Yahoo
Finance via 'yfinance' :
| Series | Ticker | Notes |
|---|---|---|
| Gold futures (USD/oz) | `GC=F` | Daily OHLCV, 2004–present |
| USD/INR exchange rate | `INR=X` | Daily close |
| Import duty on gold | manually compiled | ~8 rate changes since 2013, sourced from public Union Budget announcements [Source:Financial Express](https://www.financialexpress.com/policy/economy/why-was-the-import-duty-on-gold-raised/4240070/) |
