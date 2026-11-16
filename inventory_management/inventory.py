from models import Product, ProductPatch, UserCreate, UserResponse
from fastapi import FastAPI, Depends, HTTPException, status
from database import engine, session
import database_models
from sqlalchemy.orm import Session
from security import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from security import verify_password
from auth import create_access_token, oauth2_scheme, SECRET_KEY, ALGORITHM
import jwt
from jwt.exceptions import InvalidTokenError



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


@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(database_models.User).filter(database_models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
        status_code=400,
        detail="Username already exists"
    )
    hashed_password = hash_password(user.password)
    new_user = database_models.User(
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(database_models.User).filter(database_models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(
        user_credentials.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_current_user(
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

    except InvalidTokenError:
        raise credentials_exception

    user = db.query(database_models.User).filter(
        database_models.User.username == username
    ).first()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user

@app.get('/products')
def get_all(db:Session = Depends(get_db), current_user: database_models.User = Depends(get_current_user)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get('/products/{id}')
def get_by_id(id:int, db:Session = Depends(get_db), current_user: database_models.User = Depends(get_current_user)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product not found"

@app.post('/product')
def create_product(product:Product, db:Session = Depends(get_db),current_user: database_models.User = Depends(get_current_user)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return "Product added sucessfully"

@app.put('/product/{id}')
def update_product(id:int,product:Product, db:Session = Depends(get_db), current_user: database_models.User = Depends(get_current_user)):
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
def delete_product(id:int, db:Session = Depends(get_db), current_user: database_models.User = Depends(get_current_user)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    return "Product not found"


@app.patch('/product/{id}')
def patch_product(id: int, product: ProductPatch, db: Session = Depends(get_db), current_user: database_models.User = Depends(get_current_user)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        return "Product updated successfully"
    return "Product not found"