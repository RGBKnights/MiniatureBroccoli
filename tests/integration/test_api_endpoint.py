"""
Integration tests for the API endpoint
"""
import os
import unittest
import io
import json
import sys
from unittest.mock import patch, MagicMock

# Add src directory to path to enable imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import azure.functions as func
from src.function_app.function_app import convert_file

class TestApiEndpoint(unittest.TestCase):
    """Integration tests for the convert API endpoint"""
    
    def test_convert_file_no_files(self):
        """Test convert_file with no files in request"""
        # Create mock request with no files
        req = func.HttpRequest(
            method='POST',
            url='/api/convert',
            body=None,
            headers={}
        )
        req.files = {}
        
        # Call the function
        response = convert_file(req)
        
        # Check response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.mimetype, "application/json")
        body = json.loads(response.get_body())
        self.assertIn("error", body)
        self.assertIn("No file content", body["error"])
    
    @patch('src.function_app.converter.file_detector.detect_file_type')
    def test_convert_file_unsupported_type(self, mock_detect_file_type):
        """Test convert_file with unsupported file type"""
        # Mock file detection to return unsupported type
        mock_detect_file_type.return_value = ('.xyz', 'application/octet-stream', False)
        
        # Create mock request with a file
        file_body = b'Test file content'
        req = func.HttpRequest(
            method='POST',
            url='/api/convert',
            body=None,
            headers={'Content-Type': 'multipart/form-data; boundary=boundary'}
        )
        
        # Mock the files dictionary
        mock_file = MagicMock()
        mock_file.read.return_value = file_body
        req.files = {'test.xyz': mock_file}
        
        # Call the function
        response = convert_file(req)
        
        # Check response
        self.assertEqual(response.status_code, 415)  # Unsupported Media Type
        self.assertEqual(response.mimetype, "application/json")
        body = json.loads(response.get_body())
        self.assertIn("error", body)
        self.assertIn("Unsupported file type", body["error"])
    
    @patch('src.function_app.converter.file_detector.detect_file_type')
    @patch('src.function_app.converter.file_detector.get_converter_for_file')
    @patch('src.function_app.converter.markitdown_service.MarkitdownService.convert_to_markdown')
    def test_convert_file_successful(self, mock_convert, mock_get_converter, mock_detect_file_type):
        """Test convert_file with successful conversion"""
        # Mock file detection to return a supported type
        mock_detect_file_type.return_value = ('.txt', 'text/plain', True)
        mock_get_converter.return_value = 'text'
        
        # Mock the conversion result
        mock_convert.return_value = {
            "filename": "test.txt",
            "title": "Test Document",
            "markdown": "# Test Document\n\nThis is test content.",
            "metadata": {
                "converter_type": "text",
                "file_size": 16
            }
        }
        
        # Create mock request with a file
        file_body = b'Test file content'
        req = func.HttpRequest(
            method='POST',
            url='/api/convert',
            body=None,
            headers={'Content-Type': 'multipart/form-data; boundary=boundary'}
        )
        
        # Mock the files dictionary
        mock_file = MagicMock()
        mock_file.read.return_value = file_body
        req.files = {'test.txt': mock_file}
        
        # Call the function
        response = convert_file(req)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        body = json.loads(response.get_body())
        self.assertEqual(body["filename"], "test.txt")
        self.assertEqual(body["title"], "Test Document")
        self.assertEqual(body["markdown"], "# Test Document\n\nThis is test content.")
        self.assertEqual(body["metadata"]["converter_type"], "text")
    
    @patch('src.function_app.converter.file_detector.detect_file_type')
    @patch('src.function_app.converter.file_detector.get_converter_for_file')
    @patch('src.function_app.converter.markitdown_service.MarkitdownService.convert_to_markdown')
    def test_convert_file_validation_error(self, mock_convert, mock_get_converter, mock_detect_file_type):
        """Test convert_file with validation error (e.g., file size)"""
        # Mock file detection to return a supported type
        mock_detect_file_type.return_value = ('.txt', 'text/plain', True)
        mock_get_converter.return_value = 'text'
        
        # Mock the conversion to raise a ValueError (e.g., file too large)
        mock_convert.side_effect = ValueError("File size exceeds maximum allowed size")
        
        # Create mock request with a file
        file_body = b'Test file content' * 1000  # Large file
        req = func.HttpRequest(
            method='POST',
            url='/api/convert',
            body=None,
            headers={'Content-Type': 'multipart/form-data; boundary=boundary'}
        )
        
        # Mock the files dictionary
        mock_file = MagicMock()
        mock_file.read.return_value = file_body
        req.files = {'test.txt': mock_file}
        
        # Call the function
        response = convert_file(req)
        
        # Check response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.mimetype, "application/json")
        body = json.loads(response.get_body())
        self.assertIn("error", body)
        self.assertIn("File size exceeds", body["error"])
    
    @patch('src.function_app.converter.file_detector.detect_file_type')
    @patch('src.function_app.converter.file_detector.get_converter_for_file')
    @patch('src.function_app.converter.markitdown_service.MarkitdownService.convert_to_markdown')
    def test_convert_file_unexpected_error(self, mock_convert, mock_get_converter, mock_detect_file_type):
        """Test convert_file with unexpected error"""
        # Mock file detection to return a supported type
        mock_detect_file_type.return_value = ('.txt', 'text/plain', True)
        mock_get_converter.return_value = 'text'
        
        # Mock the conversion to raise an unexpected exception
        mock_convert.side_effect = Exception("Unexpected conversion error")
        
        # Create mock request with a file
        file_body = b'Test file content'
        req = func.HttpRequest(
            method='POST',
            url='/api/convert',
            body=None,
            headers={'Content-Type': 'multipart/form-data; boundary=boundary'}
        )
        
        # Mock the files dictionary
        mock_file = MagicMock()
        mock_file.read.return_value = file_body
        req.files = {'test.txt': mock_file}
        
        # Call the function
        response = convert_file(req)
        
        # Check response
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.mimetype, "application/json")
        body = json.loads(response.get_body())
        self.assertIn("error", body)
        self.assertIn("Internal server error", body["error"])

if __name__ == '__main__':
    unittest.main()