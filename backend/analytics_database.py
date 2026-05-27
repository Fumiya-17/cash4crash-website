from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/cash4crash_analytics"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocalAnalytics = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseAnalytics = declarative_base()

def get_analytics_db():
    db = SessionLocalAnalytics()
    try:
        yield db
    finally:
        db.close()
