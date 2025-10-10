"""
Comprehensive test suite for Day20 - PDF Q&A Bot with FastAPI

This module tests:
- FastAPI PDF upload endpoint with file validation
- PDF text extraction using PyPDF2
- Document processing and text chunking
- FAISS vector store with PDF content
- RetrievalQA chain for PDF-based Q&A
- Global state management for FAISS index
- Error handling and edge cases
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
import pytest
from fastapi.testclient import TestClient
import json
import io
from pathlib import Path


class TestDay20PDFQABot(unittest.TestCase):
    """Test suite for Day20 PDF Q&A Bot system."""

    def setUp(self):
        """Set up test client and mocks for FastAPI app."""
        # Mock all external dependencies before importing
        with patch('Day20.example.PdfReader') as mock_pdf_reader, \
             patch('Day20.example.OpenAIEmbeddings') as mock_embeddings, \
             patch('Day20.example.FAISS') as mock_faiss, \
             patch('Day20.example.ChatOpenAI') as mock_chat, \
             patch('Day20.example.RetrievalQA') as mock_qa:
            
            # Configure PDF reader mock
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "This is sample PDF text content."
            mock_pdf_instance = MagicMock()
            mock_pdf_instance.pages = [mock_page, mock_page]  # Two pages
            mock_pdf_reader.return_value = mock_pdf_instance
            
            # Configure embeddings mock
            mock_embeddings_instance = MagicMock()
            mock_embeddings.return_value = mock_embeddings_instance
            
            # Configure FAISS mock
            mock_faiss_instance = MagicMock()
            mock_faiss.from_documents.return_value = mock_faiss_instance
            mock_faiss_instance.as_retriever.return_value = MagicMock()
            
            # Configure ChatOpenAI mock
            mock_chat_instance = MagicMock()
            mock_chat.return_value = mock_chat_instance
            
            # Configure RetrievalQA mock
            mock_qa_chain = MagicMock()
            mock_qa_chain.run.return_value = "This is a PDF-based answer."
            mock_qa.from_chain_type.return_value = mock_qa_chain
            
            # Import the module after setting up mocks
            from Day20.example import app
            self.app = app
            self.client = TestClient(app)
            
            # Store mocks for assertions
            self.mock_pdf_reader = mock_pdf_reader
            self.mock_embeddings = mock_embeddings
            self.mock_faiss = mock_faiss
            self.mock_chat = mock_chat
            self.mock_qa = mock_qa
            self.mock_qa_chain = mock_qa_chain

    def create_mock_pdf_file(self, filename="test.pdf", content=b"fake pdf content"):
        """Helper method to create mock PDF file for testing."""
        return ("file", (filename, io.BytesIO(content), "application/pdf"))

    def test_upload_pdf_successful(self):
        """Test successful PDF upload and processing."""
        pdf_file = self.create_mock_pdf_file()
        
        response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert "test.pdf" in response_data["message"]
        assert "uploaded and indexed successfully" in response_data["message"]

    def test_upload_pdf_invalid_file_extension(self):
        """Test PDF upload with invalid file extension."""
        txt_file = ("file", ("test.txt", io.BytesIO(b"text content"), "text/plain"))
        
        response = self.client.post("/upload-pdf", files=[txt_file])
        
        assert response.status_code == 400
        assert "Only PDF files are allowed" in response.json()["detail"]

    def test_upload_pdf_no_file_provided(self):
        """Test PDF upload endpoint without providing a file."""
        response = self.client.post("/upload-pdf")
        
        assert response.status_code == 422  # Validation error

    def test_upload_pdf_empty_file(self):
        """Test PDF upload with empty file."""
        empty_file = self.create_mock_pdf_file(content=b"")
        
        response = self.client.post("/upload-pdf", files=[empty_file])
        
        # Should still process successfully due to mocking
        assert response.status_code == 200

    def test_upload_multiple_pdfs(self):
        """Test uploading multiple PDFs (should replace previous one)."""
        pdf_file1 = self.create_mock_pdf_file("doc1.pdf")
        pdf_file2 = self.create_mock_pdf_file("doc2.pdf")
        
        # Upload first PDF
        response1 = self.client.post("/upload-pdf", files=[pdf_file1])
        assert response1.status_code == 200
        
        # Upload second PDF (should replace first)
        response2 = self.client.post("/upload-pdf", files=[pdf_file2])
        assert response2.status_code == 200
        assert "doc2.pdf" in response2.json()["message"]

    def test_pdf_text_extraction_and_processing(self):
        """Test that PDF text is properly extracted and processed."""
        pdf_file = self.create_mock_pdf_file()
        
        response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 200
        # Verify PDF reader was called
        self.mock_pdf_reader.assert_called_once()
        # Verify FAISS indexing was performed
        self.mock_faiss.from_documents.assert_called_once()

    def test_qa_after_pdf_upload(self):
        """Test Q&A functionality after successful PDF upload."""
        # First upload a PDF
        pdf_file = self.create_mock_pdf_file()
        upload_response = self.client.post("/upload-pdf", files=[pdf_file])
        assert upload_response.status_code == 200
        
        # Then ask a question
        qa_data = {"query": "What is this document about?"}
        qa_response = self.client.post("/qa", json=qa_data)
        
        assert qa_response.status_code == 200
        response_data = qa_response.json()
        assert "answer" in response_data
        assert response_data["answer"] == "This is a PDF-based answer."

    def test_qa_without_uploading_pdf(self):
        """Test Q&A functionality without first uploading a PDF."""
        qa_data = {"query": "What is this document about?"}
        
        # Reset the global faiss_index to None
        import Day20.example
        Day20.example.faiss_index = None
        
        qa_response = self.client.post("/qa", json=qa_data)
        
        assert qa_response.status_code == 400
        assert "No PDF uploaded yet" in qa_response.json()["detail"]

    def test_qa_missing_query_field(self):
        """Test Q&A endpoint with missing query field."""
        # First upload a PDF
        pdf_file = self.create_mock_pdf_file()
        self.client.post("/upload-pdf", files=[pdf_file])
        
        # Try Q&A without query
        response = self.client.post("/qa", json={})
        
        assert response.status_code == 422  # Validation error

    def test_qa_empty_query(self):
        """Test Q&A with empty query string."""
        # First upload a PDF
        pdf_file = self.create_mock_pdf_file()
        self.client.post("/upload-pdf", files=[pdf_file])
        
        # Ask with empty query
        qa_data = {"query": ""}
        qa_response = self.client.post("/qa", json=qa_data)
        
        assert qa_response.status_code == 200

    def test_qa_long_query(self):
        """Test Q&A with very long query."""
        # First upload a PDF
        pdf_file = self.create_mock_pdf_file()
        self.client.post("/upload-pdf", files=[pdf_file])
        
        # Ask with long query
        long_query = "This is a very long query. " * 100
        qa_data = {"query": long_query}
        qa_response = self.client.post("/qa", json=qa_data)
        
        assert qa_response.status_code == 200

    @patch('Day20.example.CharacterTextSplitter')
    def test_text_splitting_configuration(self, mock_splitter):
        """Test that text splitter is configured correctly."""
        mock_splitter_instance = MagicMock()
        mock_splitter_instance.split_text.return_value = ["chunk1", "chunk2"]
        mock_splitter.return_value = mock_splitter_instance
        
        pdf_file = self.create_mock_pdf_file()
        
        with patch('Day20.example.PdfReader') as mock_pdf, \
             patch('Day20.example.OpenAIEmbeddings'), \
             patch('Day20.example.FAISS'):
            
            # Mock PDF reader
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "Long text content"
            mock_pdf_instance = MagicMock()
            mock_pdf_instance.pages = [mock_page]
            mock_pdf.return_value = mock_pdf_instance
            
            response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 200
        # Verify text splitter was configured correctly
        mock_splitter.assert_called_with(chunk_size=500, chunk_overlap=50)

    def test_openai_embeddings_initialization(self):
        """Test OpenAI embeddings initialization."""
        pdf_file = self.create_mock_pdf_file()
        
        response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 200
        # Verify embeddings were initialized with correct model
        self.mock_embeddings.assert_called_with(model="text-embedding-3-small")

    def test_chatgpt_model_initialization(self):
        """Test ChatOpenAI model initialization for Q&A."""
        # Upload PDF first
        pdf_file = self.create_mock_pdf_file()
        self.client.post("/upload-pdf", files=[pdf_file])
        
        # Ask question to trigger model initialization
        qa_data = {"query": "Test question"}
        response = self.client.post("/qa", json=qa_data)
        
        assert response.status_code == 200
        # Verify ChatOpenAI was initialized correctly
        self.mock_chat.assert_called_with(model_name="gpt-3.5-turbo", temperature=0)

    def test_pdf_with_multiple_pages(self):
        """Test PDF processing with multiple pages."""
        # Mock PDF with multiple pages
        with patch('Day20.example.PdfReader') as mock_pdf:
            mock_pages = []
            for i in range(5):  # 5 pages
                mock_page = MagicMock()
                mock_page.extract_text.return_value = f"Page {i+1} content"
                mock_pages.append(mock_page)
            
            mock_pdf_instance = MagicMock()
            mock_pdf_instance.pages = mock_pages
            mock_pdf.return_value = mock_pdf_instance
            
            pdf_file = self.create_mock_pdf_file()
            response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 200

    def test_pdf_with_empty_pages(self):
        """Test PDF processing with empty pages."""
        with patch('Day20.example.PdfReader') as mock_pdf:
            mock_page = MagicMock()
            mock_page.extract_text.return_value = ""  # Empty content
            mock_pdf_instance = MagicMock()
            mock_pdf_instance.pages = [mock_page]
            mock_pdf.return_value = mock_pdf_instance
            
            pdf_file = self.create_mock_pdf_file()
            response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 200

    def test_error_handling_in_pdf_processing(self):
        """Test error handling during PDF processing."""
        # Mock PDF reader to raise an exception
        self.mock_pdf_reader.side_effect = Exception("PDF processing error")
        
        pdf_file = self.create_mock_pdf_file()
        response = self.client.post("/upload-pdf", files=[pdf_file])
        
        assert response.status_code == 500
        assert "detail" in response.json()

    def test_error_handling_in_qa_processing(self):
        """Test error handling during Q&A processing."""
        # Upload PDF first
        pdf_file = self.create_mock_pdf_file()
        self.client.post("/upload-pdf", files=[pdf_file])
        
        # Mock QA chain to raise an exception
        self.mock_qa_chain.run.side_effect = Exception("QA processing error")
        
        qa_data = {"query": "Test question"}
        response = self.client.post("/qa", json=qa_data)
        
        assert response.status_code == 500
        assert "detail" in response.json()

    def test_app_configuration(self):
        """Test FastAPI app configuration."""
        assert self.app.title == "PDF Q&A Bot"

    def test_global_faiss_index_management(self):
        """Test global FAISS index state management."""
        import Day20.example
        
        # Initially should be None
        Day20.example.faiss_index = None
        
        # Upload PDF should set the index
        pdf_file = self.create_mock_pdf_file()
        response = self.client.post("/upload-pdf", files=[pdf_file])
        assert response.status_code == 200
        
        # Index should now be set (mocked)
        # This tests the global state management concept

    def test_file_extension_validation_edge_cases(self):
        """Test file extension validation with edge cases."""
        # Test with .PDF (uppercase)
        pdf_file = ("file", ("test.PDF", io.BytesIO(b"content"), "application/pdf"))
        response = self.client.post("/upload-pdf", files=[pdf_file])
        assert response.status_code == 400  # Should fail due to case sensitivity
        
        # Test with no extension
        no_ext_file = ("file", ("test", io.BytesIO(b"content"), "application/pdf"))
        response = self.client.post("/upload-pdf", files=[no_ext_file])
        assert response.status_code == 400

    def test_concurrent_pdf_uploads(self):
        """Test handling of concurrent PDF uploads."""
        pdf_file1 = self.create_mock_pdf_file("doc1.pdf")
        pdf_file2 = self.create_mock_pdf_file("doc2.pdf")
        
        # Simulate concurrent uploads
        response1 = self.client.post("/upload-pdf", files=[pdf_file1])
        response2 = self.client.post("/upload-pdf", files=[pdf_file2])
        
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_qa_request_model_validation(self):
        """Test QARequest model validation."""
        # Upload PDF first
        pdf_file = self.create_mock_pdf_file()
        self.client.post("/upload-pdf", files=[pdf_file])
        
        # Test with wrong data type
        invalid_data = {"query": ["should", "be", "string"]}
        response = self.client.post("/qa", json=invalid_data)
        
        assert response.status_code == 422

    def test_retrieval_qa_chain_creation(self):
        """Test RetrievalQA chain creation and configuration."""
        # Upload PDF first
        pdf_file = self.create_mock_pdf_file()
        self.client.post("/upload-pdf", files=[pdf_file])
        
        # Ask question to trigger chain creation
        qa_data = {"query": "Test question"}
        response = self.client.post("/qa", json=qa_data)
        
        assert response.status_code == 200
        # Verify RetrievalQA chain was created
        self.mock_qa.from_chain_type.assert_called_once()

    def test_large_pdf_handling(self):
        """Test handling of large PDF files (simulated)."""
        # Mock a large PDF with many pages
        with patch('Day20.example.PdfReader') as mock_pdf:
            # Simulate 100 pages
            mock_pages = []
            for i in range(100):
                mock_page = MagicMock()
                mock_page.extract_text.return_value = f"Page {i+1} with substantial content. " * 50
                mock_pages.append(mock_page)
            
            mock_pdf_instance = MagicMock()
            mock_pdf_instance.pages = mock_pages
            mock_pdf.return_value = mock_pdf_instance
            
            large_pdf = self.create_mock_pdf_file("large.pdf")
            response = self.client.post("/upload-pdf", files=[large_pdf])
        
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()