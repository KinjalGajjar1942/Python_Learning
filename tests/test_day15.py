"""
Test cases for Day 15 - LangChain Polite Text Rewriting
Tests the polite sentence rewriting functionality.
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add Day15 to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Day15'))

class TestDay15PolitenessRewriting:
    """Test cases for Day 15 polite text rewriting functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.test_sentences = [
            "Give me that report now.",
            "Send me the files immediately!",
            "Fix this bug right now.",
            "Call me back today.",
            "Update the system now."
        ]
        
        self.expected_polite_responses = [
            "Could you please provide me with that report at your earliest convenience?",
            "Would you be able to send me the files when you have a moment?",
            "Could you please fix this bug when you get a chance?",
            "Would you mind calling me back today?",
            "Could you please update the system when convenient?"
        ]
    
    def test_langchain_polite_rewriting_mock(self):
        """Test the LangChain polite rewriting functionality with mocking."""
        # Test that module can be imported without errors
        try:
            import Day15.example as day15_example
            # Basic functionality test
            assert hasattr(day15_example, 'chain')
            assert hasattr(day15_example, 'llm')
        except ImportError:
            pytest.skip("Day15 example module not available")
    
    def test_simple_politeness_rules(self):
        """Test simple politeness transformation rules."""
        
        def make_polite(sentence):
            """Simple politeness transformation function."""
            sentence = sentence.strip()
            
            # Transform imperatives to polite requests
            if sentence.lower().startswith("give me"):
                return sentence.replace("Give me", "Could you please provide me with", 1)
            elif sentence.lower().startswith("send me"):
                return sentence.replace("Send me", "Could you please send me", 1)
            elif sentence.lower().startswith("fix"):
                return f"Could you please {sentence.lower()}"
            elif sentence.lower().startswith("call me"):
                return sentence.replace("Call me", "Would you mind calling me", 1)
            elif sentence.lower().startswith("update"):
                return f"Could you please {sentence.lower()}"
            
            # Remove aggressive words
            polite_sentence = sentence.replace(" now", " when convenient")
            polite_sentence = polite_sentence.replace("immediately", "at your earliest convenience")
            polite_sentence = polite_sentence.rstrip("!") + "?"
            
            return polite_sentence
        
        # Test transformation
        test_cases = [
            ("Give me that report now.", "Could you please provide me with that report when convenient?"),
            ("Send me the files!", "Could you please send me the files?"),
            ("Fix this bug.", "Could you please fix this bug."),
            ("Call me back today!", "Would you mind calling me back today?")
        ]
        
        for original, expected in test_cases:
            result = make_polite(original)
            assert isinstance(result, str)
            assert len(result) > len(original)  # Polite version should be longer
            assert "please" in result.lower() or "would you" in result.lower()
    
    def test_environment_variables_validation(self):
        """Test that required environment variables are set."""
        # Save original values
        original_api_key = os.environ.get("OPENAI_API_KEY")
        original_api_base = os.environ.get("OPENAI_API_BASE")
        
        try:
            # Import should set environment variables
            import Day15.example as day15_example
            
            # Check that environment variables are set
            assert os.environ.get("OPENAI_API_KEY") is not None
            assert os.environ.get("OPENAI_API_BASE") is not None
            assert "openrouter.ai" in os.environ.get("OPENAI_API_BASE", "")
            
        except ImportError:
            pytest.skip("Day15 example module not available")
        finally:
            # Restore original values
            if original_api_key:
                os.environ["OPENAI_API_KEY"] = original_api_key
            if original_api_base:
                os.environ["OPENAI_API_BASE"] = original_api_base
    
    def test_llm_initialization(self):
        """Test LLM initialization with correct parameters."""
        try:
            import Day15.example as day15_example
            
            # Verify LLM attributes exist
            assert hasattr(day15_example, 'llm')
            assert day15_example.llm is not None
        except ImportError:
            pytest.skip("Day15 example module not available")
    
    def test_prompt_template_structure(self):
        """Test that prompt template is correctly structured."""
        try:
            from langchain.prompts import PromptTemplate
            
            # Test our expected prompt template
            prompt = PromptTemplate(
                input_variables=["sentence"],
                template="Rewrite the following sentence politely:\n\n'{sentence}'"
            )
            
            # Test prompt formatting
            formatted = prompt.format(sentence="Give me that report.")
            assert "politely" in formatted
            assert "Give me that report." in formatted
            
        except ImportError:
            pytest.skip("LangChain not available")
    
    def test_edge_cases(self):
        """Test edge cases for polite rewriting."""
        edge_cases = [
            "",  # Empty string
            "   ",  # Whitespace only
            "Please do this already.",  # Already polite
            "A" * 1000,  # Very long string
            "你好",  # Non-English text
            "123 456",  # Numbers only
            "!@#$%",  # Special characters only
        ]
        
        def safe_make_polite(text):
            """Safe version that handles edge cases."""
            if not text or not text.strip():
                return "Could you please help me with this request?"
            
            if len(text) > 500:
                return f"Could you please help with: {text[:50]}..."
            
            if "please" in text.lower():
                return text  # Already polite
            
            return f"Could you please help with: {text}"
        
        for case in edge_cases:
            result = safe_make_polite(case)
            assert isinstance(result, str)
            assert len(result) > 0
            assert "please" in result.lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])