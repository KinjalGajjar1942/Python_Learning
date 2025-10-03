import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestDay11(unittest.TestCase):
    
    @patch('Day11.benchmark_models.pipeline')
    def test_pipeline_initialization(self, mock_pipeline):
        """Test that both pipelines initialize correctly"""
        mock_distilbert = MagicMock()
        mock_bert = MagicMock()
        
        # Configure mock to return different pipelines for different models
        def pipeline_side_effect(task, model):
            if "distilbert" in model:
                return mock_distilbert
            elif "bert" in model:
                return mock_bert
            return MagicMock()
        
        mock_pipeline.side_effect = pipeline_side_effect
        
        # Import the module to trigger pipeline creation
        import Day11.benchmark_models
        
        # Verify both pipelines were created
        self.assertEqual(mock_pipeline.call_count, 2)
    
    @patch('Day11.benchmark_models.measure_inference')
    @patch('Day11.benchmark_models.pipeline')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_benchmark_execution_and_logging(self, mock_json_dump, mock_file, mock_pipeline, mock_measure):
        """Test that benchmark runs and logs results correctly"""
        # Mock measure_inference to return predictable results
        mock_measure.side_effect = [
            (2.5, [{'label': 'POSITIVE', 'score': 0.99}] * 50),  # DistilBERT results
            (5.0, [{'label': 'NEGATIVE', 'score': 0.95}] * 50)   # BERT results
        ]
        
        mock_pipeline.return_value = MagicMock()
        
        # Import and execute
        import Day11.benchmark_models
        
        # Verify measure_inference was called twice
        self.assertEqual(mock_measure.call_count, 2)
        
        # Verify JSON dump was called
        mock_json_dump.assert_called_once()
        
        # Check the structure of logged data
        logged_data = mock_json_dump.call_args[0][0]
        self.assertIn('num_sentences', logged_data)
        self.assertIn('distilbert_time_sec', logged_data)
        self.assertIn('bert_time_sec', logged_data)
        self.assertIn('distilbert_results', logged_data)
        self.assertIn('bert_results', logged_data)
    
    def test_sentences_generation(self):
        """Test that sentences are generated correctly"""
        import Day11.benchmark_models
        
        sentences = Day11.benchmark_models.sentences
        
        # Verify we have 50 sentences
        self.assertEqual(len(sentences), 50)
        
        # Verify sentence format
        for i, sentence in enumerate(sentences, 1):
            self.assertIn(f"sentence number {i}", sentence)
            self.assertIn("I love testing models!", sentence)
    
    @patch('Day11.benchmark_models.time.time')
    @patch('Day11.benchmark_models.pipeline')
    def test_measure_inference_timing(self, mock_pipeline, mock_time):
        """Test that measure_inference correctly measures timing"""
        from Day11.benchmark_models import measure_inference
        
        # Mock time.time to return predictable values
        mock_time.side_effect = [10.0, 15.0]  # 5 second difference
        
        # Mock pipeline
        mock_pipeline_instance = MagicMock()
        mock_results = [{'label': 'POSITIVE', 'score': 0.99}]
        mock_pipeline_instance.return_value = mock_results
        
        # Test sentences
        test_sentences = ["Test sentence 1", "Test sentence 2"]
        
        # Call measure_inference
        elapsed_time, results = measure_inference(mock_pipeline_instance, test_sentences)
        
        # Verify timing calculation
        self.assertEqual(elapsed_time, 5.0)
        self.assertEqual(results, mock_results)
        mock_pipeline_instance.assert_called_once_with(test_sentences)
    
    @patch('Day11.benchmark_models.pipeline')
    def test_pipeline_model_names(self, mock_pipeline):
        """Test that correct model names are used for pipelines"""
        mock_pipeline.return_value = MagicMock()
        
        # Import the module
        import Day11.benchmark_models
        
        # Verify pipeline was called with correct models
        expected_calls = [
            unittest.mock.call("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english"),
            unittest.mock.call("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
        ]
        
        mock_pipeline.assert_has_calls(expected_calls, any_order=True)
    
    def test_day11_module_imports_correctly(self):
        """Test that Day11 module imports without errors"""
        try:
            import Day11.benchmark_models
            import_successful = True
        except ImportError:
            import_successful = False
        
        self.assertTrue(import_successful)
    
    @patch('Day11.benchmark_models.measure_inference')
    @patch('Day11.benchmark_models.pipeline')
    @patch('builtins.print')
    def test_performance_reporting(self, mock_print, mock_pipeline, mock_measure):
        """Test that performance results are printed correctly"""
        # Mock measure_inference results
        mock_measure.side_effect = [
            (1.5, []),  # DistilBERT faster
            (3.2, [])   # BERT slower
        ]
        
        mock_pipeline.return_value = MagicMock()
        
        # Import and execute
        import Day11.benchmark_models
        
        # Verify print statements were made about timing
        print_calls = [str(call) for call in mock_print.call_args_list]
        timing_prints = [call for call in print_calls if 'took' in call and 'seconds' in call]
        
        # Should have printed timing for both models
        self.assertGreaterEqual(len(timing_prints), 2)
    
    @patch('Day11.benchmark_models.pipeline')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_json_file_creation(self, mock_json_dump, mock_file, mock_pipeline):
        """Test that JSON results file is created with correct name"""
        mock_pipeline.return_value = MagicMock()
        
        # Import and execute
        import Day11.benchmark_models
        
        # Verify file was opened with correct name
        mock_file.assert_called_with("benchmark_results.json", "w")
        
        # Verify JSON dump was called
        mock_json_dump.assert_called_once()

if __name__ == "__main__":
    unittest.main()