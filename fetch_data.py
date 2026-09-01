import yfinance as yf
import pandas as pd
from datetime import datetime, date

def fetch_historical_gold(start_year: int=2001) -> pd.DataFrame:
    """  Fetch historical gold price data from Yahoo Finance starting from the specified year."""
    start_date=f"{start_year}-01-01"
    end_date=datetime.today().strftime('%Y-%m-%d')

    print(f"Fetching gold data from {start_date} to {end_date}...")
    ticker=yf.Ticker("GC=F")
    df=ticker.history(start=start_date, end=end_date,interval="1d")

    if df.empty:
        raise ValueError("No data fetched. ERROR.") 
    

    df=df.reset_index()
    df=df.rename(columns={"Date": "date", "Open": "open_price", "High": "high_price", "Low": "low_price", "Close": "close_price", "Volume": "volume"})
    df["date"]=pd.to_datetime(df["date"]).dt.date
    df["currency"]="USD"

    return df[["date", "open_price", "high_price", "low_price", "close_price", "volume", "currency"]]

def fetch_todays_price() -> dict:
    """ Fetch today's gold price data from Yahoo Finance."""
    ticker=yf.Ticker("GC=F")
    info=ticker.fast_info
    return {
        "date": date.today(),
        "open_price": info.open,
        "high_price": info.day_high,
        "low_price": info.day_low,
        "close_price": info.last_price,
        "volume": info.three_month_average_volume,
        "currency": "USD"
}   


def fetch_todays_USD_INR_exchange_rate() -> dict:
    """ Fetch today's USD to INR exchange rate data from Yahoo Finance."""
    ticker=yf.Ticker("INR=X")
    info=ticker.fast_info
    return {
        "date": date.today(),
        "close_price": info.last_price,
}   

def compute_quality_flag(row):
    return bool(
        row['high_price'] < row['low_price'] or
        row['close_price'] > row['high_price'] or
        row['close_price'] < row['low_price'] or
        row['open_price'] > row['high_price'] or
        row['open_price'] < row['low_price'] or
        row['close_price'] <= 0 or
        row['open_price'] <= 0
    )


def fetch_historical_USD_INR_exchange_rate(start_year: int=2001) -> pd.DataFrame:
    """ Fetch the historical USD to INR exchange rate from Yahoo Finance starting from the specified year."""
    start_date=f"{start_year}-01-01"
    end_date=datetime.today().strftime('%Y-%m-%d')
    print(f"Fetching USD to INR exchange rate data from {start_date} to {end_date}...")
    ticker = yf.Ticker("INR=X")
    df =ticker.history(start=start_date, end=end_date, interval="1d")
    if df.empty:
        raise ValueError("No data fetched for USD to INR exchange rate. ERROR.")
    df=df.reset_index()
    df=df.rename(columns={"Date":"date", "Close":"close_price"})
    df["date"]=pd.to_datetime(df["date"]).dt.date    
    return df[["date", "close_price"]]
