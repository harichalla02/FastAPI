from database import get_db, session, engine
import schemas
import databasemodels 
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
import security
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from config import SECRET_KEY, ALGORITHM
import jwt

app = FastAPI()

databasemodels.Base.metadata.create_all(bind = engine)

@app.post('/admin/register')
def admin_register(admin: schemas.AdminCreate, db:Session = Depends(get_db)):
    existing_admin = db.query(databasemodels.Admin).filter(databasemodels.Admin.email == admin.email).first()
    if existing_admin:
        return "Admin already registered"
    hashed_password = security.hash_password(admin.password)
    new_admin = databasemodels.Admin(
        username = admin.username,
        email = admin.email,
        password = hashed_password
    )
    db.add(new_admin)
    db.commit()
    return "Admin added successfully"


@app.post("/admin/login")
def admin_login(db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    admin = db.query(databasemodels.Admin).filter(databasemodels.Admin.username == form_data.username).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not security.verify_password(form_data.password,admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = security.create_access_token(data={"sub": admin.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/admin/login"
)


def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception

    admin = db.query(databasemodels.Admin).filter(
        databasemodels.Admin.username == username
    ).first()

    if admin is None:
        raise credentials_exception

    return admin



@app.get('/students')
def get_all(db:Session = Depends(get_db), current_admin: databasemodels.Admin = Depends(security.get_current_admin)):
    db_students = db.query(databasemodels.Student).all()
    return db_students

@app.get('/students/{id}')
def get_by_is(id:int, db:Session = Depends(get_db), current_admin: databasemodels.Admin = Depends(security.get_current_admin)):
    db_student = db.query(databasemodels.Student).filter(databasemodels.Student.id == id).first()
    if db_student:
        return db_student
    return "Studnet not found in the database"

@app.post('/students')
def add_student(student:schemas.Student, db:Session = Depends(get_db), current_admin: databasemodels.Admin = Depends(security.get_current_admin)):
    db.add(databasemodels.Student(**student.model_dump()))
    db.commit()
    return "Student added succesfully"

@app.put('/students/{id}')
def update_student(id:int, student: schemas.Student, db:Session = Depends(get_db), current_admin: databasemodels.Admin = Depends(security.get_current_admin)):
    db_student = db.query(databasemodels.Student).filter(databasemodels.Student.id == id).first()
    if db_student:
        db_student.name = student.name
        db_student.age = student.age
        db_student.email = student.email
        db_student.course = student.course
        db_student.city = student.city
        
        db.commit()
        return "Student details are updated"
    return "Student is not found in the databe to update"

@app.patch('/students/{id}')
def patch_update(id:int, student: schemas.Student_patch, db:Session = Depends(get_db), current_admin: databasemodels.Admin = Depends(security.get_current_admin)):
    db_student = db.query(databasemodels.Student).filter(databasemodels.Student.id == id).first()
    if db_student:
        update_data = student.model_dump(exclude_unset = True)
        for key, value in update_data.items():
            setattr(db_student, key, value)
        db.commit()
        return "Student updated partially"
    return "Student not found to update"

@app.delete('/students/{id}')
def delete_student(id:int, db:Session = Depends(get_db), current_admin: databasemodels.Admin = Depends(security.get_current_admin)):
    db_student = db.query(databasemodels.Student).filter(databasemodels.Student.id == id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return "Student deleted"
    return "Student not found to delete"