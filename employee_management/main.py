from fastapi import FastAPI, Depends
from database import engine, get_db
from models import Base, Employees, Admin
from sqlalchemy.orm import Session
import schemas
import auth
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

Base.metadata.create_all(bind = engine)


@app.post('/admin/register')
def admin_register(admin:schemas.AdminCreate,db:Session = Depends(get_db)):
    existing_admin = db.query(Admin).filter(Admin.username == admin.username).first()
    if existing_admin:
        return {"message" : "Admin already registered"}
    hashed_password = auth.hashed_password(admin.password)
    new_admin = Admin(username = admin.username, email = admin.email, password = hashed_password)
    db.add(new_admin)
    db.commit()
    return {"message" : 'Admin added successfully'}


@app.post("/admin/login")
def admin_login(db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    admin = db.query(Admin).filter(Admin.username == form_data.username).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not auth.verify_password(form_data.password,admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = auth.create_access_token(data={"sub": admin.username})

    return {
        "access_token": access_token,
        "token_type": "Authorization->auth type->Bearer Token"
    }


@app.get('/employees')
def get_all(db:Session = Depends(get_db), current_admin: Admin = Depends(auth.get_current_admin)):
    db_employees = db.query(Employees).all()
    return db_employees

@app.get('/employees/{id}')
def get_by_id(id:int, db:Session = Depends(get_db), current_admin: Admin = Depends(auth.get_current_admin)):
    db_employee = db.query(Employees).filter(Employees.id == id).first()
    if db_employee:
        return db_employee
    return "Employee not found in the database"

@app.post('/employees')
def add_employee(employee:schemas.Employees, db:Session = Depends(get_db), current_admin: Admin = Depends(auth.get_current_admin)):
    db.add(Employees(**employee.model_dump()))
    db.commit()
    return "Employee added succesfully"

@app.put('/employees/{id}')
def update_employee(id:int, employee:schemas.Employees, db:Session = Depends(get_db), current_admin: Admin = Depends(auth.get_current_admin)):
    db_employee = db.query(Employees).filter(Employees.id == id).first()
    if db_employee:
        db_employee.name = employee.name
        db_employee.age = employee.age
        db_employee.department = employee.department
        db_employee.salary = employee.salary
        db.commit()
        return "Employee details are updated"
    return "Employee is not found in the databe to update"

@app.patch('/employees/{id}')
def patch_employee(id:int, employee: schemas.Employee_Patch, db:Session = Depends(get_db), current_admin: Admin = Depends(auth.get_current_admin)):
    db_employee = db.query(Employees).filter(Employees.id == id).first()
    if db_employee:
        update_data = employee.model_dump(exclude_unset = True)
        for key, value in update_data.items():
            setattr(db_employee, key, value)
        db.commit()
        return "Employee updated partially"
    return "Employee not found to update"

@app.delete('/employees/{id}')
def delete_Employee(id:int, db:Session = Depends(get_db), current_admin: Admin = Depends(auth.get_current_admin)):
    db_employee = db.query(Employees).filter(Employees.id == id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
        return "Employee deleted"
    return "Employee not found to delete"