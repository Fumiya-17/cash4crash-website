import json
from database import SessionLocal
from models import Car

cars_data = [
  {
    "id": "mercedes-1", "brand": "mercedes", "name": "AMG GT R", "make": "Mercedes-Benz", "model": "2023",
    "image": "img/mercedes.png", "price": 9200000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 2, "seats": 2, "mpg": 15}
  },
  {
    "id": "mercedes-2", "brand": "mercedes", "name": "G-Class G63", "make": "Mercedes-Benz", "model": "2024",
    "image": "img/mercedes.png", "price": 10100000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 5, "seats": 5, "mpg": 13}
  },
  {
    "id": "mercedes-3", "brand": "mercedes", "name": "S-Class S580", "make": "Mercedes-Benz", "model": "2023",
    "image": "img/mercedes.png", "price": 6700000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Hybrid", "doors": 4, "seats": 5, "mpg": 24}
  },
  {
    "id": "audi-1", "brand": "audi", "name": "R8 V10 Performance", "make": "Audi", "model": "2023",
    "image": "img/audi.png", "price": 8800000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 2, "seats": 2, "mpg": 14}
  },
  {
    "id": "audi-2", "brand": "audi", "name": "RS e-tron GT", "make": "Audi", "model": "2024",
    "image": "img/audi.png", "price": 8100000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Electric", "doors": 4, "seats": 5, "mpg": 85}
  },
  {
    "id": "audi-3", "brand": "audi", "name": "RS Q8", "make": "Audi", "model": "2023",
    "image": "img/audi.png", "price": 7000000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 5, "seats": 5, "mpg": 15}
  },
  {
    "id": "bmw-1", "brand": "bmw", "name": "M4 Competition", "make": "BMW", "model": "2024",
    "image": "img/bmw.png", "price": 4800000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 2, "seats": 4, "mpg": 19}
  },
  {
    "id": "bmw-2", "brand": "bmw", "name": "X5 M Competition", "make": "BMW", "model": "2023",
    "image": "img/bmw.png", "price": 6400000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 5, "seats": 5, "mpg": 15}
  },
  {
    "id": "bmw-3", "brand": "bmw", "name": "i8 Roadster", "make": "BMW", "model": "2020",
    "image": "img/bmw.png", "price": 8200000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Hybrid", "doors": 2, "seats": 2, "mpg": 69}
  },
  {
    "id": "ford-1", "brand": "ford", "name": "Mustang Mach-E", "make": "Ford", "model": "2023",
    "image": "img/bmw.png", "price": 2500000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Electric", "doors": 5, "seats": 5, "mpg": 90}
  },
  {
    "id": "ford-2", "brand": "ford", "name": "F-150 Raptor", "make": "Ford", "model": "2023",
    "image": "img/bmw.png", "price": 4300000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 4, "seats": 5, "mpg": 15}
  },
  {
    "id": "ford-3", "brand": "ford", "name": "Mustang Shelby GT500", "make": "Ford", "model": "2022",
    "image": "img/audi.png", "price": 4500000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 2, "seats": 4, "mpg": 14}
  },
  {
    "id": "vw-1", "brand": "volkswagen", "name": "Golf R", "make": "Volkswagen", "model": "2024",
    "image": "img/audi.png", "price": 2500000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 5, "seats": 5, "mpg": 23}
  },
  {
    "id": "vw-2", "brand": "volkswagen", "name": "ID.4 Pro", "make": "Volkswagen", "model": "2023",
    "image": "img/mercedes.png", "price": 2500000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Electric", "doors": 5, "seats": 5, "mpg": 99}
  },
  {
    "id": "vw-3", "brand": "volkswagen", "name": "Arteon", "make": "Volkswagen", "model": "2023",
    "image": "img/mercedes.png", "price": 2400000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 4, "seats": 5, "mpg": 25}
  },
  {
    "id": "bmw-featured", "brand": "bmw", "name": "M3 Competition xDrive", "make": "BMW", "model": "2023",
    "image": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=700&q=80&auto=format&fit=crop", "price": 4800000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 4, "seats": 5, "mpg": 16}
  },
  {
    "id": "mercedes-featured", "brand": "mercedes", "name": "C 300 AMG Line", "make": "Mercedes-Benz", "model": "2024",
    "image": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=700&q=80&auto=format&fit=crop", "price": 4200000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 4, "seats": 5, "mpg": 25}
  },
  {
    "id": "audi-featured", "brand": "audi", "name": "RS5 Sportback", "make": "Audi", "model": "2022",
    "image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=700&q=80&auto=format&fit=crop", "price": 3900000,
    "stock": 5, "specs": {"gearbox": "Automatic", "fuel": "Petrol", "doors": 4, "seats": 4, "mpg": 21}
  }
]

def seed():
    db = SessionLocal()
    try:
        if db.query(Car).count() > 0:
            print("Database already seeded.")
            return

        print("Seeding database...")
        db.query(Car).delete()
        
        for c in cars_data:
            car = Car(
                id=c["id"],
                brand=c["brand"],
                name=c["name"],
                make=c["make"],
                model_year=c["model"],
                image=c["image"],
                price=c["price"],
                specs=json.dumps(c["specs"])
            )
            db.add(car)
            
        db.commit()
        print("Database seeded with 15 cars successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
