# import json
# import requests
# import time
# start = time.time()
# # Run inference on an image
# url = "https://api.ultralytics.com/v1/predict/dfnC1dymmmWk0mly8iFT"
# headers = {"x-api-key": "4c44c7d013d8ea2e45313d65b9c5fb05acc1cc2044"}
# data = {"size": 640, "confidence": 0.25, "iou": 0.45}
# with open("C:\\Users\\кирюха\\Desktop\\fff1.png", "rb") as f:
# 	response = requests.post(url, headers=headers, data=data, files={"image": f})

# # Check for successful response
# response.raise_for_status()
# print(json.dumps(response.json(), indent=2))
# print(time.time() - start)
# ----------------------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------------------
# 
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.staticfiles import StaticFiles
from oauth2.security import router, authenticate_user
from detection import detect
from db import connect
from sqlalchemy.orm import Session
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import Request
from fastapi.templating import Jinja2Templates
import time

connect.Base.metadata.create_all(bind=connect.engine)
# app = FastAPI(
#     docs_url=None,
#     redoc_url=None
# )
app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory='templates')
# app.include_router(router=router)


def get_db():
    db = connect.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/", include_in_schema=False)
# async def get_swagger_documentation(request: Request):
#     response = None
#     db_cookie = request.cookies.get('db_session')
#     if db_cookie is not None:
#         response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
#     else:
#         response = templates.TemplateResponse("api_login.html", {"request": request})
#     return response


@app.post("/login", include_in_schema=False)
async def login_swagger(request: Request, db: Session = Depends(get_db)):
    form = await request.json()
    if authenticate_user(db, form['username'], form['password']):
        return True
    return False


@app.post("/detect/{model}")
async def read_main(model, file: UploadFile=File(...), imgsz: int | tuple=640, conf: float=0.45, iou: float=0.4):
    t = time.time()
    content = await file.read()
    d = detect(model, image=content, params={"imgsz": imgsz, "conf": conf, "iou": iou})
    print(time.time() - t)
    return d


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
# app.mount("/", WSGIMiddleware(flask_app))