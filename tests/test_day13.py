import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestDay13(unittest.TestCase):
    
    def setUp(self):
        """Set up test client for FastAPI app"""
        # Mock the sentiment pipeline before importing
        with patch('Day13.sentiment_api.pipeline') as mock_pipeline:
            mock_sentiment = MagicMock()
            mock_sentiment.return_value = [{'label': 'POSITIVE', 'score': 0.9998}]
            mock_pipeline.return_value = mock_sentiment
            
            from Day13.sentiment_api import app
            self.app = app
            self.client = TestClient(app)
    
    @patch('Day13.sentiment_api.sentiment_model')
    def test_predict_endpoint_with_positive_sentiment(self, mock_sentiment):
        """Test predict endpoint with positive sentiment text"""
        # Mock the sentiment model response
        mock_sentiment.return_value = [{'label': 'POSITIVE', 'score': 0.9876}]
        
        # Test data
        test_data = {"text": "I absolutely love this product!"}
        
        # Make request
        response = self.client.post("/predict", json=test_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["input"], "I absolutely love this product!")
        self.assertEqual(response_data["prediction"][0]["label"], "POSITIVE")
        self.assertEqual(response_data["prediction"][0]["score"], 0.9876)
    
    @patch('Day13.sentiment_api.sentiment_model')
    def test_predict_endpoint_with_negative_sentiment(self, mock_sentiment):
        """Test predict endpoint with negative sentiment text"""
        # Mock the sentiment model response
        mock_sentiment.return_value = [{'label': 'NEGATIVE', 'score': 0.9543}]
        
        # Test data
        test_data = {"text": "This is absolutely terrible!"}
        
        # Make request
        response = self.client.post("/predict", json=test_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["input"], "This is absolutely terrible!")
        self.assertEqual(response_data["prediction"][0]["label"], "NEGATIVE")
    
    def test_cors_middleware_configuration(self):
        """Test that CORS middleware is properly configured"""
        # Test preflight request
        response = self.client.options("/predict", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        })
        
        # Should allow CORS requests (status might be 200 or 405, both acceptable for CORS test)
        self.assertIn(response.status_code, [200, 405])
        
        # Test actual CORS headers in a real request
        test_data = {"text": "Test"}
        response = self.client.post("/predict", json=test_data, headers={
            "Origin": "http://localhost:3000"
        })
        
        # Should include CORS headers in response
        self.assertEqual(response.status_code, 200)
    
    def test_predict_endpoint_with_invalid_json(self):
        """Test predict endpoint with invalid JSON structure"""
        # Missing 'text' field
        test_data = {"message": "Invalid structure"}
        
        response = self.client.post("/predict", json=test_data)
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_predict_endpoint_with_empty_text(self):
        """Test predict endpoint with empty text"""
        test_data = {"text": ""}
        
        response = self.client.post("/predict", json=test_data)
        self.assertEqual(response.status_code, 200)
    
    @patch('Day13.sentiment_api.sentiment_model')
    def test_predict_response_format(self, mock_sentiment):
        """Test that predict endpoint returns correct response format"""
        # Mock the sentiment model response
        mock_sentiment.return_value = [{'label': 'POSITIVE', 'score': 0.8765}]
        
        test_data = {"text": "Great service!"}
        response = self.client.post("/predict", json=test_data)
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        
        # Check response structure
        self.assertIn("input", response_data)
        self.assertIn("prediction", response_data)
        self.assertEqual(response_data["input"], "Great service!")
        self.assertIsInstance(response_data["prediction"], list)
        self.assertIn("label", response_data["prediction"][0])
        self.assertIn("score", response_data["prediction"][0])
    
    def test_day13_module_imports_correctly(self):
        """Test that Day13 module imports without errors"""
        try:
            from Day13.sentiment_api import app, TextRequest
            import_successful = True
        except ImportError:
            import_successful = False
        
        self.assertTrue(import_successful)
    
    def test_text_request_model_validation(self):
        """Test that TextRequest model validates input correctly"""
        from Day13.sentiment_api import TextRequest
        
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
    
    @patch('Day13.sentiment_api.sentiment_model')
    def test_async_endpoint_functionality(self, mock_sentiment):
        """Test that async endpoint works correctly"""
        # Mock the sentiment model response
        mock_sentiment.return_value = [{'label': 'POSITIVE', 'score': 0.9234}]
        
        test_data = {"text": "Async test message"}
        response = self.client.post("/predict", json=test_data)
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["input"], "Async test message")
    
    @patch('Day13.sentiment_api.sentiment_model')
    def test_long_text_handling(self, mock_sentiment):
        """Test handling of long text input"""
        # Mock the sentiment model response
        mock_sentiment.return_value = [{'label': 'NEUTRAL', 'score': 0.5432}]
        
        # Create a long text
        long_text = "This is a very long text message. " * 50
        test_data = {"text": long_text}
        
        response = self.client.post("/predict", json=test_data)
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["input"], long_text)
    
    def test_fastapi_app_title_configuration(self):
        """Test that FastAPI app is configured with correct title"""
        from Day13.sentiment_api import app
        
        self.assertEqual(app.title, "Sentiment Analysis API")
    
    @patch('Day13.sentiment_api.sentiment_model')
    def test_multiple_requests_handling(self, mock_sentiment):
        """Test that the API can handle multiple consecutive requests"""
        # Mock different responses for each request
        mock_sentiment.side_effect = [
            [{'label': 'POSITIVE', 'score': 0.95}],
            [{'label': 'NEGATIVE', 'score': 0.87}],
            [{'label': 'POSITIVE', 'score': 0.72}]
        ]
        
        # Make multiple requests
        requests_data = [
            {"text": "Great product!"},
            {"text": "Terrible experience"},
            {"text": "It's okay"}
        ]
        
        responses = []
        for data in requests_data:
            response = self.client.post("/predict", json=data)
            self.assertEqual(response.status_code, 200)
            responses.append(response.json())
        
        # Verify all requests were processed correctly
        self.assertEqual(len(responses), 3)
        self.assertEqual(mock_sentiment.call_count, 3)
    
    def test_cors_origins_configuration(self):
        """Test that CORS origins are configured correctly"""
        # Import to check the origins configuration
        from Day13.sentiment_api import origins
        
        # Should allow all origins as configured
        self.assertEqual(origins, ["*"])

if __name__ == "__main__":
    unittest.main()