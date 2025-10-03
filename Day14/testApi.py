from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI(title="Text Analysis API")

# Enable CORS for frontend
origins = ["*"]  # Replace "*" with your frontend URL in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load NLP pipelines
sentiment_model = pipeline("sentiment-analysis")
summarizer_model = pipeline("summarization")

# Request model
class TextRequest(BaseModel):
    text: str

# 1️⃣ Sentiment API
@app.post("/sentiment")
async def sentiment(request: TextRequest):
    """
    Returns sentiment (POSITIVE/NEGATIVE) for given text.
    """
    result = sentiment_model(request.text)
    return {"input": request.text, "sentiment": result}

# 2️⃣ Summary API
@app.post("/summary")
async def summarize(request: TextRequest):
    """
    Returns a short 2-line summary of the given text.
    """
    result = summarizer_model(request.text, max_length=50, min_length=25, do_sample=False)
    return {"input": request.text, "summary": result[0]['summary_text']}
