"""
Embeddings & Vector Stores with FAISS
Day 18 - Python Learning

Features:
- Create sentence embeddings
- Store text files in FAISS vector database
- Similarity search functionality
- Query: "Which file talks about AI?"
"""

import os
import numpy as np
from typing import List, Tuple, Dict
import pickle

# Try to import required libraries
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("FAISS not available. Install with: pip install faiss-cpu")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Sentence Transformers not available. Install with: pip install sentence-transformers")

class SimpleEmbeddings:
    """Simple embedding class using basic word counting as fallback."""
    
    def __init__(self):
        self.vocab = {}
        self.dimension = 100
    
    def create_simple_embedding(self, text: str) -> np.ndarray:
        """Create a simple embedding using word frequency."""
        words = text.lower().split()
        embedding = np.zeros(self.dimension)
        
        # Simple hash-based embedding
        for word in words:
            hash_value = hash(word) % self.dimension
            embedding[hash_value] += 1
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
            
        return embedding.astype(np.float32)

class VectorStore:
    """Vector store using FAISS for similarity search."""
    
    def __init__(self, use_sentence_transformers: bool = True):
        self.use_sentence_transformers = use_sentence_transformers and SENTENCE_TRANSFORMERS_AVAILABLE
        self.dimension = 384 if self.use_sentence_transformers else 100
        
        # Initialize embedding model
        if self.use_sentence_transformers:
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self.dimension = self.model.get_sentence_embedding_dimension()
            except Exception as e:
                print(f"Error loading sentence transformer: {e}")
                self.use_sentence_transformers = False
                self.model = SimpleEmbeddings()
                self.dimension = 100
        else:
            self.model = SimpleEmbeddings()
        
        # Initialize FAISS index
        if FAISS_AVAILABLE:
            self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        else:
            self.index = None
            self.embeddings = []
        
        self.documents = []
        self.metadata = []
    
    def encode_text(self, text: str) -> np.ndarray:
        """Encode text to embedding vector."""
        if self.use_sentence_transformers:
            embedding = self.model.encode(text)
            # Normalize for cosine similarity
            embedding = embedding / np.linalg.norm(embedding)
            return embedding.astype(np.float32)
        else:
            return self.model.create_simple_embedding(text)
    
    def add_document(self, text: str, metadata: Dict = None):
        """Add a document to the vector store."""
        if metadata is None:
            metadata = {}
        
        # Create embedding
        embedding = self.encode_text(text)
        
        # Add to index
        if FAISS_AVAILABLE:
            self.index.add(embedding.reshape(1, -1))
        else:
            self.embeddings.append(embedding)
        
        # Store document and metadata
        self.documents.append(text)
        self.metadata.append(metadata)
    
    def search(self, query: str, k: int = 3) -> List[Tuple[str, float, Dict]]:
        """Search for similar documents."""
        query_embedding = self.encode_text(query)
        
        if FAISS_AVAILABLE:
            # Search using FAISS
            scores, indices = self.index.search(query_embedding.reshape(1, -1), k)
            
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx != -1:  # Valid result
                    results.append((
                        self.documents[idx],
                        float(score),
                        self.metadata[idx]
                    ))
            return results
        else:
            # Fallback similarity search
            similarities = []
            for i, doc_embedding in enumerate(self.embeddings):
                similarity = np.dot(query_embedding, doc_embedding)
                similarities.append((similarity, i))
            
            # Sort by similarity
            similarities.sort(reverse=True)
            
            results = []
            for similarity, idx in similarities[:k]:
                results.append((
                    self.documents[idx],
                    float(similarity),
                    self.metadata[idx]
                ))
            
            return results
    
    def save(self, filepath: str):
        """Save the vector store."""
        data = {
            'documents': self.documents,
            'metadata': self.metadata,
            'dimension': self.dimension,
            'use_sentence_transformers': self.use_sentence_transformers
        }
        
        if FAISS_AVAILABLE:
            # Save FAISS index
            faiss.write_index(self.index, f"{filepath}.faiss")
        else:
            # Save embeddings
            data['embeddings'] = self.embeddings
        
        # Save metadata
        with open(f"{filepath}.pkl", 'wb') as f:
            pickle.dump(data, f)
    
    def load(self, filepath: str):
        """Load the vector store."""
        # Load metadata
        with open(f"{filepath}.pkl", 'rb') as f:
            data = pickle.load(f)
        
        self.documents = data['documents']
        self.metadata = data['metadata']
        self.dimension = data['dimension']
        
        if FAISS_AVAILABLE and os.path.exists(f"{filepath}.faiss"):
            # Load FAISS index
            self.index = faiss.read_index(f"{filepath}.faiss")
        else:
            # Load embeddings
            self.embeddings = data.get('embeddings', [])

