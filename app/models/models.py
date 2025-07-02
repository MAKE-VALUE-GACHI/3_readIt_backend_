from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.functions import now

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    provider = Column(String)
    login_id = Column(String, unique=True, nullable=False)
    password = Column(String)
    profile_url = Column(String)
    email = Column(String)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), default=now())
    modified_at = Column(TIMESTAMP(timezone=True), default=now())
    deleted_at = Column(TIMESTAMP(timezone=True))

class Scrap(Base):
    __tablename__ = "scrap"

    id = Column(Integer, primary_key=True)
    task_id = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False, default="processing")
    user_id = Column(Integer, nullable=False)
    category_id = Column(String, nullable=True)
    type = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    origin_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=now())
    modified_at = Column(TIMESTAMP(timezone=True), default=now())

