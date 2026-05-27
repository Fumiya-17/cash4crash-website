from sqlalchemy import Column, Integer, String, Float, DateTime, Date
import datetime
from reporting_db import Base

class DailyMetrics(Base):
    __tablename__ = "daily_metrics"
    
    date = Column(Date, primary_key=True, index=True)
    total_revenue = Column(Float, default=0.0)
    total_orders = Column(Integer, default=0)
    users_online = Column(Integer, default=0) 

class TopProduct(Base):
    __tablename__ = "top_products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    variant = Column(String)
    total_sold = Column(Integer, default=0)

class TopBrand(Base):
    __tablename__ = "top_brands"
    
    brand = Column(String, primary_key=True, index=True)
    total_sold = Column(Integer, default=0)
