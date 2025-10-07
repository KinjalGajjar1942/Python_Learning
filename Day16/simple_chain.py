"""
Simple LangChain: Text → Summarize → Keywords
"""
from langchain.prompts import PromptTemplate
from langchain_community.llms import FakeListLLM

# Mock responses
summaries = [
    "AI helps doctors diagnose diseases better using machine learning.",
    "Climate change causes extreme weather and harms ecosystems.", 
    "Good software needs quality code and team collaboration."
]

keywords = [
    "AI, healthcare, machine learning, diagnosis",
    "climate change, extreme weather, ecosystems",
    "software, code quality, collaboration"
]

# Create LLMs
summarizer = FakeListLLM(responses=summaries)
extractor = FakeListLLM(responses=keywords)

# Create prompts
summary_prompt = PromptTemplate.from_template("Summarize: {text}")
keyword_prompt = PromptTemplate.from_template("Keywords from: {summary}")

# Process function
def process_text(text):
    summary = (summary_prompt | summarizer).invoke({"text": text})
    keywords = (keyword_prompt | extractor).invoke({"summary": summary})
    return {"summary": summary, "keywords": keywords}

# Test
text = "Artificial intelligence revolutionizes healthcare with machine learning algorithms for better medical diagnosis."
result = process_text(text)

print("📝 Text:", text)
print("📋 Summary:", result["summary"])
print("🏷️ Keywords:", result["keywords"])