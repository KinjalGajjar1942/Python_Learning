# 🚀 Free Deployment Guide for FastAPI Text Analysis API

## Overview
This guide covers multiple free platforms to deploy your FastAPI application with sentiment analysis and summarization capabilities.

## 📋 Prerequisites
- Your FastAPI application (`testApi.py`)
- GitHub account
- Basic understanding of Git

---

## 🎯 **Option 1: Railway (Recommended for FastAPI)**

### Why Railway?
- ✅ Free tier: 500 hours/month
- ✅ Automatic deployments from GitHub
- ✅ Built-in domain and HTTPS
- ✅ Easy environment variables
- ✅ Supports Python/FastAPI perfectly

### Step-by-Step Deployment:

#### 1. Prepare Your Application
```bash
# Create requirements.txt
pip freeze > requirements.txt
```

#### 2. Create Railway Configuration
Create `railway.toml`:
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn testApi:app --host 0.0.0.0 --port $PORT"
```

#### 3. Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python and deploy!

#### 4. Environment Variables (if needed)
- Add any secrets in Railway dashboard
- Set `PORT` environment variable (Railway handles this automatically)

---

## 🎯 **Option 2: Render**

### Why Render?
- ✅ 750 hours free per month
- ✅ Auto-deploys from Git
- ✅ Built-in SSL certificates
- ✅ Easy to use

### Step-by-Step:

#### 1. Create `render.yaml`
```yaml
services:
  - type: web
    name: text-analysis-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn testApi:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

#### 2. Deploy
1. Go to [render.com](https://render.com)
2. Connect GitHub account
3. Create new "Web Service"
4. Select your repository
5. Configure build and start commands

---

## 🎯 **Option 3: Heroku (Classic)**

### Step-by-Step:

#### 1. Create `Procfile`
```
web: uvicorn testApi:app --host 0.0.0.0 --port $PORT
```

#### 2. Create `runtime.txt`
```
python-3.11.7
```

#### 3. Deploy via Git
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-text-analysis-api

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

---

## 🎯 **Option 4: Vercel (Serverless)**

### Step-by-Step:

#### 1. Create `vercel.json`
```json
{
  "builds": [
    {
      "src": "testApi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "testApi.py"
    }
  ]
}
```

#### 2. Modify your FastAPI app for Vercel
Create `api/index.py`:
```python
from testApi import app

# Vercel expects the app to be available at the module level
handler = app
```

---

## 🎯 **Option 5: Google Cloud Run (Free Tier)**

### Step-by-Step:

#### 1. Create `Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "testApi:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### 2. Deploy with gcloud CLI
```bash
gcloud run deploy text-analysis-api --source . --platform managed --region us-central1
```

---

## 📂 **Required Files for All Deployments**

### 1. `requirements.txt` (Essential)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
transformers==4.35.2
torch==2.1.0
pydantic==2.5.0
```

### 2. `.gitignore`
```
__pycache__/
*.pyc
.env
.venv/
venv/
.DS_Store
*.log
```

### 3. Update your `testApi.py` for production:
```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Get port from environment variable (important for deployment)
PORT = int(os.environ.get("PORT", 8000))

app = FastAPI(
    title="Text Analysis API",
    description="AI-powered sentiment analysis and text summarization",
    version="2.0.0"
)

# Production-ready CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your existing code here...
```

---

## 🚀 **Quick Start: Deploy to Railway (Easiest)**

### Complete Setup Commands:
```bash
# 1. Navigate to your project
cd /Users/mohitrajpurohit/Kinjal/python/Python_Learning/Day14

# 2. Create requirements.txt
echo "fastapi==0.104.1
uvicorn[standard]==0.24.0
transformers==4.35.2
torch==2.1.0
pydantic==2.5.0" > requirements.txt

# 3. Create railway.toml
echo '[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn testApi:app --host 0.0.0.0 --port $PORT"' > railway.toml

# 4. Initialize git (if not already done)
git init
git add .
git commit -m "Prepare for Railway deployment"

# 5. Push to GitHub
# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/text-analysis-api.git
git branch -M main
git push -u origin main

# 6. Deploy on Railway
# Go to railway.app → Deploy from GitHub → Select repo → Deploy!
```

---

## 🔧 **Production Optimizations**

### 1. Reduce Model Loading Time
```python
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def load_models():
    """Load models once and cache them"""
    sentiment_model = pipeline("sentiment-analysis")
    summarizer_model = pipeline("summarization")
    return sentiment_model, summarizer_model

# Use in your endpoints
sentiment_model, summarizer_model = load_models()
```

### 2. Health Check Endpoint
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

### 3. Environment-based Configuration
```python
import os

class Settings:
    environment = os.getenv("ENVIRONMENT", "development")
    debug = environment == "development"
    cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")

settings = Settings()
```

---

## 🎯 **Recommended: Railway Deployment**

Railway is the easiest and most reliable for FastAPI apps. Here's why:

✅ **Pros:**
- Automatic HTTPS
- Custom domains
- Easy GitHub integration
- Great Python support
- Generous free tier

❌ **Limitations:**
- 500 hours/month limit
- Cold starts after inactivity

---

## 📱 **Testing Your Deployment**

Once deployed, test your API:

```bash
# Replace YOUR_RAILWAY_URL with your actual URL
curl -X POST "https://YOUR_RAILWAY_URL.railway.app/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this deployment guide!"}'
```

---

## 🔗 **Useful Links**

- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)

---

## 💡 **Pro Tips**

1. **Use Railway for simplicity**
2. **Always test locally first**
3. **Monitor your usage on free tiers**
4. **Set up GitHub Actions for CI/CD**
5. **Use environment variables for secrets**