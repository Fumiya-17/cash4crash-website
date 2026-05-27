import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from analytics_database import BaseAnalytics

class DailyStat(BaseAnalytics):
    __tablename__ = "daily_stats"
    
    date = Column(String, primary_key=True, index=True) # Format: YYYY-MM-DD
    total_sales = Column(Integer, default=0)
    total_revenue = Column(Float, default=0.0)
    avg_order_value = Column(Float, default=0.0)
    total_users = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class TopProduct(BaseAnalytics):
    __tablename__ = "top_products"
    
    car_id = Column(String, primary_key=True, index=True)
    brand = Column(String)
    name = Column(String)
    total_sold = Column(Integer, default=0)
    total_revenue = Column(Float, default=0.0)
