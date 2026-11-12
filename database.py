from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "mysql+pymysql://root:MySql%4012345@localhost:3306/fastapi_db"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)