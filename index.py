from fastapi import FastAPI, UploadFile, File, Depends, Request
from typing import Annotated
from sqlalchemy.orm import Session
from oauth2.security import router, authenticate_user
from detection import detect
from db import connect
from db.crud import create_user
from db.schemas import UserCreate, UserBase
from fastapi.openapi.docs import get_swagger_ui_html


connect.Base.metadata.create_all(bind=connect.engine)


app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(router=router)


def get_db():
    db = connect.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", include_in_schema=False)
async def get_swagger_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Sign detector - API")


@app.post("/login", include_in_schema=False)
async def signin(user: UserBase, db: Session = Depends(get_db)):
    if authenticate_user(db, login=user.login, password=user.password):
        return {"result": True, "message": "Successfully logged in"}
    return {"result": False, "message": "Authentication failed! Wrong login or password"}


@app.post("/signup", include_in_schema=False)
async def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user=user)


# @app.post("/detect/{model}")
# async def read_main(model, file: UploadFile=File(...), imgsz: int | tuple=640, conf: float=0.45, iou: float=0.4):
#     content = await file.read()
#     return detect(model, image=content, params={"imgsz": imgsz, "conf": conf, "iou": iou})

# @app.post("/detect/{model}")
# async def read_main(model, file: UploadFile=File(...), imgsz: int | tuple=640, conf: float=0.45, iou: float=0.4):
#     content = await file.read()
#     return detect(model, image=content)


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
# app.mount("/", WSGIMiddleware(flask_app))