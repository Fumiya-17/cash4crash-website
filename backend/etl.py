import datetime
from sqlalchemy import func

# Main DB
from database import SessionLocal
import models

# Analytics DB
from analytics_database import SessionLocalAnalytics, engine, BaseAnalytics
from analytics_models import DailyStat, TopProduct

def run_etl():
    print("Starting ETL process...")
    # Initialize analytics tables if they don't exist
    BaseAnalytics.metadata.create_all(bind=engine)
    
    main_db = SessionLocal()
    analytics_db = SessionLocalAnalytics()
    
    try:
        # --- 1. Aggregating Customer Statistics ---
        total_users = main_db.query(models.User).count()
        total_orders = main_db.query(models.Order).count()
        total_revenue_q = main_db.query(func.sum(models.Order.total_spent)).scalar()
        total_revenue = float(total_revenue_q) if total_revenue_q else 0.0
        
        avg_order_value = 0.0
        if total_orders > 0:
            avg_order_value = total_revenue / total_orders
            
        today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        
        # Upsert DailyStat for today
        stat = analytics_db.query(DailyStat).filter(DailyStat.date == today_str).first()
        if not stat:
            stat = DailyStat(date=today_str)
            analytics_db.add(stat)
            
        stat.total_sales = total_orders
        stat.total_revenue = total_revenue
        stat.avg_order_value = avg_order_value
        stat.total_users = total_users
        
        # --- 2. Aggregating Top Products ---
        # Query OrderItem to sum quantity and revenue per car
        car_stats = main_db.query(
            models.OrderItem.car_id,
            models.OrderItem.brand,
            models.OrderItem.name,
            func.sum(models.OrderItem.quantity).label('total_sold'),
            func.sum(models.OrderItem.quantity * models.OrderItem.price).label('revenue')
        ).group_by(
            models.OrderItem.car_id,
            models.OrderItem.brand,
            models.OrderItem.name
        ).all()
        
        for cs in car_stats:
            prod = analytics_db.query(TopProduct).filter(TopProduct.car_id == cs.car_id).first()
            if not prod:
                prod = TopProduct(car_id=cs.car_id, brand=cs.brand, name=cs.name)
                analytics_db.add(prod)
                
            prod.total_sold = cs.total_sold
            prod.total_revenue = float(cs.revenue)
            
        analytics_db.commit()
        print(f"ETL completed successfully for {today_str}.")
        
    except Exception as e:
        analytics_db.rollback()
        print(f"ETL failed: {e}")
    finally:
        main_db.close()
        analytics_db.close()

if __name__ == "__main__":
    run_etl()
