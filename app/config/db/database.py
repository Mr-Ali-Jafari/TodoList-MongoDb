# create database connection fastapi
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
# Create a database connection
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()
# Create a function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()