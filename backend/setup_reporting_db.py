import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect("dbname='postgres' user='postgres' password='admin' host='localhost'")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
try:
    cur.execute("CREATE DATABASE cash4crash_reporting_db;")
    print("Database cash4crash_reporting_db created successfully.")
except Exception as e:
    print(f"Error (maybe it already exists?): {e}")
cur.close()
conn.close()

from reporting_db import engine
from reporting_models import Base
Base.metadata.create_all(bind=engine)
print("Reporting tables created successfully!")
