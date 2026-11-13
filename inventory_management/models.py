from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int
    category: str

class ProductPatch(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None
    category: str | None = None