# MLOpsie: Social Media API with Sentiment Analysis

## 🚀 Project Overview
A modern FastAPI-based social media backend with:
- User and post management
- Likes and comments
- Sentiment analysis (DistilBERT)
- Monitoring (Prometheus + Grafana)
- Full Dockerization
- CI/CD with GitHub Actions

## 🛠️ Tech Stack
- **Backend:** FastAPI, SQLAlchemy, Alembic
- **ML Service:** FastAPI, HuggingFace Transformers (DistilBERT)
- **Database:** PostgreSQL
- **Monitoring:** Prometheus, Grafana
- **CI/CD:** GitHub Actions
- **Containerization:** Docker, Docker Compose

## 📦 Features
- User CRUD
- Post CRUD (with sentiment analysis)
- Likes & Comments (add, edit, delete, list)
- Prometheus metrics for backend & ML service
- Grafana dashboards
- Automated tests & linting in CI/CD

## ⚡ Quickstart (Docker Compose)
1. **Clone the repo:**
   ```sh
   git clone <your-repo-url>
   cd mlopsie
   ```
2. **Build and start all services:**
   ```sh
   docker compose build
   docker compose up -d
   ```
3. **Access services:**
   - **Backend API:** http://localhost:8000
   - **ML Service:** http://localhost:5000
   - **Prometheus:** http://localhost:9090
   - **Grafana:** http://localhost:3000 (default: admin/admin)

## 🧑‍💻 Local Development (Backend)
```sh
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

## 🧠 ML Microservice (Sentiment Analysis)
- Uses `distilbert-base-uncased-finetuned-sst-2-english` for sentiment.
- **Endpoint:** `POST /analyze`
  - **Request:** `{ "content": "I love this!" }`
  - **Response:** `{ "sentiment": "POSITIVE" }`

## 🌐 API Usage Examples
- **Create User:**
  ```http
  POST /users/
  { "username": "alice", "email": "alice@example.com", "password": "pass" }
  ```
- **Create Post (sentiment auto-assigned):**
  ```http
  POST /posts/?user_id=1
  { "title": "Hello", "content": "I love this!" }
  // Response: { ..., "tone": "POSITIVE" }
  ```
- **Like a Post:**
  ```http
  POST /posts/1/like?user_id=1
  ```
- **Add Comment:**
  ```http
  POST /posts/1/comments?user_id=1
  { "content": "Great post!" }
  ```

## 📊 Monitoring
- **Prometheus** scrapes `/metrics` from backend and ML service.
- **Grafana** dashboards visualize post creation, ML requests, etc.
- Access at [http://localhost:3000](http://localhost:3000) (admin/admin).

## 🔄 CI/CD
- **GitHub Actions** runs on every push/PR:
  - Builds Docker images
  - Runs backend & ML service tests inside containers
  - Lints code

---
**Made with MLOps and modern backend engineering!**
