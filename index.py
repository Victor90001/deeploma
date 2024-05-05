from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.wsgi import WSGIMiddleware
from flask_app import flask_app
from detection import detect


app = FastAPI()


@app.post("/detect/{model}")
async def read_main(model, file: UploadFile=File(...)):
    content = await file.read()
    # contents = await file.read()
    # nparr = np.fromstring(contents, np.uint8)
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return detect(model, image=content)


app.mount("/", WSGIMiddleware(flask_app))