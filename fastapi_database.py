from fastapi import FastAPI, Depends
from models import Customers
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind = engine)


customers = [
        Customers(id=1, name="Tony", email="tony@gmail.com", city="Hyderabad"),
        Customers(id=2, name="Hari", email="hari@gmail.com", city="Bangalore"),
        Customers(id=3, name="Ravi", email="ravi@gmail.com", city="Guntur"),
        Customers(id=4, name="Ramesh", email="ramesh@gmail.com", city="Chennai"),
        Customers(id=5, name="Suresh", email="suresh@gmail.com", city="Mumbai")
    ]


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Customers).count()
    if count == 0:
        for customer in customers:
            db.add(database_models.Customers(**customer.model_dump()))
        db.commit()
init_db()

@app.get('/customers')
def get_All_Users(db: Session = Depends(get_db)):
    db_customers = db.query(database_models.Customers).all()
    return db_customers


@app.get('/customer/{id}')
def get_customer_by_id(id:int, db: Session = Depends(get_db)):
    db_customer = db.query(database_models.Customers).filter(database_models.Customers.id == id).first()
    if  db_customer:
        return db_customer
    return "Customer not found"

@app.post('/customer')
def add_customer(Customer: Customers, db: Session = Depends(get_db)):
    db.add(database_models.Customers(**Customer.model_dump()))
    db.commit()
    return Customer

@app.put('/customer/{id}')
def update_customer(id:int, customer:Customers, db: Session = Depends(get_db)):
    db_customer = db.query(database_models.Customers).filter(database_models.Customers.id == id).first()
    if db_customer:
        db_customer.name = customer.name
        db_customer.email = customer.email
        db_customer.city = customer.city
        db.commit()
        return "Customer details are updated successfully"
    else:
        return "Customer not found"

@app.delete('/customer/{id}')
def delete_customer(id:int, db:Session = Depends(get_db)):
    db_customer = db.query(database_models.Customers).filter(database_models.Customers.id == id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return "Deletion successfull"
    return "Customer not found"