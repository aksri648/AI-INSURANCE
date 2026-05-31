# Stage 1: Build frontend
FROM node:20-slim AS frontend-build

WORKDIR /frontend

COPY FRONTEND/package.json FRONTEND/package-lock.json* ./
RUN npm ci

COPY FRONTEND/ .
RUN npm run build

# Stage 2: Backend + serve frontend
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY BACKEND/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY BACKEND/ .

COPY --from=frontend-build /frontend/dist /app/static

RUN mkdir -p uploads logs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
