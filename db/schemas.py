from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    login: str
    password: str


class UserCreate(UserBase):
    email: str


class User(UserBase):
    id: int
    token: Token

    class Config:
        orm_mode = True