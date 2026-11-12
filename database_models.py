from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
Base = declarative_base()
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(100))
    price = Column(Float)
    quantity = Column(Integer)

class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key= True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    city = Column(String(100))