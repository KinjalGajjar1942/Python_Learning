# sentiment_example.py
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

def run_sentiment_examples():
    # Create a sentiment-analysis pipeline (will download the default model if not cached)
    sentiment = pipeline("sentiment-analysis")  # default: distilbert-base-uncased-finetuned-sst-2-english

    # 3 custom sentences to test
    sentences = [
        "I love the new design of your website! It's clean and easy to use.",
        "This is the worst experience I've ever had with customer service.",
        "The product is okay, but the delivery was late and packaging was damaged."
    ]

    # Pipeline accepts a list (batch) and returns a list of dicts
    results = sentiment(sentences)

    # Print nicely
    for i, (s, r) in enumerate(zip(sentences, results), start=1):
        print(f"--- Example {i} ---")
        print(f"Sentence: {s}")
        print(f"Predicted label: {r['label']}, score: {r['score']:.4f}")
        print()

def show_tokenization_basics():
    print("=== Tokenization basics (example for first sentence) ===")
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    text = "I love the new design of your website! It's clean and easy to use."
    encoded = tokenizer(text, return_tensors="pt")
    print("tokens:", tokenizer.tokenize(text))
    print("input_ids:", encoded["input_ids"].tolist())
    print("attention_mask:", encoded["attention_mask"].tolist())

    # raw logits -> probabilities
    with __import__("torch").no_grad():
        outputs = model(**encoded)
        logits = outputs.logits
        probs = __import__("torch").nn.functional.softmax(logits, dim=-1).numpy().tolist()[0]

    # model.config.id2label maps index to label
    id2label = model.config.id2label
    print("Model probabilities (label -> probability):")
    for idx, p in enumerate(probs):
        label = id2label.get(idx, str(idx))
        print(f"  {label}: {p:.4f}")

if __name__ == "__main__":
    run_sentiment_examples()
    print()
    show_tokenization_basics()
