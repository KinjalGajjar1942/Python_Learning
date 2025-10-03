import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestDay12(unittest.TestCase):
    
    @patch('Day12.imdb_exmple.load_dataset')
    @patch('Day12.imdb_exmple.pipeline')
    @patch('Day12.imdb_exmple.random.sample')
    @patch('builtins.print')
    def test_imdb_analysis_workflow(self, mock_print, mock_sample, mock_pipeline, mock_load_dataset):
        """Test the complete IMDB analysis workflow"""
        # Mock dataset
        mock_dataset = MagicMock()
        mock_test_data = [
            {"text": "This movie is absolutely fantastic! Great acting and plot.", "label": 1},
            {"text": "Terrible movie, waste of time. Poor acting and boring story.", "label": 0},
            {"text": "An okay film, not great but not terrible either.", "label": 1},
            {"text": "Loved every minute of it! Highly recommended.", "label": 1},
            {"text": "Could not finish watching. Very disappointing.", "label": 0}
        ]
        mock_dataset.__getitem__.return_value = mock_test_data
        mock_load_dataset.return_value = mock_dataset
        
        # Mock random sample
        mock_sample.return_value = mock_test_data
        
        # Mock sentiment pipeline
        mock_sentiment = MagicMock()
        mock_sentiment.side_effect = [
            [{"label": "POSITIVE", "score": 0.9956}],
            [{"label": "NEGATIVE", "score": 0.9821}],
            [{"label": "POSITIVE", "score": 0.6234}],
            [{"label": "POSITIVE", "score": 0.9876}],
            [{"label": "NEGATIVE", "score": 0.8765}]
        ]
        mock_pipeline.return_value = mock_sentiment
        
        # Import and execute the module
        import Day12.imdb_exmple
        
        # Verify load_dataset was called
        mock_load_dataset.assert_called_once_with("imdb")
        
        # Verify random.sample was called
        mock_sample.assert_called_once()
        
        # Verify pipeline was created
        mock_pipeline.assert_called_once_with("sentiment-analysis")
        
        # Verify sentiment analysis was performed on all samples
        self.assertEqual(mock_sentiment.call_count, 5)
        
        # Verify output was printed
        self.assertTrue(mock_print.called)
    
    @patch('Day12.imdb_exmple.load_dataset')
    def test_dataset_loading(self, mock_load_dataset):
        """Test that IMDB dataset is loaded correctly"""
        mock_dataset = MagicMock()
        mock_load_dataset.return_value = mock_dataset
        
        # Import module to trigger dataset loading
        import Day12.imdb_exmple
        
        # Verify dataset was loaded with correct name
        mock_load_dataset.assert_called_once_with("imdb")
        
        # Verify test split was accessed
        mock_dataset.__getitem__.assert_called_with("test")
    
    @patch('Day12.imdb_exmple.random.sample')
    def test_random_sampling(self, mock_sample):
        """Test that random sampling selects 5 reviews"""
        mock_sample.return_value = []
        
        # Import module to trigger sampling
        with patch('Day12.imdb_exmple.load_dataset') as mock_load_dataset:
            mock_dataset = MagicMock()
            mock_test_list = ["review1", "review2", "review3"] * 100  # Simulate large dataset
            mock_dataset.__getitem__.return_value = mock_test_list
            mock_load_dataset.return_value = mock_dataset
            
            with patch('Day12.imdb_exmple.pipeline'):
                import Day12.imdb_exmple
        
        # Verify sample was called with correct parameters
        mock_sample.assert_called_once()
        call_args = mock_sample.call_args
        self.assertEqual(call_args[0][1], 5)  # Second argument should be 5 (sample size)
    
    @patch('Day12.imdb_exmple.pipeline')
    def test_text_truncation(self, mock_pipeline):
        """Test that long text is truncated to 512 characters"""
        # Mock sentiment pipeline
        mock_sentiment = MagicMock()
        mock_sentiment.return_value = [{"label": "POSITIVE", "score": 0.95}]
        mock_pipeline.return_value = mock_sentiment
        
        # Create a long review text
        long_text = "This is a very long review. " * 50  # Creates text > 512 chars
        
        with patch('Day12.imdb_exmple.load_dataset') as mock_load_dataset:
            with patch('Day12.imdb_exmple.random.sample') as mock_sample:
                mock_dataset = MagicMock()
                mock_load_dataset.return_value = mock_dataset
                mock_sample.return_value = [{"text": long_text, "label": 1}]
                
                # Import module to execute
                import Day12.imdb_exmple
        
        # Verify sentiment was called with truncated text
        mock_sentiment.assert_called_once()
        call_args = mock_sentiment.call_args[0][0]
        self.assertEqual(len(call_args), 512)  # Should be truncated to 512 chars
    
    @patch('Day12.imdb_exmple.load_dataset')
    @patch('Day12.imdb_exmple.pipeline')
    @patch('Day12.imdb_exmple.random.sample')
    @patch('builtins.print')
    def test_output_format(self, mock_print, mock_sample, mock_pipeline, mock_load_dataset):
        """Test that output is formatted correctly"""
        # Setup mocks
        mock_dataset = MagicMock()
        mock_load_dataset.return_value = mock_dataset
        
        mock_sample.return_value = [
            {"text": "Great movie!", "label": 1}
        ]
        
        mock_sentiment = MagicMock()
        mock_sentiment.return_value = [{"label": "POSITIVE", "score": 0.9956}]
        mock_pipeline.return_value = mock_sentiment
        
        # Import and execute
        import Day12.imdb_exmple
        
        # Check that print was called multiple times (for formatting)
        self.assertTrue(mock_print.called)
        
        # Verify specific format elements are printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        
        # Should contain review numbers, text preview, and sentiment results
        review_number_found = any("Review" in call for call in print_calls)
        text_found = any("Text:" in call for call in print_calls)
        sentiment_found = any("Predicted Sentiment:" in call for call in print_calls)
        
        self.assertTrue(review_number_found)
        self.assertTrue(text_found)
        self.assertTrue(sentiment_found)
    
    def test_day12_module_imports_correctly(self):
        """Test that Day12 module imports without errors"""
        try:
            # Need to mock dependencies for import to succeed
            with patch('Day12.imdb_exmple.load_dataset'):
                with patch('Day12.imdb_exmple.pipeline'):
                    with patch('Day12.imdb_exmple.random.sample'):
                        import Day12.imdb_exmple
            import_successful = True
        except ImportError:
            import_successful = False
        
        self.assertTrue(import_successful)
    
    @patch('Day12.imdb_exmple.load_dataset')
    @patch('Day12.imdb_exmple.pipeline')
    @patch('Day12.imdb_exmple.random.sample')
    def test_sentiment_pipeline_initialization(self, mock_sample, mock_pipeline, mock_load_dataset):
        """Test that sentiment pipeline is initialized correctly"""
        # Setup mocks
        mock_dataset = MagicMock()
        mock_load_dataset.return_value = mock_dataset
        mock_sample.return_value = []
        mock_pipeline.return_value = MagicMock()
        
        # Import module
        import Day12.imdb_exmple
        
        # Verify pipeline was created with correct task
        mock_pipeline.assert_called_once_with("sentiment-analysis")
    
    @patch('Day12.imdb_exmple.load_dataset')
    @patch('Day12.imdb_exmple.pipeline')
    @patch('Day12.imdb_exmple.random.sample')
    def test_handles_empty_reviews(self, mock_sample, mock_pipeline, mock_load_dataset):
        """Test handling of edge cases like empty reviews"""
        # Setup mocks
        mock_dataset = MagicMock()
        mock_load_dataset.return_value = mock_dataset
        
        # Include an empty text review
        mock_sample.return_value = [
            {"text": "", "label": 1},
            {"text": "Normal review text", "label": 0}
        ]
        
        mock_sentiment = MagicMock()
        mock_sentiment.return_value = [{"label": "NEUTRAL", "score": 0.5}]
        mock_pipeline.return_value = mock_sentiment
        
        # Should not raise an exception
        try:
            import Day12.imdb_exmple
            execution_successful = True
        except Exception:
            execution_successful = False
        
        self.assertTrue(execution_successful)

if __name__ == "__main__":
    unittest.main()