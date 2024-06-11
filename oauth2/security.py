from datetime import datetime, timedelta, timezone
from typing import Annotated
import os
from fastapi import Depends, APIRouter, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.schemas import User, Token
from db.crud import get_user_by_login, get_uid_by_token, update_user_token
from db.models import User as dbUser
from db import connect
from detection import detect

# to get a string like this run:
# openssl rand -hex 32
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
SECRET_KEY = os.environ["JWT_SECRET"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    login: str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


def get_db():
    db = connect.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, login: str, password: str):
    user = get_user_by_login(db, login)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         login: str = payload.get("sub")
#         if login is None:
#             raise credentials_exception
#         token_data = TokenData(login=login)
#     except JWTError:
#         raise credentials_exception
#     user = get_user_by_login(db, login=token_data.login)
#     if user is None:
#         raise credentials_exception
#     user_token = get_user_token(db, user.id)
#     if user_token is None:
#         raise credentials_exception
#     user_info = User(
#                     id=user.id, 
#                     is_active=user.is_active, 
#                     token={
#                         'access_token': user_token.token, 
#                         'token_type': user_token.token_type
#                     }
#                     )
#     return user_info


# async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)],):
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, 
        expires_delta=access_token_expires
    )
    update_user_token(db, uid=user.id, token=access_token)
    return Token(access_token=access_token, token_type='Bearer')


@router.post("/detect/{model}")
async def detect_sign_on_image(model, 
                               file: UploadFile=File(...), 
                               imgsz: int | tuple=640, 
                               conf: float=0.45, 
                               iou: float=0.4, 
                               db: Session = Depends(get_db)):
    
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     login: str = payload.get("sub")
    #     if login is None:
    #         raise credentials_exception
    #     token_data = TokenData(login=login)
    # except JWTError:
    #     raise credentials_exception
    # user = get_user_by_login(db, token_data.login)
    # if user is None:
    #     raise credentials_exception
    print(file)
    content = await file.read()
    return detect(model, image=content, params={"imgsz": imgsz, "conf": conf, "iou": iou})


# @router.get("/users/me/items/")
# async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)],):
#     return [{"item_id": "Foo", "owner": current_user.login}]