from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.functions import now

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider = Column(String)
    login_id = Column(String, unique=True, nullable=False)
    password = Column(String)
    profile_url = Column(String)
    email = Column(String)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), default=now())
    modified_at = Column(TIMESTAMP(timezone=True), default=now())
    deleted_at = Column(TIMESTAMP(timezone=True))

    scraps = relationship('Scrap', back_populates='user')


class Scrap(Base):
    __tablename__ = "scrap"

    id = Column(Integer, primary_key=True)
    task_id = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False, default="processing")
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"))
    type = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
    like_count = Column(Integer, default=0, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    origin_url = Column(String, nullable=True)
    text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=now())
    modified_at = Column(TIMESTAMP(timezone=True), default=now())

    category = relationship('Category', back_populates='scraps', uselist=False)
    user = relationship('User', back_populates='scraps')
    likes = relationship('ScrapLike', back_populates='scrap', cascade='all, delete-orphan', lazy='dynamic')


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

    scraps = relationship('Scrap', back_populates='category')


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    scrap_id = Column(Integer, ForeignKey(Scrap.id), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=now())


class ScrapLike(Base):
    __tablename__ = 'scrap_like'

    user_id = Column('user_id', ForeignKey('user.id'), primary_key=True)
    scrap_id = Column('scrap_id', ForeignKey('scrap.id'), primary_key=True)

    scrap = relationship('Scrap', back_populates='likes')
