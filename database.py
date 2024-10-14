# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/Employees"

# engine = create_engine(DATABASE_URL)

# SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

import psycopg2

DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/Employees"

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="Employees",
        user="myuser",
        password="mypassword"
    )
    return conn