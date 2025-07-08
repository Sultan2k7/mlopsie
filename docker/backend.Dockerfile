FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install alembic

COPY backend .

CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000
