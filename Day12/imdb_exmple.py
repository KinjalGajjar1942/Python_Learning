import random
from datasets import load_dataset
from transformers import pipeline

# 1. Load IMDB dataset
dataset = load_dataset("imdb")

# 2. Convert test split to a list
test_list = list(dataset["test"])

# 3. Sample 5 random reviews
sample_reviews = random.sample(test_list, 5)

# 4. Initialize sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# 5. Run sentiment analysis and print results
for i, review in enumerate(sample_reviews, 1):
    text = review["text"]
    result = sentiment_pipeline(text[:512])[0]  # truncate long text
    print(f"\nReview {i}:")
    print(f"Text: {text[:200]}...")  # first 200 chars
    print(f"Predicted Sentiment: {result['label']} (score: {result['score']:.4f})")
