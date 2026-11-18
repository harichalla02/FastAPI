from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50)) 
    age = Column(Integer)
    email = Column(String(50), unique=True)
    course = Column(String(30))
    city = Column(String(30))

class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(400))

