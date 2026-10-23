FROM python:3.12-slim

WORKDIR /app

# install deps first so the layer is cached when only the code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["python", "-m", "app.main", "/data/config.xml"]