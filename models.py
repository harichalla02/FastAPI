from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

class Users(BaseModel):
    id: int
    name: str
    email: str
    city: str

class Customers(BaseModel):
    id: int
    name: str
    email: str
    city: str
    

    