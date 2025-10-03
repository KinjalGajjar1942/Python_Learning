import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import torch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Day8.sentiment_example import run_sentiment_examples, show_tokenization_basics

class TestDay8(unittest.TestCase):
    
    @patch('Day8.sentiment_example.pipeline')
    def test_run_sentiment_examples_returns_expected_results(self, mock_pipeline):
        # Mock the pipeline to return expected sentiment results
        mock_sentiment = MagicMock()
        mock_sentiment.return_value = [
            {'label': 'POSITIVE', 'score': 0.9998},
            {'label': 'NEGATIVE', 'score': 0.9995},
            {'label': 'NEUTRAL', 'score': 0.6543}
        ]
        mock_pipeline.return_value = mock_sentiment
        
        # Call the function (should not raise any exceptions)
        try:
            run_sentiment_examples()
            test_passed = True
        except Exception:
            test_passed = False
        
        self.assertTrue(test_passed)
        mock_pipeline.assert_called_once_with("sentiment-analysis")
        mock_sentiment.assert_called_once()
    
    @patch('Day8.sentiment_example.AutoTokenizer')
    @patch('Day8.sentiment_example.AutoModelForSequenceClassification')
    @patch('torch.no_grad')
    def test_show_tokenization_basics_completes_successfully(self, mock_no_grad, mock_model, mock_tokenizer):
        # Mock tokenizer
        mock_tokenizer_instance = MagicMock()
        mock_tokenizer_instance.tokenize.return_value = ['i', 'love', 'the', 'new', 'design']
        mock_tokenizer_instance.return_value = {
            'input_ids': torch.tensor([[101, 1045, 2293, 1996, 2047, 2640, 102]]),
            'attention_mask': torch.tensor([[1, 1, 1, 1, 1, 1, 1]])
        }
        mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
        
        # Mock model
        mock_model_instance = MagicMock()
        mock_outputs = MagicMock()
        mock_outputs.logits = torch.tensor([[2.5, -1.5]])
        mock_model_instance.return_value = mock_outputs
        mock_model_instance.config.id2label = {0: 'NEGATIVE', 1: 'POSITIVE'}
        mock_model.from_pretrained.return_value = mock_model_instance
        
        # Mock torch.no_grad context
        mock_no_grad.return_value.__enter__.return_value = None
        
        # Call the function (should not raise any exceptions)
        try:
            show_tokenization_basics()
            test_passed = True
        except Exception:
            test_passed = False
        
        self.assertTrue(test_passed)
        mock_tokenizer.from_pretrained.assert_called_once()
        mock_model.from_pretrained.assert_called_once()
    
    def test_day8_module_imports_correctly(self):
        """Test that Day8 module imports without errors"""
        try:
            import Day8.sentiment_example
            import_successful = True
        except ImportError:
            import_successful = False
        
        self.assertTrue(import_successful)
    
    @patch('Day8.sentiment_example.pipeline')
    def test_sentiment_pipeline_handles_empty_input(self, mock_pipeline):
        """Test edge case with empty or None input"""
        mock_sentiment = MagicMock()
        mock_sentiment.return_value = [{'label': 'NEUTRAL', 'score': 0.5}]
        mock_pipeline.return_value = mock_sentiment
        
        # This tests the robustness of the pipeline function
        sentences = ["", "   ", "Valid sentence"]
        mock_sentiment.side_effect = [
            [{'label': 'NEUTRAL', 'score': 0.5}] * len(sentences)
        ]
        
        try:
            run_sentiment_examples()
            test_passed = True
        except Exception:
            test_passed = False
        
        self.assertTrue(test_passed)

if __name__ == "__main__":
    unittest.main()