from datetime import timedelta
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, uid: int):
    return db.query(models.User).filter(models.User.id == uid).first()


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


def get_uid_by_token(db: Session, token: str):
    return db.query(models.Token).filter(models.Token.token == token).first()


def get_user_token(db: Session, uid: int):
    return db.query(models.Token).filter(models.Token.uid == uid).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = get_password_hash(user.password)
    try:
        db_user = models.User(login=user.login, password=fake_hashed_password, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        return {"result": False, "message": e}
    try:
        create_user_token(db, db_user)
    except Exception as e:
        return {"result": False, "message": e}
    return {"result": True, "message":"New user created in database"}


def create_user_token(db: Session, user: models.User):
    if user is None:
        return False
    db_token = models.Token(uid=user.id, access_token="", token_type='bearer')
    try:
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
    except Exception as e:
        return {"result": False, "message": e}
    return {"result": True, "message": "User's token created"}


def update_user_token(db: Session, uid: int, token: str):
    db_token = db.query(models.Token).filter(models.Token.uid == uid)
    if not db_token.first():
        return False
    db_token.update({'access_token': token})
    db.commit()
    return {"result": True, "message": "User's token updated"}
    

# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item