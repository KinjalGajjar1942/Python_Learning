import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestDay10(unittest.TestCase):
    
    def setUp(self):
        """Set up test client for FastAPI app"""
        # Mock the sentiment pipeline before importing
        with patch('Day10.sentiment_api.pipeline') as mock_pipeline:
            mock_sentiment = MagicMock()
            mock_sentiment.return_value = [{'label': 'POSITIVE', 'score': 0.9998}]
            mock_pipeline.return_value = mock_sentiment
            
            from Day10.sentiment_api import app
            self.app = app
            self.client = TestClient(app)
    
    def test_root_endpoint_returns_message(self):
        """Test that root endpoint returns expected message"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Sentiment Analysis API is running!"})
    
    @patch('Day10.sentiment_api.sentiment_pipeline')
    def test_analyze_endpoint_with_positive_text(self, mock_pipeline):
        """Test analyze endpoint with positive sentiment text"""
        # Mock the pipeline response
        mock_pipeline.return_value = [{'label': 'POSITIVE', 'score': 0.9998}]
        
        # Test data
        test_data = {"text": "I love this product!"}
        
        # Make request
        response = self.client.post("/analyze", json=test_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["label"], "POSITIVE")
        self.assertIsInstance(response_data["score"], float)
        mock_pipeline.assert_called_once_with("I love this product!")
    
    @patch('Day10.sentiment_api.sentiment_pipeline')
    def test_analyze_endpoint_with_negative_text(self, mock_pipeline):
        """Test analyze endpoint with negative sentiment text"""
        # Mock the pipeline response
        mock_pipeline.return_value = [{'label': 'NEGATIVE', 'score': 0.9995}]
        
        # Test data
        test_data = {"text": "This is terrible!"}
        
        # Make request
        response = self.client.post("/analyze", json=test_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["label"], "NEGATIVE")
        self.assertEqual(response_data["score"], 0.9995)
    
    def test_analyze_endpoint_with_invalid_json(self):
        """Test analyze endpoint with invalid JSON structure"""
        # Missing 'text' field
        test_data = {"message": "Invalid structure"}
        
        response = self.client.post("/analyze", json=test_data)
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_analyze_endpoint_with_empty_text(self):
        """Test analyze endpoint with empty text"""
        test_data = {"text": ""}
        
        # This should still work but may return different results
        response = self.client.post("/analyze", json=test_data)
        self.assertEqual(response.status_code, 200)
    
    @patch('Day10.sentiment_api.sentiment_pipeline')
    def test_analyze_endpoint_response_format(self, mock_pipeline):
        """Test that analyze endpoint returns correct response format"""
        # Mock the pipeline response
        mock_pipeline.return_value = [{'label': 'POSITIVE', 'score': 0.8765}]
        
        test_data = {"text": "Great day today!"}
        response = self.client.post("/analyze", json=test_data)
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        
        # Check response structure
        self.assertIn("label", response_data)
        self.assertIn("score", response_data)
        self.assertIsInstance(response_data["label"], str)
        self.assertIsInstance(response_data["score"], float)
    
    def test_day10_module_imports_correctly(self):
        """Test that Day10 module imports without errors"""
        try:
            from Day10.sentiment_api import app, TextRequest
            import_successful = True
        except ImportError:
            import_successful = False
        
        self.assertTrue(import_successful)
    
    def test_text_request_model_validation(self):
        """Test that TextRequest model validates input correctly"""
        from Day10.sentiment_api import TextRequest
        
        # Valid text request
        valid_request = TextRequest(text="Hello world")
        self.assertEqual(valid_request.text, "Hello world")
        
        # Test that text field is required
        try:
            TextRequest()
            validation_failed = False
        except Exception:
            validation_failed = True
        
        self.assertTrue(validation_failed)
    
    @patch('Day10.sentiment_api.sentiment_pipeline')
    def test_long_text_handling(self, mock_pipeline):
        """Test handling of long text input"""
        # Mock the pipeline response
        mock_pipeline.return_value = [{'label': 'NEUTRAL', 'score': 0.5432}]
        
        # Create a long text
        long_text = "This is a very long text. " * 100
        test_data = {"text": long_text}
        
        response = self.client.post("/analyze", json=test_data)
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("label", response_data)
        self.assertIn("score", response_data)

if __name__ == "__main__":
    unittest.main()