def create_sample_text_files():
    """Create 10 sample text files for testing."""
    
    sample_texts = [
        {
            "filename": "ai_introduction.txt",
            "content": "Artificial Intelligence (AI) is the simulation of human intelligence in machines. AI systems can learn, reason, and make decisions. Machine learning and deep learning are key components of modern AI."
        },
        {
            "filename": "machine_learning.txt", 
            "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data. Popular techniques include supervised learning, unsupervised learning, and reinforcement learning."
        },
        {
            "filename": "cooking_recipe.txt",
            "content": "This delicious pasta recipe requires tomatoes, garlic, olive oil, and basil. Cook the pasta al dente, sauté garlic in olive oil, add tomatoes and basil. Serve hot with parmesan cheese."
        },
        {
            "filename": "sports_news.txt",
            "content": "The football championship will take place next weekend. Teams have been training intensively for months. Fans are excited to see their favorite players compete for the trophy."
        },
        {
            "filename": "deep_learning.txt",
            "content": "Deep learning uses artificial neural networks with multiple layers to model complex patterns. Convolutional neural networks excel at image recognition while recurrent networks handle sequential data."
        },
        {
            "filename": "travel_guide.txt",
            "content": "Paris is known for the Eiffel Tower, Louvre Museum, and delicious croissants. The best time to visit is spring or fall. Don't forget to try authentic French cuisine and visit the charming neighborhoods."
        },
        {
            "filename": "python_programming.txt",
            "content": "Python is a versatile programming language used for web development, data science, and automation. Its simple syntax makes it beginner-friendly. Popular libraries include NumPy, Pandas, and TensorFlow."
        },
        {
            "filename": "climate_change.txt",
            "content": "Climate change refers to long-term shifts in global temperatures and weather patterns. Human activities like burning fossil fuels contribute to greenhouse gas emissions. Renewable energy is crucial for mitigation."
        },
        {
            "filename": "neural_networks.txt",
            "content": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes that process information. Artificial neural networks power many AI applications today."
        },
        {
            "filename": "gardening_tips.txt",
            "content": "Successful gardening requires proper soil, adequate watering, and sufficient sunlight. Choose plants suitable for your climate zone. Regular pruning and fertilizing help plants grow healthy and strong."
        }
    ]
    
    # Create directory if it doesn't exist
    os.makedirs("sample_texts", exist_ok=True)
    
    created_files = []
    for item in sample_texts:
        filepath = os.path.join("sample_texts", item["filename"])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(item["content"])
        created_files.append(filepath)
        
    return created_files

def load_text_files(directory: str) -> List[Tuple[str, str]]:
    """Load all text files from directory."""
    files_content = []
    
    if not os.path.exists(directory):
        return files_content
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    files_content.append((filename, content))
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    return files_content

def demo_vector_store():
    """Demonstrate vector store functionality."""
    
    print("=" * 60)
    print("Embeddings & Vector Store Demo with FAISS")
    print("=" * 60)
    
    # Create sample files
    print("\n1. Creating 10 sample text files...")
    created_files = create_sample_text_files()
    print(f"Created {len(created_files)} files in 'sample_texts' directory")
    
    # Initialize vector store
    print("\n2. Initializing Vector Store...")
    vector_store = VectorStore()
    print(f"Using {'Sentence Transformers' if vector_store.use_sentence_transformers else 'Simple embeddings'}")
    print(f"Embedding dimension: {vector_store.dimension}")
    print(f"FAISS available: {FAISS_AVAILABLE}")
    
    # Load and index files
    print("\n3. Loading and indexing files...")
    files_content = load_text_files("sample_texts")
    
    for filename, content in files_content:
        metadata = {"filename": filename, "length": len(content)}
        vector_store.add_document(content, metadata)
        print(f"  ✓ Indexed: {filename}")
    
    print(f"\nTotal documents indexed: {len(vector_store.documents)}")
    
    # Perform searches
    print("\n4. Performing similarity searches...")
    
    queries = [
        "Which file talks about AI?",
        "Tell me about cooking",
        "What discusses neural networks?",
        "Sports and games information"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 40)
        
        results = vector_store.search(query, k=3)
        
        for i, (doc, score, metadata) in enumerate(results, 1):
            filename = metadata.get('filename', 'Unknown')
            print(f"{i}. File: {filename}")
            print(f"   Score: {score:.4f}")
            print(f"   Content: {doc[:100]}...")
            print()
    
    # Save vector store
    print("\n5. Saving vector store...")
    try:
        vector_store.save("my_vector_store")
        print("✓ Vector store saved successfully!")
    except Exception as e:
        print(f"Error saving: {e}")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

if __name__ == "__main__":
    demo_vector_store()
