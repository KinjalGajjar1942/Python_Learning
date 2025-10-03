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

# Root endpoint - API Information
@app.get("/")
async def root():
    """
    API Information and available endpoints
    """
    return {
        "message": "🤖 Text Analysis API - Powered by AI",
        "version": "2.0.0",
        "description": "Advanced text analysis with sentiment and summarization",
        "endpoints": {
            "sentiment": {
                "method": "POST",
                "url": "/sentiment",
                "description": "Analyze text sentiment (POSITIVE/NEGATIVE)",
                "example": {"text": "I love this product!"}
            },
            "summary": {
                "method": "POST", 
                "url": "/summary",
                "description": "Generate text summary",
                "example": {"text": "Long text to be summarized..."}
            },
            "analyze": {
                "method": "POST",
                "url": "/analyze", 
                "description": "🆕 Combined sentiment + summary analysis",
                "example": {"text": "Your text for comprehensive analysis"}
            }
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }

# 1️Sentiment API
@app.post("/sentiment")
async def sentiment(request: TextRequest):
    """
    Returns sentiment (POSITIVE/NEGATIVE) for given text.
    """
    result = sentiment_model(request.text)
    return {"input": request.text, "sentiment": result}

# 2️ Summary API
@app.post("/summary")
async def summarize(request: TextRequest):
    """
    Returns a short 2-line summary of the given text.
    """
    result = summarizer_model(request.text, max_length=50, min_length=25, do_sample=False)
    return {"input": request.text, "summary": result[0]['summary_text']}

# 3️ Combined Analysis API (NEW)
@app.post("/analyze")
async def analyze_text(request: TextRequest):
    """
    Returns both sentiment analysis and summary for given text.
    Combines both AI models for comprehensive text analysis.
    """
    # Get sentiment analysis
    sentiment_result = sentiment_model(request.text)
    
    # Get text summary (only if text is long enough)
    summary_result = None
    word_count = len(request.text.split())
    
    if word_count >= 20:  # Only summarize if text has 20+ words
        summary_result = summarizer_model(
            request.text, 
            max_length=50, 
            min_length=25, 
            do_sample=False
        )
        summary_text = summary_result[0]['summary_text']
    else:
        summary_text = "Text too short for summarization"
    
    # Combine results
    return {
        "input": request.text,
        "word_count": word_count,
        "sentiment": {
            "label": sentiment_result[0]["label"],
            "score": round(sentiment_result[0]["score"], 4),
            "confidence": f"{sentiment_result[0]['score']:.1%}"
        },
        "summary": {
            "text": summary_text,
            "original_length": len(request.text),
            "summary_length": len(summary_text) if summary_text != "Text too short for summarization" else 0
        },
        "analysis": {
            "is_positive": sentiment_result[0]["label"] == "POSITIVE",
            "confidence_level": "High" if sentiment_result[0]["score"] > 0.8 else "Medium" if sentiment_result[0]["score"] > 0.6 else "Low",
            "recommended_action": get_recommendation(sentiment_result[0]["label"], sentiment_result[0]["score"])
        }
    }

def get_recommendation(label: str, score: float) -> str:
    """Get recommendation based on sentiment analysis"""
    if label == "POSITIVE":
        if score > 0.9:
            return "Excellent feedback - share this testimonial!"
        elif score > 0.7:
            return "Positive response - good to highlight"
        else:
            return "Somewhat positive - monitor for improvements"
    else:  # NEGATIVE
        if score > 0.9:
            return "Strong negative feedback - immediate attention needed"
        elif score > 0.7:
            return "Negative response - investigate and address concerns"
        else:
            return "Slightly negative - consider follow-up"
