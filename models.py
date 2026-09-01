from sqlalchemy import Column, Integer, Float, Date, DateTime, String, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base=declarative_base()

class GoldPrice(Base):
    __tablename__ = 'gold_prices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date=Column(Date, nullable=False,unique=True)
    open_price=Column(Float)
    high_price=Column(Float)
    low_price=Column(Float)
    close_price=Column(Float,nullable=False)
    volume = Column(Float)
    currency = Column(String(10))
    data_quality_flag = Column(Boolean, default=False, nullable=False)
    created_at=Column(DateTime, default=datetime.now)

class USDINR_rate(Base):
    __tablename__ = 'usdinr_rate'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date=Column(Date, nullable=False,unique=True)
    close_price=Column(Float,nullable=False)
    created_at=Column(DateTime, default=datetime.now)

class ImportDuty(Base):
    __tablename__ = 'import_duty'
    id = Column(Integer, primary_key=True, autoincrement=True)
    effective_date = Column(Date, nullable=False, unique=True)
    duty_pct = Column(Float, nullable=False)
    notes = Column(String(200))
