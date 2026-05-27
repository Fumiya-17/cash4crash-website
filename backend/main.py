from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db, Base
import models, schemas
from jose import jwt
import logging
import datetime
import json
from typing import List

logging.basicConfig(level=logging.INFO)

# Create DB Tables
Base.metadata.create_all(bind=engine)

# Auto-seed the database on startup if it's empty
import seed_cars
try:
    seed_cars.seed()
except Exception as e:
    print(f"Auto-seeding skipped or failed: {e}")

app = FastAPI(title="Cash4Crash Backend")

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev. In prod: restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_user_uid(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = auth_header.split(" ")[1]
    
    try:
        # Decode the token without verifying the signature for local dev
        # In production with Firebase Admin, use verify_id_token()
        decoded = jwt.get_unverified_claims(token)
        uid = decoded.get("user_id")
        if not uid:
            raise ValueError("No user_id in token")
        return uid
    except Exception as e:
        logging.error(f"Token decoding error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/auth/sync")
def sync_user(payload: schemas.AuthSync, uid: str = Depends(get_current_user_uid), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uid == uid).first()
    if not user:
        user = models.User(
            uid=uid,
            name=payload.name,
            email=payload.email,
            street="", barangay="", city="", zip=""
        )
        db.add(user)
    else:
        user.name = payload.name
        user.email = payload.email
    db.commit()
    return {"status": "success"}

@app.get("/api/profile", response_model=schemas.ProfileResponse)
def get_profile(uid: str = Depends(get_current_user_uid), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uid == uid).first()
    
    if not user:
        user = models.User(uid=uid, name="", email="", street="", barangay="", city="", zip="")
        db.add(user)
        db.commit()
        db.refresh(user)
        
    orders = db.query(models.Order).filter(models.Order.owner_uid == uid).order_by(models.Order.created_at.desc()).all()
    
    orders_data = []
    for order in orders:
        items_data = []
        for item in order.items:
            items_data.append({
                "id": item.id,
                "name": item.name,
                "variant": item.variant,
                "price": item.price,
                "quantity": item.quantity
            })
        orders_data.append({
            "id": order.id,
            "total": order.total_spent,
            "created_at": order.created_at,
            "items": items_data
        })
    
    return {
        "is_admin": getattr(user, "is_admin", False),
        "street": user.street or "",
        "barangay": user.barangay or "",
        "city": user.city or "",
        "zip": user.zip or "",
        "total_spent": sum(order.total_spent for order in orders),
        "orders": orders_data
    }

@app.post("/api/profile/address")
def update_address(payload: schemas.AddressUpdate, uid: str = Depends(get_current_user_uid), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uid == uid).first()
    if not user:
        user = models.User(uid=uid, name=payload.name, email=payload.email, street=payload.street, barangay=payload.barangay, city=payload.city, zip=payload.zip)
        db.add(user)
    else:
        user.name = payload.name
        user.email = payload.email
        user.street = payload.street
        user.barangay = payload.barangay
        user.city = payload.city
        user.zip = payload.zip
    db.commit()
    return {"status": "success"}

@app.post("/api/checkout")
def process_checkout(payload: schemas.OrderCreate, uid: str = Depends(get_current_user_uid), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uid == uid).first()
    if not user or not user.street or not user.barangay or not user.city or not user.zip:
        raise HTTPException(status_code=400, detail="User must have a delivery address set")
        
    # Validate prices and calculate real total from database
    real_total = 0.0
    items_to_add = []
    for item in payload.items:
        car = db.query(models.Car).filter(models.Car.id == item.baseId).first()
        if not car:
            raise HTTPException(status_code=404, detail=f"Car {item.baseId} not found")
        real_total += (car.price * item.quantity)
        items_to_add.append((car, item))
        
    # Create order using secure backend total
    new_order = models.Order(
        owner_uid=uid,
        total_spent=real_total
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    # Add items
    for car, item in items_to_add:
        order_item = models.OrderItem(
            order_id=new_order.id,
            car_id=car.id,
            brand=car.id.split("-")[0].capitalize(),
            name=car.name,
            variant=item.color,
            price=car.price,
            quantity=item.quantity
        )
        db.add(order_item)
        
    db.commit()
    return {"status": "success", "order_id": new_order.id}

@app.get("/api/cars", response_model=List[schemas.CarResponse])
def get_cars(db: Session = Depends(get_db)):
    cars = db.query(models.Car).all()
    result = []
    for c in cars:
        try:
            specs = json.loads(c.specs) if c.specs else {}
        except:
            specs = {}
        result.append({
            "id": c.id, "brand": c.brand, "name": c.name, "make": c.make, 
            "model_year": c.model_year, "image": c.image, "price": c.price, "specs": specs
        })
    return result

@app.put("/api/admin/cars/{car_id}")
def update_car(car_id: str, payload: schemas.CarUpdate, uid: str = Depends(get_current_user_uid), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uid == uid).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
        
    car.brand = payload.brand
    car.name = payload.name
    car.make = payload.make
    car.model_year = payload.model_year
    car.image = payload.image
    car.price = payload.price
    car.specs = json.dumps(payload.specs)
    
    db.commit()
    return {"status": "success"}

@app.get("/api/admin/dashboard")
def get_dashboard(uid: str = Depends(get_current_user_uid), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uid == uid).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    import datetime
    from analytics_database import SessionLocalAnalytics
    from analytics_models import DailyStat, TopProduct
    
    analytics_db = SessionLocalAnalytics()
    try:
        today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        stat = analytics_db.query(DailyStat).filter(DailyStat.date == today_str).first()
        
        # If no stat generated yet for today, fallback to 0 or last available
        if not stat:
            stat = analytics_db.query(DailyStat).order_by(DailyStat.date.desc()).first()
            
        top_products = analytics_db.query(TopProduct).order_by(TopProduct.total_sold.desc()).limit(5).all()
        
        users_online = max(1, int(stat.total_users * 0.15)) if stat else 1
        
        return {
            "users_online": users_online,
            "total_revenue": stat.total_revenue if stat else 0.0,
            "total_orders": stat.total_sales if stat else 0,
            "total_users": stat.total_users if stat else 0,
            "avg_order_value": stat.avg_order_value if stat else 0.0,
            "top_products": [{"name": p.name, "brand": p.brand, "sold": p.total_sold, "revenue": p.total_revenue} for p in top_products],
            "top_brands": [] # Deprecated field but keeping array to prevent frontend crash
        }
    finally:
        analytics_db.close()
