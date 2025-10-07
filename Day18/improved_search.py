"""
Improved Vector Store with Better Text Processing
Day 18 - Python Learning
"""

import os
import math
import json
from typing import List, Tuple, Dict, Set

class ImprovedVectorStore:
    """Improved vector store with better text preprocessing."""
    
    def __init__(self):
        self.documents = []
        self.metadata = []
        self.word_vectors = {}
        
        # Common stop words to ignore
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'this', 'that', 'these', 'those', 'it', 'its', 'as', 'can', 'from'
        }
    
    def preprocess_text(self, text: str) -> List[str]:
        """Clean and preprocess text."""
        # Convert to lowercase
        text = text.lower()
        
        # Extract words (alphanumeric only)
        words = []
        current_word = ""
        
        for char in text:
            if char.isalnum():
                current_word += char
            else:
                if current_word:
                    words.append(current_word)
                    current_word = ""
        
        if current_word:  # Don't forget the last word
            words.append(current_word)
        
        # Filter out stop words and short words
        meaningful_words = []
        for word in words:
            if len(word) > 2 and word not in self.stop_words:
                meaningful_words.append(word)
        
        return meaningful_words
    
    def create_word_vector(self, text: str) -> Dict[str, float]:
        """Create TF (Term Frequency) vector."""
        words = self.preprocess_text(text)
        vector = {}
        
        # Count word frequencies
        for word in words:
            vector[word] = vector.get(word, 0) + 1
        
        # Normalize by document length (TF)
        total_words = len(words)
        if total_words > 0:
            for word in vector:
                vector[word] = vector[word] / total_words
        
        return vector
    
    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate cosine similarity."""
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
    
    def keyword_overlap_score(self, query_words: List[str], doc_text: str) -> float:
        """Calculate keyword overlap score."""
        doc_words = set(self.preprocess_text(doc_text))
        query_words_set = set(query_words)
        
        overlap = len(query_words_set & doc_words)
        return overlap / len(query_words_set) if query_words_set else 0.0
    
    def add_document(self, text: str, metadata: Dict = None):
        """Add document to store."""
        if metadata is None:
            metadata = {}
        
        vector = self.create_word_vector(text)
        
        self.documents.append(text)
        self.metadata.append(metadata)
        self.word_vectors[len(self.documents) - 1] = vector
    
    def search(self, query: str, k: int = 3) -> List[Tuple[str, float, Dict]]:
        """Enhanced search with multiple scoring methods."""
        query_vector = self.create_word_vector(query)
        query_words = self.preprocess_text(query)
        
        scores = []
        
        for idx in range(len(self.documents)):
            doc_vector = self.word_vectors[idx]
            doc_text = self.documents[idx]
            
            # Calculate different similarity scores
            cosine_sim = self.cosine_similarity(query_vector, doc_vector)
            keyword_overlap = self.keyword_overlap_score(query_words, doc_text)
            
            # Combined score (weighted average)
            combined_score = 0.7 * cosine_sim + 0.3 * keyword_overlap
            
            scores.append((combined_score, idx))
        
        # Sort by score (descending)
        scores.sort(reverse=True)
        
        # Return top k results
        results = []
        for score, idx in scores[:k]:
            results.append((
                self.documents[idx],
                score,
                self.metadata[idx]
            ))
        
        return results

def demo_improved_search():
    """Demo with improved search capabilities."""
    
    print("🚀 Improved Vector Store Demo")
    print("=" * 40)
    
    # Initialize improved store
    store = ImprovedVectorStore()
    
    # Sample documents focused on AI
    documents = [
        ("ai_introduction.txt", "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, and self-correction."),
        
        ("machine_learning_guide.txt", "Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data."),
        
        ("cooking_recipes.txt", "Learn how to cook delicious Italian pasta with tomato sauce. Heat olive oil in a pan, add garlic, then crushed tomatoes. Season with salt, pepper, and fresh basil leaves."),
        
        ("sports_news.txt", "The basketball championship finals will be held next month. Teams have been training hard all season. Fans are excited to see which team will win the trophy this year."),
        
        ("deep_learning_neural.txt", "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Neural networks mimic the human brain."),
        
        ("travel_guide_europe.txt", "Europe offers amazing destinations for travelers. Visit Rome for ancient history, Paris for art and culture, or Barcelona for beautiful architecture and beaches."),
        
        ("python_programming.txt", "Python is a high-level programming language known for its simple syntax. It's widely used in web development, data science, and artificial intelligence applications."),
        
        ("climate_environment.txt", "Climate change is a long-term shift in global weather patterns. Human activities like burning fossil fuels contribute to greenhouse gas emissions and global warming."),
        
        ("neural_networks_ai.txt", "Neural networks are computing systems vaguely inspired by the biological neural networks. Artificial neural networks are used in artificial intelligence and machine learning."),
        
        ("gardening_plants.txt", "Growing healthy plants requires proper soil, adequate water, and sufficient sunlight. Choose plants that match your local climate and soil conditions for best results.")
    ]
    
    # Add documents to store
    print("\n📚 Loading documents into vector store...")
    for filename, content in documents:
        metadata = {"filename": filename, "length": len(content)}
        store.add_document(content, metadata)
        print(f"  ✅ {filename}")
    
    # Test searches
    print(f"\n📊 Indexed {len(documents)} documents")
    print("\n🔍 Testing search queries...")
    
    queries = [
        "Which file talks about AI?",
        "artificial intelligence information", 
        "cooking and recipes",
        "neural networks and machine learning",
        "sports and games"
    ]
    
    for query in queries:
        print(f"\n❓ Query: '{query}'")
        print("-" * 25)
        
        results = store.search(query, k=3)
        
        for i, (doc, score, metadata) in enumerate(results, 1):
            filename = metadata.get('filename', 'Unknown')
            print(f"  {i}. 📄 {filename}")
            print(f"     🎯 Score: {score:.3f}")
            print(f"     📝 {doc[:70]}...")
            print()
    
    print("🎉 Improved search demo completed!")

if __name__ == "__main__":
    demo_improved_search()