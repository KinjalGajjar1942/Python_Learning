import time
import json
from transformers import pipeline

# 1️⃣ Sample 50 sentences
sentences = [
    f"This is sentence number {i}. I love testing models!" for i in range(1, 51)
]

# 2️⃣ Initialize pipelines
# DistilBERT (smaller/faster)
distilbert_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# Regular BERT (use base model + fine-tuning)
bert_pipeline = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

# 3️⃣ Helper function to measure time
def measure_inference(pipeline_model, sentences):
    start_time = time.time()
    results = pipeline_model(sentences)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time, results

# 4️⃣ Measure DistilBERT
distil_time, distil_results = measure_inference(distilbert_pipeline, sentences)
print(f"DistilBERT took {distil_time:.2f} seconds for {len(sentences)} sentences.")

# 5️⃣ Measure BERT
bert_time, bert_results = measure_inference(bert_pipeline, sentences)
print(f"BERT took {bert_time:.2f} seconds for {len(sentences)} sentences.")

# 6️⃣ Save results to JSON
log_data = {
    "num_sentences": len(sentences),
    "distilbert_time_sec": distil_time,
    "bert_time_sec": bert_time,
    "distilbert_results": distil_results,
    "bert_results": bert_results
}

with open("benchmark_results.json", "w") as f:
    json.dump(log_data, f, indent=4)

print("Benchmark results saved to 'benchmark_results.json'")
