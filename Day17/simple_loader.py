"""
Simple Document Loader and Summarizer
Day 17 - Python Learning

A minimal implementation for loading PDF/TXT files and basic summarization.
"""

import os

class SimpleDocumentLoader:
    """Simple document loader for TXT files."""
    
    def load_txt(self, file_path: str) -> str:
        """Load text file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error loading file: {e}")
            return ""

class SimpleSummarizer:
    """Basic text summarization."""
    
    def extractive_summary(self, text: str, num_sentences: int = 3) -> str:
        """Simple extractive summary - first, middle, and last sentences."""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        if len(sentences) <= num_sentences:
            return text
        
        # Get first, middle, and last sentences
        summary = []
        summary.append(sentences[0])
        if num_sentences > 2:
            summary.append(sentences[len(sentences)//2])
        summary.append(sentences[-1])
        
        return '. '.join(summary) + '.'

# Demo function
def demo():
    """Quick demo of document loading and summarization."""
    loader = SimpleDocumentLoader()
    summarizer = SimpleSummarizer()
    
    # Sample text (simulating a 2-page PDF content)
    sample_text = """
    Machine learning is transforming industries worldwide. It enables computers to learn from data without explicit programming. 
    Applications include healthcare diagnostics, financial fraud detection, and autonomous vehicles. Deep learning, a subset of ML, 
    uses neural networks to process complex patterns. The technology continues to evolve rapidly. Future developments focus on 
    interpretability and ethical AI deployment.
    """
    
    print("=== Document Loader Demo ===")
    print("\nOriginal Text:")
    print(sample_text.strip())
    
    print("\nSummary (3 sentences):")
    summary = summarizer.extractive_summary(sample_text)
    print(summary)
    
    # Test with sample file if it exists
    if os.path.exists("sample_document.txt"):
        print("\n=== Processing Sample File ===")
        content = loader.load_txt("sample_document.txt")
        if content:
            print(f"File length: {len(content)} characters")
            file_summary = summarizer.extractive_summary(content)
            print(f"\nFile Summary:\n{file_summary}")

if __name__ == "__main__":
    demo()