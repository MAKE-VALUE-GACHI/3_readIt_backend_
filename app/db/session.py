from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URI = "mariadb+pymysql://username:password@mariadb:port/endpoint"

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)