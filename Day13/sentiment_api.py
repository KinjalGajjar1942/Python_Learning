from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI(title="Sentiment Analysis API")

# Enable CORS (allow frontend access)
origins = ["*"]  # Allow all origins, or specify your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load sentiment analysis pipeline
sentiment_model = pipeline("sentiment-analysis")

# Request model
class TextRequest(BaseModel):
    text: str

# API route
@app.post("/predict")
async def predict_sentiment(request: TextRequest):
    """
    Takes text as input and returns sentiment prediction.
    """
    result = sentiment_model(request.text)
    return {"input": request.text, "prediction": result}
