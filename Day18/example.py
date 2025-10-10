"""
Day 18 - Embeddings & Vector Stores with FAISS
Fixed version with proper imports and sample data
"""

import os
from typing import List, Dict

# Updated imports (no deprecation warnings)
try:
    from langchain_community.document_loaders import TextLoader
    from langchain_core.documents import Document
    from langchain_text_splitters import CharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores.faiss import FAISS
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    print(f"LangChain packages not available: {e}")
    LANGCHAIN_AVAILABLE = False

# ----------------------
# Set your OpenAI API key (if you have one)
# ----------------------
# os.environ["OPENAI_API_KEY"] = "sk-your-actual-key-here"  # Replace with real key

# ----------------------
# 1️⃣ Create and load 10 text files
# ----------------------

def create_sample_files():
    """Create 10 sample text files for testing."""
    
    sample_texts = {
        "file1.txt": "Artificial Intelligence (AI) is revolutionizing technology. Machine learning algorithms enable computers to learn from data without explicit programming. AI applications include natural language processing, computer vision, and robotics.",
        
        "file2.txt": "Python is a versatile programming language used in web development, data science, and automation. Its simple syntax makes it beginner-friendly. Popular frameworks include Django, Flask, and FastAPI.",
        
        "file3.txt": "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data. Supervised learning uses labeled datasets, while unsupervised learning finds patterns in unlabeled data.",
        
        "file4.txt": "Climate change refers to long-term shifts in global weather patterns. Rising temperatures, melting glaciers, and extreme weather events are key indicators. Renewable energy sources are crucial for mitigation.",
        
        "file5.txt": "Deep learning uses artificial neural networks with multiple layers to process complex data. Convolutional Neural Networks (CNNs) excel at image recognition, while Transformers are powerful for natural language tasks.",
        
        "file6.txt": "Web development involves creating websites and web applications. Frontend technologies include HTML, CSS, and JavaScript. Backend development uses languages like Python, Java, and Node.js.",
        
        "file7.txt": "Data science combines statistics, programming, and domain expertise to extract insights from data. Common tools include Python libraries like Pandas, NumPy, and Scikit-learn for analysis and modeling.",
        
        "file8.txt": "Cybersecurity protects computer systems and networks from digital attacks. Common threats include malware, phishing, and ransomware. Security measures include firewalls, encryption, and authentication.",
        
        "file9.txt": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information. Artificial neural networks power many AI applications today.",
        
        "file10.txt": "Cloud computing provides on-demand access to computing resources over the internet. Services include Infrastructure as a Service (IaaS), Platform as a Service (PaaS), and Software as a Service (SaaS)."
    }
    
    # Create files
    for filename, content in sample_texts.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return list(sample_texts.keys())

def load_documents_simple():
    """Load documents without LangChain dependencies."""
    
    file_paths = create_sample_files()
    documents = []
    
    for path in file_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Create a simple document structure
                doc = {
                    'content': content,
                    'metadata': {'source_file': path}
                }
                documents.append(doc)
                print(f"✅ Loaded: {path}")
        except Exception as e:
            print(f"❌ Error loading {path}: {e}")
    
    return documents

def load_documents_langchain():
    """Load documents using LangChain."""
    
    file_paths = create_sample_files()
    documents = []
    
    for path in file_paths:
        try:
            loader = TextLoader(path, encoding="utf-8")
            docs = loader.load()
            # Add filename as metadata
            for doc in docs:
                doc.metadata["source_file"] = path
            documents.extend(docs)
            print(f"✅ Loaded: {path}")
        except Exception as e:
            print(f"❌ Error loading {path}: {e}")
    
    return documents

# Load documents
print("📁 Creating and loading 10 text files...")
if LANGCHAIN_AVAILABLE:
    documents = load_documents_langchain()
else:
    documents = load_documents_simple()

# ----------------------
# 2️⃣ Simple Vector Search (without external APIs)
# ----------------------

class SimpleVectorSearch:
    """Simple similarity search without external dependencies."""
    
    def __init__(self, documents):
        self.documents = documents
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """Search for similar documents using keyword matching."""
        query_words = set(query.lower().split())
        scores = []
        
        for doc in self.documents:
            if LANGCHAIN_AVAILABLE:
                content = doc.page_content.lower()
                source_file = doc.metadata.get("source_file", "Unknown")
            else:
                content = doc['content'].lower()
                source_file = doc['metadata']['source_file']
            
            # Calculate simple similarity score
            doc_words = set(content.split())
            common_words = query_words & doc_words
            score = len(common_words) / len(query_words) if query_words else 0
            
            scores.append({
                'score': score,
                'content': doc['content'] if not LANGCHAIN_AVAILABLE else doc.page_content,
                'source_file': source_file
            })
        
        # Sort by score and return top k
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:k]

# ----------------------
# 3️⃣ Search for AI-related content
# ----------------------

def search_with_langchain():
    """Search using LangChain + FAISS (if API key available)."""
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-or-v1-"):
        print("❌ No valid OpenAI API key found")
        return False
    
    try:
        # Split documents into chunks
        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = []
        for doc in documents:
            chunks = splitter.split_text(doc.page_content)
            for chunk in chunks:
                split_docs.append(Document(page_content=chunk, metadata=doc.metadata))
        
        # Create embeddings and FAISS index
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        faiss_index = FAISS.from_documents(split_docs, embeddings)
        
        # Query FAISS
        query = "Which file talks about AI?"
        results = faiss_index.similarity_search(query, k=3)
        
        print(f"🤖 LangChain + FAISS Results for: '{query}'\n")
        for i, res in enumerate(results):
            source_file = res.metadata.get("source_file", "Unknown")
            print(f"{i+1}. 📄 Source: {source_file}")
            print(f"   📝 Text: {res.page_content[:150]}...\n")
        
        return True
        
    except Exception as e:
        print(f"❌ LangChain error: {e}")
        return False

def search_with_simple_method():
    """Search using simple keyword matching."""
    
    print("🔍 Simple Vector Search Results:\n")
    
    searcher = SimpleVectorSearch(documents)
    query = "Which file talks about AI?"
    results = searcher.search(query, k=3)
    
    print(f"Query: '{query}'\n")
    for i, result in enumerate(results):
        print(f"{i+1}. 📄 Source: {result['source_file']}")
        print(f"   🎯 Score: {result['score']:.3f}")
        print(f"   📝 Text: {result['content'][:150]}...\n")

# ----------------------
# 4️⃣ Run the search
# ----------------------

def main():
    """Main function to run the demo."""
    
    print("🎯 Day 18: Embeddings & Vector Stores Demo")
    print("=" * 50)
    print()
    
    if not documents:
        print("❌ No documents loaded!")
        return
    
    print(f"📊 Loaded {len(documents)} documents successfully!\n")
    
    # Try LangChain + FAISS first
    if LANGCHAIN_AVAILABLE:
        success = search_with_langchain()
        if success:
            print("\n" + "="*50)
            print("✅ LangChain + FAISS search completed!")
            return
    
    # Fallback to simple search
    print("💡 Using simple keyword-based search...")
    search_with_simple_method()
    
    print("="*50)
    print("✅ Demo completed!")
    print("\n💡 Tips:")
    print("   - Add a valid OpenAI API key for advanced embeddings")
    print("   - Install: pip install langchain-openai")
    print("   - Format: OPENAI_API_KEY=sk-...")

if __name__ == "__main__":
    main()
