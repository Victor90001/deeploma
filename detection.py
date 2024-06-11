from ultralytics import YOLO
from PIL import Image
import requests
import io

# Метод распознавания изображения с собственной моделью распознавания
def sign_detect(image, imgsz, conf, iou):
    # инициализация модели
    sign_detection_model = YOLO('./models/best2.pt')
    # предсказание моделью на изображении и получение данных граничащих рамок
    boxes = sign_detection_model.predict(image, imgsz=imgsz, conf=conf, iou=iou)[0].cpu().boxes.numpy()
    results = {}
    # возврат данных граничащих рамок: определённый класс, вероятность и кординаты границ рамок
    for i, box in enumerate(boxes):
        xyxy = box.xyxy[0].astype(float)
        results[i] = {"cls": float(box.cls[0]),
                      "conf": float(box.conf[0]),
                      "x1": xyxy[0],
                      "y1": xyxy[1],
                      "x2": xyxy[2],
                      "y2": xyxy[3]}
    return {"data": results}

# Метод распознавания изображения по средствам облачного сервиса Ultralytics Hub
def cloud_detect(image, imgsz, conf, iou):
    # адресс модели
    url = "https://api.ultralytics.com/v1/predict/dfnC1dymmmWk0mly8iFT"
    headers = {"x-api-key": "4c44c7d013d8ea2e45313d65b9c5fb05acc1cc2044"}
    # параметры распознавания
    try:
        data = {"size": imgsz[0]}
    except:
        data = {"size": imgsz}
    data["confidence"] = conf
    data["iou"] = iou
    # ответ
    response = requests.post(url, headers=headers, data=data, files={"image": image})
    return response.json()


def detect(model, image, params):
    img = image
    imgStr = io.BytesIO(image)
    image = Image.open(imgStr)
    if model == '0':
        return sign_detect(image=image, imgsz=params['imgsz'], conf=params['conf'], iou=params['iou'])
    elif model == '1':
        return cloud_detect(image=img, imgsz=params['imgsz'], conf=params['conf'], iou=params['iou'])
    else: return {"error": Exception("You chose wrong model!")}