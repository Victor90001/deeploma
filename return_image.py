from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np


def puttext(x1, y1, x2, y2, img, cls, conf):
  pil_font = ImageFont.truetype("arial.ttf", 14)
  imgOrignal = img.copy()
  # PUTTING TEXT
  imgOrignal = cv2.cvtColor(imgOrignal, cv2.COLOR_BGR2RGB)
  img_pil = Image.fromarray(imgOrignal)
  draw = ImageDraw.Draw(img_pil)
  draw.text((x1, y1-15), f'{cls}', (255, 0, 0), font=pil_font)
  img_ar = np.array(img_pil)
  imgOrignal = cv2.cvtColor(img_ar, cv2.COLOR_RGB2BGR)
  return imgOrignal


def add_bb(image, results):
    for sign in results['data']:
            box = sign['box']
            res_image = puttext(box['x1'],box['y1'],box['x2'], box['y2'], image, sign['name'], sign['confidence'])