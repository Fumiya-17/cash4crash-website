from pydantic import BaseModel
from typing import List, Optional
import datetime
from typing import Dict, Any

class CarUpdate(BaseModel):
    brand: str
    name: str
    make: str
    model_year: str
    image: str
    price: float
    specs: Dict[str, Any]

class CarResponse(BaseModel):
    id: str
    brand: str
    name: str
    make: str
    model_year: str
    image: str
    price: float
    specs: Dict[str, Any]

    class Config:
        orm_mode = True

class AuthSync(BaseModel):
    name: str
    email: str

class AddressUpdate(BaseModel):
    name: str
    email: str
    street: str
    barangay: str
    city: str
    zip: str

class OrderItemCreate(BaseModel):
    id: str
    baseId: str
    name: str
    imgUrl: str
    price: str
    color: str
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    total: float

class OrderItemResponse(BaseModel):
    id: int
    name: str
    variant: str
    price: float
    quantity: int

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    total: float
    created_at: datetime.datetime
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True

class ProfileResponse(BaseModel):
    is_admin: bool
    street: str
    barangay: str
    city: str
    zip: str
    total_spent: float
    orders: List[OrderResponse]
