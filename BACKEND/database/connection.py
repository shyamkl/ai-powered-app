from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:463165Shyam@localhost/happyhour"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)