FROM python:3.12-slim

WORKDIR /app

# Copy only requirements first for caching
COPY ml_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY ml_service .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
