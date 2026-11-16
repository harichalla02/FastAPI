from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key= True, index=True)
    name = Column(String(100))
    description = Column(String(200))
    price = Column(Float)
    quantity = Column(Integer)
    category = Column(String(100))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)