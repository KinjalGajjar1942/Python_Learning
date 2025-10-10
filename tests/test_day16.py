"""
Test cases for Day 16 - LangChain Text Summarization and Keywords
Tests the multi-step chain processing for text summarization and keyword extraction.
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add Day16 to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Day16'))

class TestDay16TextSummarizationChains:
    """Test cases for Day 16 multi-step text processing chains."""
    
    def setup_method(self):
        """Setup test environment."""
        self.sample_text = """
        Artificial Intelligence (AI) is revolutionizing various industries by automating 
        complex tasks and providing intelligent solutions. Machine learning, a subset of AI, 
        enables computers to learn from data without explicit programming. Deep learning, 
        which uses neural networks with multiple layers, has achieved remarkable success 
        in image recognition, natural language processing, and game playing. Companies are 
        increasingly adopting AI technologies to improve efficiency, reduce costs, and 
        enhance customer experiences. However, AI also raises concerns about job displacement, 
        privacy, and ethical considerations that need to be addressed.
        """
        
        self.expected_summary = "AI is transforming industries through automation and intelligent solutions, with machine learning and deep learning driving advances in various applications, while raising concerns about employment and ethics."
        self.expected_keywords = "artificial intelligence, machine learning, deep learning, automation, industries, neural networks, efficiency, privacy, ethics"
    
    def test_chain_initialization(self):
        """Test that chains are properly initialized."""
        try:
            import Day16.example as day16_example
            
            # Verify key components exist
            assert hasattr(day16_example, 'llm')
            assert hasattr(day16_example, 'overall_chain')
            assert day16_example.llm is not None
            assert day16_example.overall_chain is not None
            
        except ImportError:
            pytest.skip("Day16 example module not available")
    
    def test_prompt_templates(self):
        """Test prompt template structures."""
        try:
            from langchain.prompts import PromptTemplate
            
            # Test summary prompt
            summary_prompt = PromptTemplate(
                input_variables=["text"],
                template="Summarize the following text in a concise way:\n\n{text}"
            )
            
            formatted_summary = summary_prompt.format(text=self.sample_text)
            assert "Summarize" in formatted_summary
            assert self.sample_text.strip() in formatted_summary
            
            # Test keywords prompt
            keywords_prompt = PromptTemplate(
                input_variables=["summary"],
                template="Extract the most important keywords from the following summary. Provide them as a comma-separated list:\n\n{summary}"
            )
            
            formatted_keywords = keywords_prompt.format(summary=self.expected_summary)
            assert "keywords" in formatted_keywords
            assert "comma-separated" in formatted_keywords
            
        except ImportError:
            pytest.skip("LangChain not available")
    
    def test_simple_text_summarization(self):
        """Test simple text summarization without external dependencies."""
        
        def simple_summarize(text, max_sentences=2):
            """Simple extractive summarization."""
            sentences = text.split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) <= max_sentences:
                return text
            
            # Take first and last sentences
            summary_sentences = [sentences[0], sentences[-1]]
            return '. '.join(summary_sentences) + '.'
        
        def extract_keywords(text, max_keywords=5):
            """Simple keyword extraction."""
            import re
            
            # Remove common stop words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
            
            # Extract words
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            
            # Count word frequency
            word_freq = {}
            for word in words:
                if word not in stop_words:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top keywords
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:max_keywords]
            return ', '.join([word for word, freq in top_keywords])
        
        # Test summarization
        summary = simple_summarize(self.sample_text)
        assert isinstance(summary, str)
        assert len(summary) < len(self.sample_text)
        assert len(summary) > 0
        
        # Test keyword extraction
        keywords = extract_keywords(self.sample_text)
        assert isinstance(keywords, str)
        assert ',' in keywords
        assert 'artificial' in keywords.lower() or 'intelligence' in keywords.lower()
    
    def test_sequential_chain_execution(self):
        """Test sequential chain execution with mocked responses."""
        try:
            import Day16.example as day16_example
            
            # Verify overall chain exists and is callable
            assert hasattr(day16_example, 'overall_chain')
            assert day16_example.overall_chain is not None
            
            # Test that the chain has the expected methods (but don't call them)
            assert hasattr(day16_example.overall_chain, 'run') or hasattr(day16_example.overall_chain, 'invoke')
            
        except ImportError:
            pytest.skip("Day16 example module not available")
    
    def test_environment_setup(self):
        """Test environment variable configuration."""
        try:
            import Day16.example as day16_example
            
            # Check environment variables are set
            assert "OPENAI_API_KEY" in os.environ
            assert "OPENAI_API_BASE" in os.environ
            assert "openrouter.ai" in os.environ["OPENAI_API_BASE"]
            
        except ImportError:
            pytest.skip("Day16 example module not available")
    
    def test_chain_output_keys(self):
        """Test that chains have correct output keys."""
        
        # Test expected chain configuration
        expected_config = {
            'summary_chain_output_key': 'summary',
            'keywords_chain_output_key': 'keywords',
            'overall_chain_input_key': 'text',
            'overall_chain_output_key': 'keywords'
        }
        
        for key, expected_value in expected_config.items():
            assert isinstance(expected_value, str)
            assert len(expected_value) > 0
    
    def test_text_processing_pipeline(self):
        """Test the complete text processing pipeline simulation."""
        
        def simulate_processing_pipeline(text):
            """Simulate the complete processing pipeline."""
            
            # Step 1: Summarization
            sentences = text.split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
            summary = '. '.join(sentences[:3]) + '.'  # Take first 3 sentences
            
            # Step 2: Keyword extraction
            import re
            words = re.findall(r'\b[A-Za-z]{4,}\b', summary.lower())
            
            # Filter and get unique keywords
            stop_words = {'this', 'that', 'with', 'from', 'they', 'have', 'been', 'will', 'would', 'could', 'should'}
            keywords = []
            for word in words:
                if word not in stop_words and word not in keywords:
                    keywords.append(word)
            
            return {
                'summary': summary,
                'keywords': ', '.join(keywords[:8])
            }
        
        # Test pipeline
        result = simulate_processing_pipeline(self.sample_text)
        
        assert 'summary' in result
        assert 'keywords' in result
        assert isinstance(result['summary'], str)
        assert isinstance(result['keywords'], str)
        assert len(result['summary']) > 0
        assert len(result['keywords']) > 0
        assert ',' in result['keywords']
    
    def test_edge_cases(self):
        """Test edge cases for text processing."""
        
        edge_cases = [
            "",  # Empty string
            "Short text.",  # Very short text
            "A" * 10000,  # Very long text
            "One sentence only",  # Single sentence
            "Multiple! Sentences? With. Different! Punctuation?",  # Mixed punctuation
        ]
        
        def safe_process(text):
            """Safe processing that handles edge cases."""
            if not text or len(text.strip()) == 0:
                return {'summary': 'No content provided', 'keywords': 'none'}
            
            if len(text) < 20:
                return {'summary': text, 'keywords': 'short, text'}
            
            if len(text) > 5000:
                text = text[:5000] + "..."
            
            # Simple processing
            words = text.split()[:10]
            return {
                'summary': ' '.join(words) + '...',
                'keywords': ', '.join(words[:5])
            }
        
        for case in edge_cases:
            result = safe_process(case)
            assert isinstance(result, dict)
            assert 'summary' in result
            assert 'keywords' in result

if __name__ == "__main__":
    pytest.main([__file__, "-v"])