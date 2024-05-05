FROM python:3.10.12-slim

WORKDIR /api

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8000"]