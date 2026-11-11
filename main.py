from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get('/')
def greet():
    return "Welcome to Fast API learning session"

products = [
    Product(id = 1, name = 'Mobile', description = 'RedMI phone with 12GB RAM, 256GB storage and white in clour', price = 25000, quantity = 10),
    Product(id = 2, name = 'Laptop', description = 'Gaming Laptop with 16GB RAM, 512GB SSD and white in clour', price = 125000, quantity = 10),
    Product(id = 3, name = 'Tablet', description = '10-inch Tablet with 8GB RAM, 128GB storage and black in clour', price = 35000, quantity = 15),
    Product(id = 4, name = 'Watch', description = 'Smart Watch with fitness tracking and water resistance', price = 5000, quantity = 20)
]
@app.get('/products')
def get_All_Products():
    return products


@app.get('/product/{id}')
def get_product_by_id(id:int):
    for product in products:
        if product.id == id:
            return product
    return "Product not found"


@app.post('/product')
def add_product(product:Product):
    products.append(product)
    return product

@app.put('/prodct')
def update_prodct(id:int, product:Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product updated successfully"
    return "Product not found"


@app.delete('/product')
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Product deleted"
    return "Product not found"