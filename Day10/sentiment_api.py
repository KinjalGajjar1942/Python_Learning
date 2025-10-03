from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# 1️⃣ Define request schema
class TextRequest(BaseModel):
    text: str

# 2️⃣ Initialize FastAPI app
app = FastAPI(title="Sentiment Analysis API")

# 3️⃣ Load Hugging Face pipeline (runs once on startup)
sentiment_pipeline = pipeline("sentiment-analysis")

# 4️⃣ Define POST endpoint
@app.post("/analyze")
def analyze_sentiment(request: TextRequest):
    """
    Accepts JSON with 'text', returns sentiment label + score
    Example input:
    { "text": "I love this product!" }
    """
    result = sentiment_pipeline(request.text)[0]  # returns list of dicts
    return {
        "label": result["label"],
        "score": float(result["score"])
    }

# 5️⃣ Root endpoint (optional)
@app.get("/")
def read_root():
    return {"message": "Sentiment Analysis API is running!"}
