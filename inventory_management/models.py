from pydantic import BaseModel, Field, ConfigDict

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

class UserCreate(BaseModel):
    username: str
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)