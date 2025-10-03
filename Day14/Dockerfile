FROM python:3.11-slim

# Create a non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser

# Copy only requirements for a small image
COPY Day14/requirements.txt ./
RUN pip install --no-cache-dir -r Day14/requirements.txt

# Copy app
COPY . /home/appuser
RUN chown -R appuser:appuser /home/appuser
USER appuser

ENV PYTHONUNBUFFERED=1

EXPOSE 5000
CMD ["uvicorn", "src.day4:app", "--host", "0.0.0.0", "--port", "5000"]
