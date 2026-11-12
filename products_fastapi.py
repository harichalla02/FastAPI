from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import database_models
from database import session, engine
from models import Product
from fastapi.middleware.cors import CORSMiddleware

database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)

Products = [
    Product(id = 1, name = 'Mobile', description = 'RedMI phone with 12GB RAM, 256GB storage and white in clour', price = 25000, quantity = 10),
    Product(id = 2, name = 'Laptop', description = 'Gaming Laptop with 16GB RAM, 512GB SSD and white in clour', price = 125000, quantity = 10),
    Product(id = 3, name = 'Tablet', description = '10-inch Tablet with 8GB RAM, 128GB storage and black in clour', price = 35000, quantity = 15),
    Product(id = 4, name = 'Watch', description = 'Smart Watch with fitness tracking and water resistance', price = 5000, quantity = 20)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    if count == 0:
        for product in Products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    db.close()
init_db()    

@app.get("/products/")
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(database_models.Product).all()
    return products


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if product:
        return product
    return "Product not found"

@app.post("/products/")
def create_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return "Product created successfully"


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
       return "Product not found"
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    "Product updated successfully"


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        return "Product not found"
    db.delete(db_product)
    db.commit()
    return "Product deleted successfully"