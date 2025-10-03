import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestDay14(unittest.TestCase):
    
    def setUp(self):
        """Set up test client for FastAPI app"""
        # Mock both pipelines before importing
        with patch('Day14.testApi.pipeline') as mock_pipeline:
            mock_sentiment = MagicMock()
            mock_sentiment.return_value = [{'label': 'POSITIVE', 'score': 0.9998}]
            mock_summarizer = MagicMock()
            mock_summarizer.return_value = [{'summary_text': 'Test summary'}]
            
            # Configure pipeline to return different models based on task
            def pipeline_side_effect(task, **kwargs):
                if task == "sentiment-analysis":
                    return mock_sentiment
                elif task == "summarization":
                    return mock_summarizer
                return MagicMock()
            
            mock_pipeline.side_effect = pipeline_side_effect
            
            from Day14.testApi import app
            self.app = app
            self.client = TestClient(app)
    
    @patch('Day14.testApi.sentiment_model')
    def test_sentiment_endpoint_positive(self, mock_sentiment):
        """Test sentiment endpoint with positive text"""
        # Mock the sentiment model response
        mock_sentiment.return_value = [{'label': 'POSITIVE', 'score': 0.9876}]
        
        # Test data
        test_data = {"text": "I love this amazing product!"}
        
        # Make request
        response = self.client.post("/sentiment", json=test_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["input"], "I love this amazing product!")
        self.assertEqual(response_data["sentiment"][0]["label"], "POSITIVE")
        self.assertEqual(response_data["sentiment"][0]["score"], 0.9876)
    
    @patch('Day14.testApi.sentiment_model')
    def test_sentiment_endpoint_negative(self, mock_sentiment):
        """Test sentiment endpoint with negative text"""
        # Mock the sentiment model response
        mock_sentiment.return_value = [{'label': 'NEGATIVE', 'score': 0.9543}]
        
        # Test data
        test_data = {"text": "This is completely awful!"}
        
        # Make request
        response = self.client.post("/sentiment", json=test_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["input"], "This is completely awful!")
        self.assertEqual(response_data["sentiment"][0]["label"], "NEGATIVE")
    
    @patch('Day14.testApi.summarizer_model')
    def test_summary_endpoint(self, mock_summarizer):
        """Test summary endpoint functionality"""
        # Mock the summarizer model response
        expected_summary = "This is a concise summary of the input text."
        mock_summarizer.return_value = [{'summary_text': expected_summary}]
        
        # Test data with long text
        test_data = {
            "text": "This is a very long article about artificial intelligence and machine learning. " * 10
        }
        
        # Make request
        response = self.client.post("/summary", json=test_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("input", response_data)
        self.assertEqual(response_data["summary"], expected_summary)
        
        # Verify summarizer was called with correct parameters
        mock_summarizer.assert_called_once()
        call_args, call_kwargs = mock_summarizer.call_args
        self.assertIn('max_length', call_kwargs)
        self.assertIn('min_length', call_kwargs)
        self.assertIn('do_sample', call_kwargs)
        self.assertEqual(call_kwargs['max_length'], 50)
        self.assertEqual(call_kwargs['min_length'], 25)
        self.assertEqual(call_kwargs['do_sample'], False)
    
    def test_cors_middleware_configuration(self):
        """Test that CORS middleware is properly configured"""
        # Test preflight request for sentiment endpoint
        response = self.client.options("/sentiment", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        })
        
        # Should handle CORS requests
        self.assertIn(response.status_code, [200, 405])
        
        # Test preflight request for summary endpoint
        response = self.client.options("/summary", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        })
        
        self.assertIn(response.status_code, [200, 405])
    
    def test_sentiment_endpoint_with_invalid_json(self):
        """Test sentiment endpoint with invalid JSON structure"""
        # Missing 'text' field
        test_data = {"message": "Invalid structure"}
        
        response = self.client.post("/sentiment", json=test_data)
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_summary_endpoint_with_invalid_json(self):
        """Test summary endpoint with invalid JSON structure"""
        # Missing 'text' field
        test_data = {"content": "Invalid structure"}
        
        response = self.client.post("/summary", json=test_data)
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_endpoints_with_empty_text(self):
        """Test both endpoints with empty text"""
        test_data = {"text": ""}
        
        # Test sentiment endpoint
        response = self.client.post("/sentiment", json=test_data)
        self.assertEqual(response.status_code, 200)
        
        # Test summary endpoint
        response = self.client.post("/summary", json=test_data)
        self.assertEqual(response.status_code, 200)
    
    def test_day14_module_imports_correctly(self):
        """Test that Day14 module imports without errors"""
        try:
            from Day14.testApi import app, TextRequest
            import_successful = True
        except ImportError:
            import_successful = False
        
        self.assertTrue(import_successful)
    
    def test_text_request_model_validation(self):
        """Test that TextRequest model validates input correctly"""
        from Day14.testApi import TextRequest
        
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
    
    @patch('Day14.testApi.sentiment_model')
    @patch('Day14.testApi.summarizer_model')
    def test_both_endpoints_work_independently(self, mock_summarizer, mock_sentiment):
        """Test that both endpoints can be used independently"""
        # Mock responses
        mock_sentiment.return_value = [{'label': 'POSITIVE', 'score': 0.95}]
        mock_summarizer.return_value = [{'summary_text': 'Independent test summary'}]
        
        test_text = "This is a test message for both endpoints."
        test_data = {"text": test_text}
        
        # Test sentiment endpoint
        sentiment_response = self.client.post("/sentiment", json=test_data)
        self.assertEqual(sentiment_response.status_code, 200)
        
        # Test summary endpoint
        summary_response = self.client.post("/summary", json=test_data)
        self.assertEqual(summary_response.status_code, 200)
        
        # Verify both were called
        mock_sentiment.assert_called_once_with(test_text)
        mock_summarizer.assert_called_once()
    
    def test_fastapi_app_configuration(self):
        """Test that FastAPI app is configured with correct title"""
        from Day14.testApi import app
        
        self.assertEqual(app.title, "Text Analysis API")
    
    @patch('Day14.testApi.sentiment_model')
    def test_async_sentiment_endpoint(self, mock_sentiment):
        """Test that async sentiment endpoint works correctly"""
        # Mock the sentiment model response
        mock_sentiment.return_value = [{'label': 'POSITIVE', 'score': 0.9234}]
        
        test_data = {"text": "Async sentiment test"}
        response = self.client.post("/sentiment", json=test_data)
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["input"], "Async sentiment test")
    
    @patch('Day14.testApi.summarizer_model')
    def test_async_summary_endpoint(self, mock_summarizer):
        """Test that async summary endpoint works correctly"""
        # Mock the summarizer model response
        mock_summarizer.return_value = [{'summary_text': 'Async summary test'}]
        
        test_data = {"text": "Long text for async summarization testing. " * 10}
        response = self.client.post("/summary", json=test_data)
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["summary"], "Async summary test")
    
    def test_cors_origins_configuration(self):
        """Test that CORS origins are configured correctly"""
        # Import to check the origins configuration
        from Day14.testApi import origins
        
        # Should allow all origins as configured
        self.assertEqual(origins, ["*"])
    
    @patch('Day14.testApi.sentiment_model')
    @patch('Day14.testApi.summarizer_model')
    def test_long_text_handling_both_endpoints(self, mock_summarizer, mock_sentiment):
        """Test handling of long text in both endpoints"""
        # Mock responses
        mock_sentiment.return_value = [{'label': 'NEUTRAL', 'score': 0.6}]
        mock_summarizer.return_value = [{'summary_text': 'Long text summary'}]
        
        # Create a very long text
        long_text = "This is a very long text message that should be handled properly by both endpoints. " * 100
        test_data = {"text": long_text}
        
        # Test both endpoints with long text
        sentiment_response = self.client.post("/sentiment", json=test_data)
        self.assertEqual(sentiment_response.status_code, 200)
        
        summary_response = self.client.post("/summary", json=test_data)
        self.assertEqual(summary_response.status_code, 200)
    
    @patch('Day14.testApi.pipeline')
    def test_pipeline_initialization(self, mock_pipeline):
        """Test that both pipelines are initialized correctly during import"""
        # Reset the mock to track calls during import
        mock_pipeline.reset_mock()
        
        # Re-import the module to trigger pipeline initialization
        import importlib
        if 'Day14.testApi' in sys.modules:
            importlib.reload(sys.modules['Day14.testApi'])
        else:
            import Day14.testApi
        
        # Verify both pipelines were created
        expected_calls = [
            unittest.mock.call("sentiment-analysis"),
            unittest.mock.call("summarization")
        ]
        
        # Check that pipeline was called for both tasks (order may vary)
        self.assertEqual(mock_pipeline.call_count, 2)
        calls_made = [call[0][0] for call in mock_pipeline.call_args_list]
        self.assertIn("sentiment-analysis", calls_made)
        self.assertIn("summarization", calls_made)

if __name__ == "__main__":
    unittest.main()