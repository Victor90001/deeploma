from ultralytics import YOLO
from PIL import Image
import requests
import io


def sign_detect(image):
    sign_detection_model = YOLO('./models/best2.pt')
    boxes = sign_detection_model.predict(image)[0].cpu().boxes.numpy()
    results = {}
    for i, box in enumerate(boxes):
        xyxy = box.xyxy[0].astype(float)
        results[i] = {"cls": float(box.cls[0]),
                      "conf": float(box.conf[0]),
                      "x1": xyxy[0],
                      "y1": xyxy[1],
                      "x2": xyxy[2],
                      "y2": xyxy[3]}
    return {"data": results}


def cloud_detect(image):
    # Run inference on an image
    url = "https://api.ultralytics.com/v1/predict/dfnC1dymmmWk0mly8iFT"
    headers = {"x-api-key": "4c44c7d013d8ea2e45313d65b9c5fb05acc1cc2044"}
    data = {"size": 640, "confidence": 0.25, "iou": 0.45}
    response = requests.post(url, headers=headers, data=data, files={"image": image})

    # Check for successful response
    response.raise_for_status()

    # Print inference results
    return response.json()


def detect(model, image):
    # return {'image': image}
    imgStr = io.BytesIO(image)
    image = Image.open(imgStr)
    if model == '0':
        return sign_detect(image=image)
    elif model == '1':
        return cloud_detect(image=image)
    else: return {"error": Exception("You chose wrong model!")}