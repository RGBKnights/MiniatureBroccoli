"""
Unit tests for markitdown_service module
"""
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import tempfile

# Add src directory to path to enable imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.function_app.converter.markitdown_service import MarkitdownService

class TestMarkitdownService(unittest.TestCase):
    """Test cases for MarkitdownService functionality"""
    
    def setUp(self):
        """Set up tests"""
        # Override environment variable for testing
        with patch.dict('os.environ', {'MARKITDOWN_MAX_FILE_SIZE': '1000'}):
            self.service = MarkitdownService()
    
    def test_init(self):
        """Test service initialization"""
        self.assertEqual(self.service.max_file_size, 1000)
    
    def test_check_file_size_within_limit(self):
        """Test file size check when within limits"""
        file_content = b"x" * 500  # 500 bytes, under the 1000 byte limit
        result = self.service.check_file_size(file_content)
        self.assertTrue(result)
    
    def test_check_file_size_exceeds_limit(self):
        """Test file size check when exceeding limits"""
        file_content = b"x" * 1500  # 1500 bytes, over the 1000 byte limit
        result = self.service.check_file_size(file_content)
        self.assertFalse(result)
    
    def test_extract_title_with_header(self):
        """Test title extraction from markdown with header"""
        markdown = "# This is a title\n\nSome content"
        title = self.service._extract_title(markdown)
        self.assertEqual(title, "This is a title")
    
    def test_extract_title_without_header(self):
        """Test title extraction from markdown without header"""
        markdown = "Some content without header"
        title = self.service._extract_title(markdown)
        self.assertEqual(title, "Untitled Document")
    
    def test_extract_title_with_error(self):
        """Test title extraction handling errors"""
        with patch.object(self.service, '_extract_title', side_effect=Exception("Test error")):
            title = self.service._extract_title(None)
            self.assertEqual(title, "Untitled Document")
    
    @patch('tempfile.NamedTemporaryFile')
    @patch('os.unlink')
    def test_convert_to_markdown_file_size_error(self, mock_unlink, mock_temp_file):
        """Test convert_to_markdown with file size error"""
        # Mock a large file
        file_content = b"x" * 1500  # Larger than our 1000 byte limit
        
        # Expect ValueError for file size
        with self.assertRaises(ValueError):
            self.service.convert_to_markdown("test.txt", file_content, "text")
        
        # Verify temp file wasn't created
        mock_temp_file.assert_not_called()
    
    @patch('tempfile.NamedTemporaryFile')
    @patch('os.path.exists', return_value=True)
    @patch('os.unlink')
    def test_convert_to_markdown_text_file(self, mock_unlink, mock_exists, mock_temp_file):
        """Test convert_to_markdown with text file"""
        # Mock file content
        file_content = b"This is test content"
        file_name = "test.txt"
        
        # Mock the temporary file
        mock_temp = MagicMock()
        mock_temp.name = "/tmp/mockfile.txt"
        mock_temp_file.return_value.__enter__.return_value = mock_temp
        
        # Mock open to return our test content
        m = mock_open(read_data="This is test content")
        
        with patch('builtins.open', m):
            # Test the conversion
            result = self.service.convert_to_markdown(file_name, file_content, "text")
            
            # Verify result
            self.assertEqual(result["filename"], file_name)
            self.assertEqual(result["title"], "test.txt")
            self.assertIn("# test.txt", result["markdown"])
            self.assertIn("This is test content", result["markdown"])
            self.assertEqual(result["metadata"]["converter_type"], "text")
            self.assertEqual(result["metadata"]["file_size"], len(file_content))
            
            # Verify cleanup
            mock_unlink.assert_called_once_with(mock_temp.name)
    
    @patch('importlib.util.find_spec', return_value=None)  # Mock markitdown not installed
    @patch('tempfile.NamedTemporaryFile')
    @patch('os.path.exists', return_value=True)
    @patch('os.unlink')
    def test_convert_to_markdown_mock_implementation(self, mock_unlink, mock_exists, mock_temp_file, mock_find_spec):
        """Test convert_to_markdown using the mock implementation when markitdown is not installed"""
        # Reload the module to use our mocked importlib.util.find_spec
        import importlib
        from src.function_app.converter import markitdown_service
        importlib.reload(markitdown_service)
        
        # Create a service with the mocked environment
        service = markitdown_service.MarkitdownService()
        
        # Mock file content
        file_content = b"This is test content"
        file_name = "test.pdf"
        
        # Mock the temporary file
        mock_temp = MagicMock()
        mock_temp.name = "/tmp/mockfile.pdf"
        mock_temp_file.return_value.__enter__.return_value = mock_temp
        
        # Test the conversion
        result = service.convert_to_markdown(file_name, file_content, "pdf")
        
        # Verify result contains mock data
        self.assertEqual(result["filename"], file_name)
        self.assertIn("Mock conversion for pdf", result["markdown"])
        
        # Verify cleanup
        mock_unlink.assert_called_once_with(mock_temp.name)

if __name__ == '__main__':
    unittest.main()