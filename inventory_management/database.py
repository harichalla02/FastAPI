from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "mysql+pymysql://root:MySql%4012345@localhost:3306/inventory_management"

engine = create_engine(db_url)

session = sessionmaker(autoflush= False, autocommit = False, bind= engine)