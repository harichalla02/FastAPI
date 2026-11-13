from models import Product, ProductPatch
from fastapi import FastAPI, Depends
from database import engine, session
import database_models
from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware

database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

products = [
    Product(id = 1, name = 'Mobile', description = 'RedMI phone with 12GB RAM, 256GB storage and white in clour', price = 25000, quantity = 10, category = "Electronics"),
    Product(id = 2, name = 'Laptop', description = 'Gaming Laptop with 16GB RAM, 512GB SSD and white in clour', price = 125000, quantity = 10, category = "Electronics"),
    Product(id = 3, name = 'Tablet', description = '10-inch Tablet with 8GB RAM, 128GB storage and black in clour', price = 35000, quantity = 15, category = "Electronics"),
    Product(id = 4, name = 'Watch', description = 'Smart Watch with fitness tracking and water resistance', price = 5000, quantity = 20, category = "Electronics")
    
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
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    db.close()
init_db()

@app.get('/products')
def get_all(db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get('/products/{id}')
def get_by_id(id:int, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product not found"

@app.post('/prodcut')
def create_product(product:Product, db:Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return "Product added sucessfully"

@app.put('/product/{id}')
def update_product(id:int,product:Product, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    print(db_product)
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db_product.category = product.category
        db.commit()
        return "Product updated successfully"
    return "Product not found"

@app.delete('/product/{id}')
def delete_product(id:int, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    return "Product not found"


@app.patch('/product/{id}')
def patch_product(id: int, product: ProductPatch, db: Session = Depends(get_db)):

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        return "Product updated successfully"
    return "Product not found"