import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# .env file se environment variables load karein
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable set nahi hai!")

# Database connection engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session manager
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model class
Base = declarative_base()

# Request dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()