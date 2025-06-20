from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.functions import now

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    provider = Column(String)
    login_id = Column(String, unique=True, nullable=False)
    password = Column(String)
    email = Column(String)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), default=now())
    modified_at = Column(TIMESTAMP(timezone=True), default=now())
    deleted_at = Column(TIMESTAMP(timezone=True))
