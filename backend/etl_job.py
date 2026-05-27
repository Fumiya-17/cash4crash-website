from database import SessionLocal as MainSession
from reporting_db import SessionLocal as ReportSession
from models import User, Order, OrderItem
from reporting_models import DailyMetrics, TopProduct, TopBrand
import datetime
from sqlalchemy import func

def run_etl():
    main_db = MainSession()
    report_db = ReportSession()
    
    try:
        today = datetime.date.today()
        
        # Extract total revenue and total orders
        total_revenue = main_db.query(func.sum(Order.total_spent)).scalar() or 0.0
        total_orders = main_db.query(func.count(Order.id)).scalar() or 0
        
        # Estimate users online: Rough estimate based on total users
        total_users = main_db.query(func.count(User.uid)).scalar() or 0
        users_online = max(1, int(total_users * 0.15)) 
        
        # Load into DailyMetrics
        metrics = report_db.query(DailyMetrics).filter(DailyMetrics.date == today).first()
        if not metrics:
            metrics = DailyMetrics(date=today)
            report_db.add(metrics)
        
        metrics.total_revenue = total_revenue
        metrics.total_orders = total_orders
        metrics.users_online = users_online
        
        # Clear existing top products and brands for current snapshot
        report_db.query(TopProduct).delete()
        report_db.query(TopBrand).delete()
        
        # Aggregate products
        product_sales = {}
        brand_sales = {}
        for item in main_db.query(OrderItem).all():
            prod_key = f"{item.name} - {item.variant}"
            product_sales[prod_key] = product_sales.get(prod_key, 0) + item.quantity
            
            # Simple brand extraction: first word of car name
            brand = item.name.split(" ")[0]
            brand_sales[brand] = brand_sales.get(brand, 0) + item.quantity
            
        # Insert top products (top 5)
        sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
        for name_var, qty in sorted_products:
            name, variant = name_var.split(" - ")
            tp = TopProduct(name=name, variant=variant, total_sold=qty)
            report_db.add(tp)
            
        # Insert top brands (top 5)
        sorted_brands = sorted(brand_sales.items(), key=lambda x: x[1], reverse=True)[:5]
        for brand, qty in sorted_brands:
            tb = TopBrand(brand=brand, total_sold=qty)
            report_db.add(tb)
            
        report_db.commit()
        print(f"ETL completed successfully for {today}!")
        
    except Exception as e:
        report_db.rollback()
        print(f"ETL failed: {e}")
    finally:
        main_db.close()
        report_db.close()

if __name__ == "__main__":
    run_etl()
