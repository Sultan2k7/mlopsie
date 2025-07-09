from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel
from extractor import analyze_sentiment

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

class AnalyzeRequest(BaseModel):
    content: str

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    return analyze_sentiment(req.content) 