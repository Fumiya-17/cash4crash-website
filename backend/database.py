from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# We use SQLite for local dev since postgres wasn't found. 
# This URL will be changed to a postgresql URL in production (e.g. postgresql://user:pass@host/db)
#SQLALCHEMY_DATABASE_URL = "sqlite:///./cash4crash.db"

import os
from urllib.parse import urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://postgres:admin@db:5432/cash4crash_db"
)

if SQLALCHEMY_DATABASE_URL.startswith("postgresql"):
    parsed = urlparse(SQLALCHEMY_DATABASE_URL)
    db_name = parsed.path.lstrip('/')
    try:
        try:
            conn = psycopg2.connect(
                user=parsed.username,
                password=parsed.password,
                host=parsed.hostname,
                port=parsed.port,
                dbname='postgres'
            )
        except psycopg2.OperationalError:
            conn = psycopg2.connect(
                user=parsed.username,
                password=parsed.password,
                host=parsed.hostname,
                port=parsed.port,
                dbname='template1'
            )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f'CREATE DATABASE "{db_name}"')
        conn.close()
    except Exception as e:
        print(f"Error creating database {db_name}: {e}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
