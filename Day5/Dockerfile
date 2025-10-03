
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the API file
COPY user_api.py ./

EXPOSE 5000
CMD ["uvicorn", "user_api:app", "--host", "0.0.0.0", "--port", "5000"]
