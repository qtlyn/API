from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
pwd=os.getenv("pwd_db")
DB_URL = f"mssql+pyodbc://sa:{pwd}@LYN\\LYN/USER_DB?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__="users"
    Id = Column(Integer, primary_key=True,index=True,autoincrement=False)
    Ten = Column(String,index=True)
    DiaChi =Column(String)
    Email = Column(String, unique=True, index=True)

def get_db():
    db=SessionLocal()
    try: 
        yield db
    finally:
        db.close()