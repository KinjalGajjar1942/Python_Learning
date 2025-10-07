"""
Simple Embeddings & Vector Store
Day 18 - Python Learning

A minimal implementation without external dependencies.
"""

import os
import math
from typing import List, Tuple, Dict
import json

class SimpleVectorStore:
    """Simple vector store using basic text similarity."""
    
    def __init__(self):
        self.documents = []
        self.metadata = []
        self.word_vectors = {}
    
    def create_word_vector(self, text: str) -> Dict[str, float]:
        """Create simple word frequency vector."""
        words = text.lower().split()
        vector = {}
        
        # Count word frequencies
        for word in words:
            # Clean word
            word = ''.join(c for c in word if c.isalnum())
            if word and len(word) > 2:  # Skip very short words
                vector[word] = vector.get(word, 0) + 1
        
        # Normalize by document length
        total_words = sum(vector.values())
        if total_words > 0:
            for word in vector:
                vector[word] = vector[word] / total_words
        
        return vector
    
    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two vectors."""
        # Get common words
        common_words = set(vec1.keys()) & set(vec2.keys())
        
        if not common_words:
            return 0.0
        
        # Calculate dot product
        dot_product = sum(vec1[word] * vec2[word] for word in common_words)
        
        # Calculate magnitudes
        mag1 = math.sqrt(sum(val**2 for val in vec1.values()))
        mag2 = math.sqrt(sum(val**2 for val in vec2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    def add_document(self, text: str, metadata: Dict = None):
        """Add document to the store."""
        if metadata is None:
            metadata = {}
        
        # Create vector representation
        vector = self.create_word_vector(text)
        
        # Store document, metadata, and vector
        self.documents.append(text)
        self.metadata.append(metadata)
        self.word_vectors[len(self.documents) - 1] = vector
    
    def search(self, query: str, k: int = 3) -> List[Tuple[str, float, Dict]]:
        """Search for similar documents."""
        query_vector = self.create_word_vector(query)
        
        similarities = []
        
        for idx in range(len(self.documents)):
            doc_vector = self.word_vectors[idx]
            similarity = self.cosine_similarity(query_vector, doc_vector)
            similarities.append((similarity, idx))
        
        # Sort by similarity (descending)
        similarities.sort(reverse=True)
        
        # Return top k results
        results = []
        for similarity, idx in similarities[:k]:
            results.append((
                self.documents[idx],
                similarity,
                self.metadata[idx]
            ))
        
        return results
    
    def save(self, filename: str):
        """Save vector store to file."""
        data = {
            'documents': self.documents,
            'metadata': self.metadata,
            'word_vectors': self.word_vectors
        }
        
        with open(f"{filename}.json", 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self, filename: str):
        """Load vector store from file."""
        with open(f"{filename}.json", 'r') as f:
            data = json.load(f)
        
        self.documents = data['documents']
        self.metadata = data['metadata']
        self.word_vectors = {int(k): v for k, v in data['word_vectors'].items()}

def create_sample_files():
    """Create 10 sample text files."""
    
    texts = {
        "ai_basics.txt": "Artificial Intelligence (AI) is computer science focused on creating intelligent machines. AI systems can learn, reason, and solve problems like humans. Machine learning and neural networks are key AI technologies.",
        
        "machine_learning.txt": "Machine learning is a branch of artificial intelligence that uses algorithms to learn from data. Supervised learning uses labeled data, while unsupervised learning finds patterns in unlabeled data.",
        
        "cooking_pasta.txt": "Making perfect pasta requires boiling salted water, cooking pasta al dente, and preparing a good sauce. Fresh ingredients like tomatoes, basil, and garlic make the best flavors.",
        
        "football_game.txt": "Football is a popular sport played by two teams of eleven players. The objective is to score goals by getting the ball into the opponent's goal. The World Cup is the biggest football tournament.",
        
        "deep_learning.txt": "Deep learning uses artificial neural networks with multiple layers to process data. These networks can recognize images, understand speech, and translate languages. It's a powerful AI technique.",
        
        "travel_paris.txt": "Paris is the capital of France, famous for the Eiffel Tower, Louvre Museum, and Notre-Dame Cathedral. The city offers amazing food, art, and architecture for tourists to enjoy.",
        
        "python_coding.txt": "Python is a programming language known for its simplicity and readability. It's widely used in web development, data science, automation, and artificial intelligence applications.",
        
        "climate_science.txt": "Climate change refers to long-term changes in Earth's weather patterns. Rising temperatures, melting ice caps, and extreme weather are signs of climate change caused by human activities.",
        
        "neural_networks.txt": "Neural networks are computing systems inspired by the human brain. They consist of interconnected nodes that process information. Artificial neural networks power many modern AI applications.",
        
        "gardening_guide.txt": "Successful gardening requires understanding soil types, watering schedules, and plant care. Choose plants suitable for your climate and provide adequate sunlight and nutrients for healthy growth."
    }
    
    # Create directory
    os.makedirs("text_files", exist_ok=True)
    
    created = []
    for filename, content in texts.items():
        filepath = os.path.join("text_files", filename)
        with open(filepath, 'w') as f:
            f.write(content)
        created.append(filepath)
    
    return created

def load_files_from_directory(directory: str) -> List[Tuple[str, str]]:
    """Load all text files from directory."""
    files = []
    
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r') as f:
                    content = f.read()
                    files.append((filename, content))
    
    return files

def main_demo():
    """Main demonstration function."""
    
    print("🔍 Simple Embeddings & Vector Store Demo")
    print("=" * 50)
    
    # Step 1: Create sample files
    print("\n📝 Creating 10 sample text files...")
    created_files = create_sample_files()
    print(f"✅ Created {len(created_files)} files in 'text_files' directory")
    
    # Step 2: Initialize vector store
    print("\n🏪 Initializing vector store...")
    store = SimpleVectorStore()
    
    # Step 3: Load and index files
    print("\n📚 Loading and indexing files...")
    files = load_files_from_directory("text_files")
    
    for filename, content in files:
        metadata = {"filename": filename, "word_count": len(content.split())}
        store.add_document(content, metadata)
        print(f"  ✅ {filename}")
    
    print(f"\n📊 Total documents indexed: {len(store.documents)}")
    
    # Step 4: Perform searches
    print("\n🔍 Performing similarity searches...")
    
    test_queries = [
        "Which file talks about AI?",
        "Information about cooking food",
        "Tell me about neural networks", 
        "Sports and games content",
        "Programming languages"
    ]
    
    for query in test_queries:
        print(f"\n❓ Query: '{query}'")
        print("-" * 30)
        
        results = store.search(query, k=3)
        
        for i, (doc, score, metadata) in enumerate(results, 1):
            filename = metadata.get('filename', 'Unknown')
            print(f"  {i}. 📄 {filename}")
            print(f"     🎯 Score: {score:.3f}")
            print(f"     📝 Preview: {doc[:80]}...")
            print()
    
    # Step 5: Save the store
    print("💾 Saving vector store...")
    store.save("my_store")
    print("✅ Saved to 'my_store.json'")
    
    print("\n🎉 Demo completed!")
    print("=" * 50)

if __name__ == "__main__":
    main_demo()