import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestDay9(unittest.TestCase):
    
    @patch('Day9.summarizer.pipeline')
    def test_summarizer_pipeline_initialization(self, mock_pipeline):
        """Test that summarizer pipeline initializes correctly"""
        mock_summarizer = MagicMock()
        mock_pipeline.return_value = mock_summarizer
        
        # Import the module (this will execute the pipeline creation)
        try:
            import Day9.summarizer
            initialization_successful = True
        except Exception:
            initialization_successful = False
        
        self.assertTrue(initialization_successful)
        mock_pipeline.assert_called_with("summarization", model="facebook/bart-large-cnn")
    
    @patch('Day9.summarizer.pipeline')
    def test_summarizer_produces_output(self, mock_pipeline):
        """Test that summarizer produces expected output format"""
        # Mock the summarizer to return expected format
        mock_summarizer = MagicMock()
        mock_summarizer.return_value = [{'summary_text': 'Apollo program landed first humans on Moon from 1969 to 1972. It was managed by NASA and used Saturn family rockets.'}]
        mock_pipeline.return_value = mock_summarizer
        
        # Import and execute
        import Day9.summarizer
        
        # Verify the summarizer was called with expected parameters
        expected_call_args = (
            Day9.summarizer.article_text,
        )
        expected_call_kwargs = {
            'max_length': 60,
            'min_length': 30,
            'do_sample': False
        }
        
        mock_summarizer.assert_called_with(*expected_call_args, **expected_call_kwargs)
    
    def test_article_text_is_not_empty(self):
        """Test that the article text is properly defined"""
        import Day9.summarizer
        
        self.assertIsInstance(Day9.summarizer.article_text, str)
        self.assertGreater(len(Day9.summarizer.article_text.strip()), 0)
        self.assertIn("Apollo", Day9.summarizer.article_text)
    
    @patch('Day9.summarizer.pipeline')
    @patch('builtins.print')
    def test_summarizer_output_format(self, mock_print, mock_pipeline):
        """Test that the output is printed in the expected format"""
        # Mock the summarizer
        mock_summarizer = MagicMock()
        expected_summary = "Apollo program landed humans on Moon. It used Saturn rockets."
        mock_summarizer.return_value = [{'summary_text': expected_summary}]
        mock_pipeline.return_value = mock_summarizer
        
        # Import the module to execute it
        import Day9.summarizer
        
        # Verify print was called (output was generated)
        self.assertTrue(mock_print.called)
        
        # Check that summary text is in one of the print calls
        print_calls = [call[0] for call in mock_print.call_args_list]
        summary_found = any(expected_summary in str(call) for call in print_calls)
        self.assertTrue(summary_found)
    
    def test_day9_module_imports_correctly(self):
        """Test that Day9 module imports without errors"""
        try:
            import Day9.summarizer
            import_successful = True
        except ImportError:
            import_successful = False
        
        self.assertTrue(import_successful)
    
    @patch('Day9.summarizer.pipeline')
    def test_summarizer_handles_text_processing(self, mock_pipeline):
        """Test that summarizer can handle text processing parameters"""
        mock_summarizer = MagicMock()
        mock_summarizer.return_value = [{'summary_text': 'Test summary'}]
        mock_pipeline.return_value = mock_summarizer
        
        import Day9.summarizer
        
        # Verify the call included proper parameters for text length control
        call_args, call_kwargs = mock_summarizer.call_args
        self.assertIn('max_length', call_kwargs)
        self.assertIn('min_length', call_kwargs)
        self.assertIn('do_sample', call_kwargs)
        self.assertEqual(call_kwargs['max_length'], 60)
        self.assertEqual(call_kwargs['min_length'], 30)
        self.assertEqual(call_kwargs['do_sample'], False)

if __name__ == "__main__":
    unittest.main()