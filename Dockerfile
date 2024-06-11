FROM python:3.10-slim-bookworm as base

RUN apt update \
    && apt install --no-install-recommends -y libgl1 libglib2.0-0

WORKDIR /app

RUN pip3 install --no-cache torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && pip3 install ultralytics

FROM base

COPY requirements.txt requirements.txt

RUN pip install --no-cache -r requirements.txt

COPY . .

CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000