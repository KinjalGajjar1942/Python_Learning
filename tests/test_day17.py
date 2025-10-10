"""
Test cases for Day 17 - Document Loaders & Summarization
Tests document loading, text processing, and summarization functionality.
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock, mock_open
import tempfile

# Add Day17 to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Day17'))

class TestDay17DocumentLoaders:
    """Test cases for Day 17 document loading and summarization."""
    
    def setup_method(self):
        """Setup test environment."""
        self.sample_text = """
        This is a sample document for testing purposes. It contains multiple sentences 
        and paragraphs to test the document loading and summarization functionality.
        
        The document discusses various topics including technology, science, and education.
        These topics are important for understanding modern developments in various fields.
        
        Document processing is crucial for information extraction and analysis in many
        applications including search engines, content management, and data analytics.
        """
        
        self.sample_pdf_content = "Sample PDF content for testing document loaders and summarization features."
        
    def test_text_file_loading(self):
        """Test loading text files."""
        
        def load_text_file(filepath):
            """Simple text file loader."""
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                return ""
            except Exception as e:
                return f"Error: {str(e)}"
        
        # Test with temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            tmp.write(self.sample_text)
            tmp_path = tmp.name
        
        try:
            content = load_text_file(tmp_path)
            assert isinstance(content, str)
            assert len(content) > 0
            assert "sample document" in content
        finally:
            os.unlink(tmp_path)
        
        # Test with non-existent file
        content = load_text_file("nonexistent.txt")
        assert content == ""
    
    def test_document_summarization(self):
        """Test document summarization functionality."""
        
        def simple_summarize(text, num_sentences=3):
            """Simple extractive summarization."""
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            
            if len(sentences) <= num_sentences:
                return text
            
            # Take first, middle, and last sentences
            indices = [0, len(sentences) // 2, -1]
            summary_sentences = [sentences[i] for i in indices]
            return '. '.join(summary_sentences) + '.'
        
        summary = simple_summarize(self.sample_text)
        
        assert isinstance(summary, str)
        assert len(summary) < len(self.sample_text)
        assert summary.count('.') <= 4  # Should have 3 sentences + final period
        assert "sample document" in summary
    
    def test_document_metadata_extraction(self):
        """Test extraction of document metadata."""
        
        def extract_metadata(text, filepath="test.txt"):
            """Extract basic document metadata."""
            return {
                'filename': os.path.basename(filepath),
                'extension': os.path.splitext(filepath)[1],
                'character_count': len(text),
                'word_count': len(text.split()),
                'line_count': text.count('\n') + 1,
                'paragraph_count': len([p for p in text.split('\n\n') if p.strip()])
            }
        
        metadata = extract_metadata(self.sample_text, "sample.txt")
        
        assert metadata['filename'] == "sample.txt"
        assert metadata['extension'] == ".txt"
        assert metadata['character_count'] > 0
        assert metadata['word_count'] > 0
        assert metadata['line_count'] > 0
        assert metadata['paragraph_count'] > 0
    
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_document_loading(self, mock_file):
        """Test loading multiple documents."""
        
        def load_multiple_documents(file_paths):
            """Load multiple documents and return content with metadata."""
            documents = []
            
            for filepath in file_paths:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        documents.append({
                            'filepath': filepath,
                            'filename': os.path.basename(filepath),
                            'content': content,
                            'length': len(content)
                        })
                except Exception as e:
                    documents.append({
                        'filepath': filepath,
                        'filename': os.path.basename(filepath),
                        'content': "",
                        'error': str(e),
                        'length': 0
                    })
            
            return documents
        
        # Mock file content
        mock_file.return_value.read.return_value = self.sample_text
        
        test_files = ["doc1.txt", "doc2.txt", "doc3.txt"]
        documents = load_multiple_documents(test_files)
        
        assert len(documents) == 3
        for doc in documents:
            assert 'filepath' in doc
            assert 'filename' in doc
            assert 'content' in doc
            assert 'length' in doc
    
    def test_text_preprocessing(self):
        """Test text preprocessing functionality."""
        
        def preprocess_text(text):
            """Clean and preprocess text."""
            # Remove extra whitespace
            text = ' '.join(text.split())
            
            # Remove special characters but keep punctuation
            import re
            text = re.sub(r'[^\w\s.,!?;:]', '', text)
            
            # Convert to lowercase for processing (keep original for display)
            processed = {
                'original': text,
                'lowercase': text.lower(),
                'word_count': len(text.split()),
                'sentences': [s.strip() for s in text.split('.') if s.strip()]
            }
            
            return processed
        
        processed = preprocess_text(self.sample_text)
        
        assert 'original' in processed
        assert 'lowercase' in processed
        assert 'word_count' in processed
        assert 'sentences' in processed
        assert processed['word_count'] > 0
        assert len(processed['sentences']) > 0
        assert processed['lowercase'] == processed['original'].lower()
    
    def test_keyword_extraction(self):
        """Test keyword extraction from documents."""
        
        def extract_keywords(text, max_keywords=10):
            """Extract keywords using simple frequency analysis."""
            import re
            
            # Common stop words to filter out
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
                'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 
                'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 
                'would', 'could', 'should', 'this', 'that', 'these', 'those'
            }
            
            # Extract words (alphanumeric only, length > 2)
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            
            # Count word frequency
            word_freq = {}
            for word in words:
                if word not in stop_words:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Sort by frequency and return top keywords
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [word for word, freq in top_keywords[:max_keywords]]
        
        keywords = extract_keywords(self.sample_text)
        
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        assert len(keywords) <= 10
        assert 'document' in keywords or 'testing' in keywords
    
    def test_document_chunking(self):
        """Test splitting documents into chunks."""
        
        def chunk_document(text, chunk_size=100, overlap=20):
            """Split document into overlapping chunks."""
            chunks = []
            
            words = text.split()
            
            for i in range(0, len(words), chunk_size - overlap):
                chunk_words = words[i:i + chunk_size]
                if chunk_words:
                    chunk_text = ' '.join(chunk_words)
                    chunks.append({
                        'text': chunk_text,
                        'start_word': i,
                        'end_word': i + len(chunk_words) - 1,
                        'word_count': len(chunk_words)
                    })
            
            return chunks
        
        chunks = chunk_document(self.sample_text, chunk_size=20, overlap=5)
        
        assert isinstance(chunks, list)
        assert len(chunks) > 0
        
        for chunk in chunks:
            assert 'text' in chunk
            assert 'start_word' in chunk
            assert 'end_word' in chunk
            assert 'word_count' in chunk
            assert chunk['word_count'] > 0
    
    def test_file_format_detection(self):
        """Test detection of different file formats."""
        
        def detect_file_format(filepath):
            """Detect file format based on extension."""
            extension = os.path.splitext(filepath)[1].lower()
            
            format_map = {
                '.txt': 'text',
                '.pdf': 'pdf',
                '.doc': 'word',
                '.docx': 'word',
                '.md': 'markdown',
                '.html': 'html',
                '.json': 'json',
                '.csv': 'csv'
            }
            
            return format_map.get(extension, 'unknown')
        
        test_cases = [
            ('document.txt', 'text'),
            ('report.pdf', 'pdf'),
            ('readme.md', 'markdown'),
            ('data.json', 'json'),
            ('unknown.xyz', 'unknown')
        ]
        
        for filepath, expected_format in test_cases:
            detected = detect_file_format(filepath)
            assert detected == expected_format
    
    def test_error_handling(self):
        """Test error handling in document processing."""
        
        def safe_process_document(text):
            """Safely process document with error handling."""
            try:
                if not text or not text.strip():
                    return {'error': 'Empty document', 'processed': False}
                
                if len(text) > 1000000:  # Very large document
                    return {'error': 'Document too large', 'processed': False}
                
                # Process document
                processed = {
                    'content': text[:1000],  # Truncate if needed
                    'word_count': len(text.split()),
                    'processed': True,
                    'error': None
                }
                
                return processed
                
            except Exception as e:
                return {'error': f'Processing failed: {str(e)}', 'processed': False}
        
        # Test normal case
        result = safe_process_document(self.sample_text)
        assert result['processed'] == True
        assert result['error'] is None
        
        # Test empty document
        result = safe_process_document("")
        assert result['processed'] == False
        assert 'Empty document' in result['error']
        
        # Test very large document
        large_text = "A" * 2000000
        result = safe_process_document(large_text)
        assert result['processed'] == False
        assert 'too large' in result['error']
    
    def test_document_similarity(self):
        """Test basic document similarity comparison."""
        
        def calculate_similarity(doc1, doc2):
            """Calculate simple word-based similarity between documents."""
            words1 = set(doc1.lower().split())
            words2 = set(doc2.lower().split())
            
            intersection = words1 & words2
            union = words1 | words2
            
            if len(union) == 0:
                return 0.0
            
            return len(intersection) / len(union)
        
        doc1 = "This is a test document about machine learning and AI"
        doc2 = "This document discusses machine learning algorithms and AI applications"
        doc3 = "Cooking recipes and kitchen tips for beginners"
        
        # Similar documents should have higher similarity
        similarity_1_2 = calculate_similarity(doc1, doc2)
        similarity_1_3 = calculate_similarity(doc1, doc3)
        
        assert 0.0 <= similarity_1_2 <= 1.0
        assert 0.0 <= similarity_1_3 <= 1.0
        assert similarity_1_2 > similarity_1_3  # More similar documents

if __name__ == "__main__":
    pytest.main([__file__, "-v"])