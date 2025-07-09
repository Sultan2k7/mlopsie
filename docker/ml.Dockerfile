FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy only requirements first for caching
COPY ml_service/requirements.txt .

# Install dependencies with uv
RUN uv pip install -r requirements.txt

# Copy the rest of your code
COPY ml_service .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
