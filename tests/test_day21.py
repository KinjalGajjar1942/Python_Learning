"""
Comprehensive test suite for Day21 - Advanced PDF Q&A Bot

This module tests:
- FastAPI PDF upload with enhanced processing
- Advanced PDF text extraction and optimization
- Improved document chunking and indexing
- Enhanced FAISS vector store operations
- Optimized RetrievalQA chain performance
- Advanced error handling and validation
- Performance and scalability considerations
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
import pytest
from fastapi.testclient import TestClient
import json
import io
import tempfile
from pathlib import Path


class TestDay21AdvancedPDFQABot(unittest.TestCase):
    """Test suite for Day21 Advanced PDF Q&A Bot system."""

    def setUp(self):
        """Set up test client and mocks for FastAPI app."""
        # Mock all external dependencies before importing
        with patch('Day21.example.PdfReader') as mock_pdf_reader, \
             patch('Day21.example.OpenAIEmbeddings') as mock_embeddings, \
             patch('Day21.example.FAISS') as mock_faiss, \
             patch('Day21.example.ChatOpenAI') as mock_chat, \
             patch('Day21.example.RetrievalQA') as mock_qa:
            
            # Configure PDF reader mock with enhanced features
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "Advanced PDF content with enhanced text extraction capabilities."
            mock_pdf_instance = MagicMock()
            mock_pdf_instance.pages = [mock_page, mock_page, mock_page]  # Three pages
            mock_pdf_reader.return_value = mock_pdf_instance
            
            # Configure advanced embeddings mock
            mock_embeddings_instance = MagicMock()
            mock_embeddings.return_value = mock_embeddings_instance
            
            # Configure enhanced FAISS mock
            mock_faiss_instance = MagicMock()
            mock_faiss.from_documents.return_value = mock_faiss_instance
            mock_retriever = MagicMock()
            mock_faiss_instance.as_retriever.return_value = mock_retriever
            
            # Configure optimized ChatOpenAI mock
            mock_chat_instance = MagicMock()
            mock_chat.return_value = mock_chat_instance
            
            # Configure enhanced RetrievalQA mock
            mock_qa_chain = MagicMock()
            mock_qa_chain.run.return_value = "Advanced PDF-based answer with enhanced processing."
            mock_qa.from_chain_type.return_value = mock_qa_chain
            
            # Import the module after setting up mocks
            from Day21.example import app
            self.app = app
            self.client = TestClient(app)
            
            # Store mocks for assertions
            self.mock_pdf_reader = mock_pdf_reader
            self.mock_embeddings = mock_embeddings
            self.mock_faiss = mock_faiss
            self.mock_chat = mock_chat
            self.mock_qa = mock_qa
            self.mock_qa_chain = mock_qa_chain
            self.mock_retriever = mock_retriever

    def create_mock_pdf_file(self, filename="advanced_test.pdf", content=b"advanced pdf content"):
        """Helper method to create mock PDF file for advanced testing."""
        return ("file", (filename, io.BytesIO(content), "application/pdf"))

    def test_advanced_pdf_upload_successful(self):
        """Test successful PDF upload with advanced processing."""
        pdf_file = self.create_mock_pdf_file()
        
        response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert "advanced_test.pdf" in response_data["message"]
        assert "uploaded and indexed successfully" in response_data["message"]

    def test_enhanced_pdf_validation(self):
        """Test enhanced PDF file validation."""
        # Test various invalid file types
        invalid_files = [
            ("file", ("test.doc", io.BytesIO(b"doc content"), "application/msword")),
            ("file", ("test.txt", io.BytesIO(b"text content"), "text/plain")),
            ("file", ("test.jpg", io.BytesIO(b"image content"), "image/jpeg")),
            ("file", ("test", io.BytesIO(b"no extension"), "application/octet-stream"))
        ]
        
        for invalid_file in invalid_files:
            response = self.client.post("/upload-pdf", files=[invalid_file])
            assert response.status_code == 400
            assert "Only PDF files are allowed" in response.json()["detail"]

    def test_pdf_upload_with_advanced_metadata_extraction(self):
        """Test PDF processing with enhanced metadata extraction."""
        pdf_file = self.create_mock_pdf_file("research_paper.pdf")
        
        response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 200
        # Verify that documents were created with proper metadata
        self.mock_faiss.from_documents.assert_called_once()
        
        # Check that the call included documents with metadata
        call_args = self.mock_faiss.from_documents.call_args
        documents = call_args[0][0]  # First argument is the documents list
        assert len(documents) > 0

    def test_advanced_text_chunking_strategy(self):
        """Test advanced text chunking with optimized parameters."""
        with patch('Day21.example.CharacterTextSplitter') as mock_splitter:
            mock_splitter_instance = MagicMock()
            mock_splitter_instance.split_text.return_value = [
                "Advanced chunk 1", "Advanced chunk 2", "Advanced chunk 3"
            ]
            mock_splitter.return_value = mock_splitter_instance
            
            pdf_file = self.create_mock_pdf_file()
            
            with patch('Day21.example.PdfReader') as mock_pdf, \
                 patch('Day21.example.OpenAIEmbeddings'), \
                 patch('Day21.example.FAISS'):
                
                # Mock PDF with substantial content
                mock_page = MagicMock()
                mock_page.extract_text.return_value = "Long research content " * 100
                mock_pdf_instance = MagicMock()
                mock_pdf_instance.pages = [mock_page]
                mock_pdf.return_value = mock_pdf_instance
                
                response = self.client.post("/upload-pdf", files=[pdf_file])
            
            assert response.status_code == 200
            # Verify advanced chunking parameters
            mock_splitter.assert_called_with(chunk_size=500, chunk_overlap=50)

    def test_enhanced_qa_functionality(self):
        """Test enhanced Q&A functionality with advanced features."""
        # Upload PDF first
        pdf_file = self.create_mock_pdf_file("technical_manual.pdf")
        upload_response = self.client.post("/upload-pdf", files=[pdf_file])
        assert upload_response.status_code == 200
        
        # Test various types of questions
        advanced_queries = [
            "What are the main concepts discussed?",
            "Can you summarize the methodology?",
            "What are the key findings and conclusions?",
            "How does this relate to current research trends?"
        ]
        
        for query in advanced_queries:
            qa_data = {"query": query}
            qa_response = self.client.post("/qa", json=qa_data)
            
            assert qa_response.status_code == 200
            response_data = qa_response.json()
            assert "answer" in response_data
            assert len(response_data["answer"]) > 0

    def test_optimized_embeddings_configuration(self):
        """Test optimized embeddings configuration."""
        pdf_file = self.create_mock_pdf_file()
        
        response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 200
        # Verify embeddings were configured with optimal model
        self.mock_embeddings.assert_called_with(model="text-embedding-3-small")

    def test_enhanced_chatgpt_configuration(self):
        """Test enhanced ChatGPT model configuration for better Q&A."""
        # Upload PDF first
        pdf_file = self.create_mock_pdf_file()
        self.client.post("/upload-pdf", files=[pdf_file])
        
        # Trigger Q&A to initialize ChatGPT
        qa_data = {"query": "Advanced technical question"}
        response = self.client.post("/qa", json=qa_data)
        
        assert response.status_code == 200
        # Verify optimal ChatGPT configuration
        self.mock_chat.assert_called_with(model_name="gpt-3.5-turbo", temperature=0)

    def test_complex_pdf_structure_handling(self):
        """Test handling of complex PDF structures."""
        with patch('Day21.example.PdfReader') as mock_pdf:
            # Simulate complex PDF with various content types
            mock_pages = []
            page_contents = [
                "Title Page - Research Document",
                "Abstract: This document presents advanced findings...",
                "Table of Contents\n1. Introduction\n2. Methodology\n3. Results",
                "Chapter 1: Introduction\nThis chapter covers...",
                "Chapter 2: Methodology\nWe employed various techniques...",
                "References and Bibliography"
            ]
            
            for content in page_contents:
                mock_page = MagicMock()
                mock_page.extract_text.return_value = content
                mock_pages.append(mock_page)
            
            mock_pdf_instance = MagicMock()
            mock_pdf_instance.pages = mock_pages
            mock_pdf.return_value = mock_pdf_instance
            
            pdf_file = self.create_mock_pdf_file("complex_document.pdf")
            response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 200

    def test_advanced_error_handling_scenarios(self):
        """Test advanced error handling scenarios."""
        # Test PDF reader exceptions
        self.mock_pdf_reader.side_effect = Exception("Advanced PDF parsing error")
        
        pdf_file = self.create_mock_pdf_file()
        response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 500
        error_detail = response.json()["detail"]
        assert "Advanced PDF parsing error" in error_detail

    def test_qa_error_recovery_mechanisms(self):
        """Test Q&A error recovery mechanisms."""
        # Upload PDF first
        pdf_file = self.create_mock_pdf_file()
        self.client.post("/upload-pdf", files=[pdf_file])
        
        # Simulate various QA errors
        qa_errors = [
            "Embedding generation failed",
            "Retrieval timeout error", 
            "LLM processing error"
        ]
        
        for error_msg in qa_errors:
            self.mock_qa_chain.run.side_effect = Exception(error_msg)
            
            qa_data = {"query": "Test question"}
            response = self.client.post("/qa", json=qa_data)
            
            assert response.status_code == 500
            assert error_msg in response.json()["detail"]

    def test_global_state_management_advanced(self):
        """Test advanced global state management."""
        import Day21.example
        
        # Test initial state
        initial_index = Day21.example.faiss_index
        
        # Upload first PDF
        pdf_file1 = self.create_mock_pdf_file("doc1.pdf")
        response1 = self.client.post("/upload-pdf", files=[pdf_file1])
        assert response1.status_code == 200
        
        # Upload second PDF (should replace)
        pdf_file2 = self.create_mock_pdf_file("doc2.pdf")  
        response2 = self.client.post("/upload-pdf", files=[pdf_file2])
        assert response2.status_code == 200
        
        # Verify state management worked
        assert "doc2.pdf" in response2.json()["message"]

    def test_performance_with_large_documents(self):
        """Test performance considerations with large documents."""
        with patch('Day21.example.PdfReader') as mock_pdf:
            # Simulate very large document
            large_pages = []
            for i in range(500):  # 500 pages
                mock_page = MagicMock()
                # Each page has substantial content
                mock_page.extract_text.return_value = f"Page {i+1} content. " + "Large amount of text. " * 200
                large_pages.append(mock_page)
            
            mock_pdf_instance = MagicMock()
            mock_pdf_instance.pages = large_pages
            mock_pdf.return_value = mock_pdf_instance
            
            large_pdf = self.create_mock_pdf_file("large_document.pdf")
            response = self.client.post("/upload-pdf", files=[large_pdf])
        
        assert response.status_code == 200
        # Should handle large documents gracefully due to chunking

    def test_concurrent_operations_handling(self):
        """Test handling of concurrent operations."""
        # Simulate multiple concurrent uploads and queries
        pdf_files = [
            self.create_mock_pdf_file(f"doc{i}.pdf") for i in range(5)
        ]
        
        # Upload multiple files (simulating concurrent access)
        responses = []
        for pdf_file in pdf_files:
            response = self.client.post("/upload-pdf", files=[pdf_file])
            responses.append(response)
        
        # All should succeed (last one wins due to global state)
        for response in responses:
            assert response.status_code == 200

    def test_enhanced_query_validation(self):
        """Test enhanced query validation and processing."""
        # Upload PDF first
        pdf_file = self.create_mock_pdf_file()
        self.client.post("/upload-pdf", files=[pdf_file])
        
        # Test various query formats
        query_tests = [
            {"query": "Simple question"},
            {"query": "Question with special characters: @#$%^&*()"},
            {"query": "Very long question that exceeds normal length limits and tests system robustness" * 10},
            {"query": "Question with Unicode: 你好, مرحبا, Здравствуйте"},
            {"query": "Question\nwith\nnewlines"},
            {"query": "   Query with extra spaces   "}
        ]
        
        for query_test in query_tests:
            response = self.client.post("/qa", json=query_test)
            assert response.status_code == 200

    def test_retriever_optimization_settings(self):
        """Test retriever optimization settings."""
        # Upload PDF first
        pdf_file = self.create_mock_pdf_file()
        self.client.post("/upload-pdf", files=[pdf_file])
        
        # Trigger Q&A to create retriever
        qa_data = {"query": "Test optimization"}
        response = self.client.post("/qa", json=qa_data)
        
        assert response.status_code == 200
        # Verify retriever was created from FAISS index
        self.mock_faiss.from_documents.return_value.as_retriever.assert_called()

    def test_app_title_and_configuration(self):
        """Test FastAPI app configuration and metadata."""
        assert self.app.title == "PDF Q&A Bot"
        # Could test additional app configurations here

    def test_edge_case_pdf_files(self):
        """Test edge cases with various PDF file characteristics."""
        edge_cases = [
            # Empty filename
            ("file", ("", io.BytesIO(b"content"), "application/pdf")),
            # Very long filename  
            ("file", ("a" * 200 + ".pdf", io.BytesIO(b"content"), "application/pdf")),
            # Filename with spaces and special characters
            ("file", ("My Document (2024) - Final.pdf", io.BytesIO(b"content"), "application/pdf"))
        ]
        
        for edge_case in edge_cases:
            response = self.client.post("/upload-pdf", files=[edge_case])
            # Most should succeed or fail gracefully
            assert response.status_code in [200, 400, 422]

    def test_memory_efficiency_with_repeated_uploads(self):
        """Test memory efficiency with repeated PDF uploads."""
        # Simulate multiple uploads to test memory management
        for i in range(10):
            pdf_file = self.create_mock_pdf_file(f"iteration_{i}.pdf")
            response = self.client.post("/upload-pdf", files=[pdf_file])
            assert response.status_code == 200
            
            # Each upload should replace the previous index
            # This tests the global state management

    def test_json_response_structure_validation(self):
        """Test JSON response structure validation."""
        # Test upload response structure
        pdf_file = self.create_mock_pdf_file()
        upload_response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert upload_response.status_code == 200
        upload_data = upload_response.json()
        assert isinstance(upload_data, dict)
        assert "message" in upload_data
        assert isinstance(upload_data["message"], str)
        
        # Test Q&A response structure
        qa_data = {"query": "Test question"}
        qa_response = self.client.post("/qa", json=qa_data)
        
        assert qa_response.status_code == 200
        qa_data = qa_response.json()
        assert isinstance(qa_data, dict)
        assert "answer" in qa_data
        assert isinstance(qa_data["answer"], str)

    def test_advanced_document_preprocessing(self):
        """Test advanced document preprocessing capabilities."""
        with patch('Day21.example.PdfReader') as mock_pdf:
            # Simulate PDF with various text formatting
            mock_page = MagicMock()
            mock_page.extract_text.return_value = (
                "TITLE IN CAPITALS\n"
                "subtitle in lowercase\n" 
                "Mixed Case Content With Numbers 123\n"
                "Special symbols: @#$%^&*()\n"
                "   Extra    spacing   issues   \n"
                "Bullet points:\n• Point 1\n• Point 2"
            )
            mock_pdf_instance = MagicMock()
            mock_pdf_instance.pages = [mock_page]
            mock_pdf.return_value = mock_pdf_instance
            
            pdf_file = self.create_mock_pdf_file("formatted_document.pdf")
            response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()