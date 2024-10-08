from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# .env dosyasını yükleyin
load_dotenv()

# Veritabanı URL'sini al
DATABASE_URL = os.getenv('DATABASE_URL')

# Engine'i oluştur
engine = create_engine(DATABASE_URL)

# SessionLocal'ı tanımlayın
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Log(Base):
    __tablename__ = 'log'
    
    id = Column(Integer, primary_key=True, index=True)
    user_question = Column(String(500), nullable=False)
    assistant_answer = Column(String(500), nullable=False)
    datetime = Column(DateTime(timezone=True), server_default=func.now())

class Blog(Base):
    __tablename__ = 'blog'  

    id = Column(Integer, primary_key=True, index=True)
    blog_name = Column(String(100), nullable=False)
    context = Column(String(500), nullable=False)
    author = Column(String(50), nullable=False)
