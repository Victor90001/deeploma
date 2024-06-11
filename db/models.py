from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .connect import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    access_token = relationship("Token", back_populates="user")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.id"))
    access_token = Column(String)
    token_type = Column(String)

    user = relationship("User", back_populates="access_token")