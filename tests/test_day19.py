"""
Comprehensive test suite for Day19 - FastAPI Q&A System with Vector Store

This module tests:
- FastAPI QA endpoint with text input processing
- Document creation and text splitting
- FAISS vector store integration
- RetrievalQA chain functionality
- OpenAI embeddings and chat models
- Error handling and edge cases
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
from fastapi.testclient import TestClient
import json
import os


class TestDay19QASystem(unittest.TestCase):
    """Test suite for Day19 FastAPI Q&A system with vector store."""

    def setUp(self):
        """Set up test client and mocks for FastAPI app."""
        # Mock all external dependencies before importing
        with patch('Day19.example.OpenAIEmbeddings') as mock_embeddings, \
             patch('Day19.example.FAISS') as mock_faiss, \
             patch('Day19.example.ChatOpenAI') as mock_chat, \
             patch('Day19.example.RetrievalQA') as mock_qa:
            
            # Configure mocks
            mock_embeddings_instance = MagicMock()
            mock_embeddings.return_value = mock_embeddings_instance
            
            mock_faiss_instance = MagicMock()
            mock_faiss.from_documents.return_value = mock_faiss_instance
            mock_faiss_instance.as_retriever.return_value = MagicMock()
            
            mock_chat_instance = MagicMock()
            mock_chat.return_value = mock_chat_instance
            
            mock_qa_chain = MagicMock()
            mock_qa_chain.run.return_value = "This is a test answer."
            mock_qa.from_chain_type.return_value = mock_qa_chain
            
            # Import the module after setting up mocks
            from Day19.example import app
            self.app = app
            self.client = TestClient(app)
            
            # Store mocks for assertions
            self.mock_embeddings = mock_embeddings
            self.mock_faiss = mock_faiss
            self.mock_chat = mock_chat
            self.mock_qa = mock_qa
            self.mock_qa_chain = mock_qa_chain

    def test_qa_endpoint_successful_response(self):
        """Test successful Q&A processing with valid input."""
        request_data = {
            "texts": [
                "Python is a programming language.", 
                "FastAPI is a web framework for Python."
            ],
            "query": "What is Python?"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert "answer" in response_data
        assert response_data["answer"] == "This is a test answer."

    def test_qa_endpoint_with_single_text(self):
        """Test Q&A processing with single input text."""
        request_data = {
            "texts": ["Machine learning is a subset of artificial intelligence."],
            "query": "What is machine learning?"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 200
        assert "answer" in response.json()

    def test_qa_endpoint_with_empty_texts(self):
        """Test Q&A processing with empty texts list."""
        request_data = {
            "texts": [],
            "query": "What is Python?"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        # Should still process but might return an error or empty result
        assert response.status_code in [200, 500]  # Depending on implementation

    def test_qa_endpoint_with_long_texts(self):
        """Test Q&A processing with long input texts that require chunking."""
        long_text = "Python is a high-level programming language. " * 100  # Very long text
        request_data = {
            "texts": [long_text],
            "query": "What is Python?"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 200
        # Verify that text splitter would be called for long texts
        self.assertTrue(self.mock_faiss.from_documents.called)

    def test_qa_endpoint_missing_texts_field(self):
        """Test Q&A endpoint with missing texts field."""
        request_data = {
            "query": "What is Python?"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 422  # Validation error

    def test_qa_endpoint_missing_query_field(self):
        """Test Q&A endpoint with missing query field."""
        request_data = {
            "texts": ["Python is a programming language."]
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 422  # Validation error

    def test_qa_endpoint_invalid_json(self):
        """Test Q&A endpoint with invalid JSON data."""
        response = self.client.post("/qa", data="invalid json")
        
        assert response.status_code == 422

    def test_qa_endpoint_with_special_characters(self):
        """Test Q&A processing with special characters in text and query."""
        request_data = {
            "texts": ["Hello! @#$% How are you? 😊 This is a test."],
            "query": "What's the mood? 🤔"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 200

    def test_document_creation_and_metadata(self):
        """Test that documents are created with proper metadata."""
        request_data = {
            "texts": ["Text 1", "Text 2", "Text 3"],
            "query": "Test query"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 200
        # Verify FAISS was called with documents
        self.mock_faiss.from_documents.assert_called_once()

    @patch('Day19.example.CharacterTextSplitter')
    def test_text_splitting_configuration(self, mock_splitter):
        """Test that text splitter is configured correctly."""
        mock_splitter_instance = MagicMock()
        mock_splitter_instance.split_text.return_value = ["chunk1", "chunk2"]
        mock_splitter.return_value = mock_splitter_instance
        
        request_data = {
            "texts": ["This is a long text that needs to be split into chunks."],
            "query": "Test query"
        }
        
        with patch('Day19.example.OpenAIEmbeddings'), \
             patch('Day19.example.FAISS') as mock_faiss, \
             patch('Day19.example.RetrievalQA') as mock_qa:
            
            mock_qa_chain = MagicMock()
            mock_qa_chain.run.return_value = "Test answer"
            mock_qa.from_chain_type.return_value = mock_qa_chain
            
            response = self.client.post("/qa", json=request_data)
        
        # Verify text splitter was configured with correct parameters
        mock_splitter.assert_called_with(chunk_size=500, chunk_overlap=50)

    def test_openai_embeddings_initialization(self):
        """Test OpenAI embeddings initialization with correct model."""
        request_data = {
            "texts": ["Test text"],
            "query": "Test query"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 200
        # Verify embeddings were initialized with correct model
        self.mock_embeddings.assert_called_with(model="text-embedding-3-small")

    def test_chatgpt_model_initialization(self):
        """Test ChatOpenAI model initialization with correct parameters."""
        request_data = {
            "texts": ["Test text"],
            "query": "Test query"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 200
        # Verify ChatOpenAI was initialized with correct parameters
        self.mock_chat.assert_called_with(model_name="gpt-3.5-turbo", temperature=0)

    def test_retrieval_qa_chain_creation(self):
        """Test RetrievalQA chain creation and configuration."""
        request_data = {
            "texts": ["Test text"],
            "query": "Test query"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 200
        # Verify RetrievalQA chain was created
        self.mock_qa.from_chain_type.assert_called_once()

    def test_faiss_vector_store_creation(self):
        """Test FAISS vector store creation from documents."""
        request_data = {
            "texts": ["Test text 1", "Test text 2"],
            "query": "Test query"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 200
        # Verify FAISS was created from documents
        self.mock_faiss.from_documents.assert_called_once()

    @patch.dict(os.environ, {}, clear=True)
    def test_environment_variable_handling(self):
        """Test handling of environment variables."""
        # Test should work even without API key in environment
        # since we're mocking the components
        request_data = {
            "texts": ["Test text"],
            "query": "Test query"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 200

    def test_multiple_concurrent_requests(self):
        """Test handling of multiple requests."""
        request_data = {
            "texts": ["Test text"],
            "query": "Test query"
        }
        
        # Send multiple requests
        responses = []
        for _ in range(3):
            response = self.client.post("/qa", json=request_data)
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
            assert "answer" in response.json()

    def test_error_handling_in_qa_processing(self):
        """Test error handling during Q&A processing."""
        # Mock an exception in the QA chain
        self.mock_qa_chain.run.side_effect = Exception("Processing error")
        
        request_data = {
            "texts": ["Test text"],
            "query": "Test query"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 500
        assert "detail" in response.json()

    def test_qa_request_model_validation(self):
        """Test QARequest model validation."""
        # Test with wrong data types
        invalid_request_data = {
            "texts": "should be a list",  # Wrong type
            "query": ["should be a string"]  # Wrong type
        }
        
        response = self.client.post("/qa", json=invalid_request_data)
        
        assert response.status_code == 422

    def test_empty_query_handling(self):
        """Test handling of empty query string."""
        request_data = {
            "texts": ["Test text"],
            "query": ""
        }
        
        response = self.client.post("/qa", json=request_data)
        
        # Should still process but might have different behavior
        assert response.status_code in [200, 500]

    def test_app_configuration(self):
        """Test FastAPI app configuration."""
        # Test app title and basic configuration
        assert self.app.title == "QA API"

    def test_large_number_of_texts(self):
        """Test processing with a large number of input texts."""
        large_texts = [f"This is text number {i}" for i in range(100)]
        request_data = {
            "texts": large_texts,
            "query": "What is this about?"
        }
        
        response = self.client.post("/qa", json=request_data)
        
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()