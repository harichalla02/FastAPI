from pydantic import BaseModel, EmailStr

class Student(BaseModel):
    id : int
    name : str
    age : int
    email: EmailStr
    course : str
    city : str

class Student_patch(BaseModel):
    id : int | None = None
    name : str | None = None
    age : int | None = None
    email: EmailStr | None = None
    course : str | None = None
    city : str | None = None

class AdminCreate(BaseModel):
    username : str
    email : EmailStr
    password : str

class AdminLogin(BaseModel):
    username : str
    password : str