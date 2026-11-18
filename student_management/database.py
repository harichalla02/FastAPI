from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "mysql+pymysql://root:MySql%4012345@localhost:3306/student_management"

engine = create_engine(db_url)

session = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
    