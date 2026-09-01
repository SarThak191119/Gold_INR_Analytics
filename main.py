from database import init_db, get_session
# from sqlalchemy.orm import sessionmaker
from fetch_data import fetch_historical_gold,fetch_todays_price, compute_quality_flag, fetch_historical_USD_INR_exchange_rate,fetch_todays_USD_INR_exchange_rate   
from models import GoldPrice 
from models import USDINR_rate
from models import ImportDuty
from datetime import date
# from sqlalchemy import engine, select
import pandas as pd



def load_gold_data(session):
    df=fetch_historical_gold(start_year=2004)
    inserted=0
    skipped=0
    for _, row in df.iterrows():
        exists=session.query(GoldPrice).filter_by(date=row['date']).first()
        if exists:
            skipped+=1
            continue
        record=GoldPrice(date=row['date'], 
                         open_price=row['open_price'],
                         high_price=row['high_price'],
                         low_price=row['low_price'],
                         close_price=row['close_price'],
                         volume=row['volume'],
                         currency=row['currency'],
                         data_quality_flag =compute_quality_flag(row))
        session.add(record)
        inserted+=1
        
    session.commit()
    print(f"Inserted {inserted} records, skipped {skipped} existing records.")
    today=fetch_todays_price()
    existing_today=session.query(GoldPrice).filter_by(date=today['date']).first()
    if existing_today:
        existing_today.close_price=today['close_price']
        existing_today.high_price=today['high_price']
        existing_today.low_price=today['low_price']
        existing_today.data_quality_flag=compute_quality_flag(today)
        print(f"Updated today's price for {today['date']}.")
    else:
        today['data_quality_flag']=compute_quality_flag(today)
        session.add(GoldPrice(**today))
    session.commit()

def load_usdinr_data(session):
    df=fetch_historical_USD_INR_exchange_rate(start_year=2004)
    inserted=0
    skipped=0
    for _, row in df.iterrows():
        exists=session.query(USDINR_rate).filter_by(date=row['date']).first()
        if exists:
            skipped+=1
            continue
        record=USDINR_rate(date=row['date'], 
                          close_price=row['close_price'])
        session.add(record)
        inserted+=1
        
    session.commit()
    print(f"Inserted {inserted} records, skipped {skipped} existing records.")


    today=fetch_todays_USD_INR_exchange_rate()
    existing_today=session.query(USDINR_rate).filter_by(date=today['date']).first()

    if existing_today:
        existing_today.close_price=today['close_price']
        print(f"Updated today's price for {today['date']}.")
    else:
        session.add(USDINR_rate(**today))
    session.commit()


def load_import_duty(session):
    duty_data = [
        {"effective_date": date(2013, 1, 1), "duty_pct": 6.0, "notes": "Baseline rate"},
        {"effective_date": date(2013, 6, 6), "duty_pct": 8.0, "notes": "Duty increased "},
        {"effective_date": date(2013, 8, 1), "duty_pct": 10.0, "notes": "Union Budget 2021-22 cut"},
        {"effective_date": date(2019, 1, 1), "duty_pct": 12.5, "notes": "Hiked amid rupee pressure"},
        {"effective_date": date(2021, 1, 1), "duty_pct": 10.75, "notes": "Union Budget 2024-25 cut"},
       {"effective_date": date(2022, 7, 1), "duty_pct": 15.0, "notes": "Hiked amid rupee pressure"},
        {"effective_date": date(2024, 7, 23), "duty_pct": 6.0, "notes": "Union Budget 2024-25 cut"},
       {"effective_date": date(2026, 7, 1), "duty_pct": 15.0, "notes": "Hiked amid rupee pressure"}
    ]
    session.query(ImportDuty).delete()
    for row in duty_data:
        session.add(ImportDuty(**row))
    session.commit()
    print(f"Import duty table reloaded: {len(duty_data)} rows")

def load_data():
    engine=init_db()
    session=get_session(engine)
    load_gold_data(session)
    load_usdinr_data(session)
    load_import_duty(session)
    session.close()


if __name__=="__main__":
    load_data()