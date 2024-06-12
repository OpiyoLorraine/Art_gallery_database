# database/connection.py

import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite connection for direct SQL operations
def get_db_connection():
    conn = sqlite3.connect('artgallery.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

# SQLAlchemy setup for ORM
DATABASE_URL = "sqlite:///artgallery.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
