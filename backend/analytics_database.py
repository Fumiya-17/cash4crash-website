from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from urllib.parse import urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

SQLALCHEMY_DATABASE_URL = os.environ.get(
    "ANALYTICS_DATABASE_URL", 
    "postgresql://postgres:admin@db:5432/cash4crash_analytics"
)

if SQLALCHEMY_DATABASE_URL.startswith("postgresql"):
    parsed = urlparse(SQLALCHEMY_DATABASE_URL)
    db_name = parsed.path.lstrip('/')
    try:
        try:
            # Connect to 'postgres' first
            conn = psycopg2.connect(
                user=parsed.username,
                password=parsed.password,
                host=parsed.hostname,
                port=parsed.port,
                dbname='postgres'
            )
        except psycopg2.OperationalError:
            # Fallback to 'template1'
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
SessionLocalAnalytics = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseAnalytics = declarative_base()

def get_analytics_db():
    db = SessionLocalAnalytics()
    try:
        yield db
    finally:
        db.close()
