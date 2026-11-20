from pydantic import BaseModel, EmailStr

class Employees(BaseModel):
    id : int
    name : str
    age : int
    department : str
    salary : float

class Employee_Patch(BaseModel):
    id : int | None = None
    name : str | None = None
    age : int | None = None
    department : str | None = None
    salary : float | None = None   

class AdminCreate(BaseModel):
    username : str
    email : EmailStr
    password : str

class AdminLogin(BaseModel):
    username : str
    password : str
