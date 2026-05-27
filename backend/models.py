from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime
from database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(String, primary_key=True, index=True)
    brand = Column(String, index=True)
    name = Column(String)
    make = Column(String)
    model_year = Column(String)
    image = Column(String)
    price = Column(Float)
    stock = Column(Integer, default=5)
    specs = Column(String) # Store as JSON string

class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, index=True) # Firebase UID
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    street = Column(String, nullable=True)
    barangay = Column(String, nullable=True)
    city = Column(String, nullable=True)
    zip = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    
    orders = relationship("Order", back_populates="owner")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    owner_uid = Column(String, ForeignKey("users.uid"))
    total_spent = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    owner = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    car_id = Column(String, index=True)
    brand = Column(String, index=True)
    name = Column(String)
    variant = Column(String)
    price = Column(Float)
    quantity = Column(Integer, default=1)
    
    order = relationship("Order", back_populates="items")
