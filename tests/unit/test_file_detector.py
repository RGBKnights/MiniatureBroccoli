"""
Unit tests for file_detector module
"""
import os
import unittest
from unittest.mock import patch, MagicMock
import sys

# Add src directory to path to enable imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.function_app.converter.file_detector import detect_file_type, get_converter_for_file

class TestFileDetector(unittest.TestCase):
    """Test cases for file_detector functionality"""
    
    def test_detect_file_type_pdf(self):
        """Test PDF file detection"""
        file_name = "test.pdf"
        file_content = b"%PDF-1.5\n"  # PDF file signature
        
        with patch("magic.from_buffer", return_value="application/pdf"):
            extension, mime_type, is_supported = detect_file_type(file_name, file_content)
            
            self.assertEqual(extension, ".pdf")
            self.assertEqual(mime_type, "application/pdf")
            self.assertTrue(is_supported)
    
    def test_detect_file_type_docx(self):
        """Test DOCX file detection"""
        file_name = "test.docx"
        file_content = b"PK\x03\x04"  # DOCX file signature (actually zip but magic should identify it)
        
        with patch("magic.from_buffer", return_value="application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
            extension, mime_type, is_supported = detect_file_type(file_name, file_content)
            
            self.assertEqual(extension, ".docx")
            self.assertEqual(mime_type, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            self.assertTrue(is_supported)
    
    def test_detect_file_type_unsupported(self):
        """Test unsupported file detection"""
        file_name = "test.xyz"
        file_content = b"Some random content"
        
        with patch("magic.from_buffer", return_value="application/octet-stream"):
            with patch("mimetypes.guess_type", return_value=(None, None)):
                extension, mime_type, is_supported = detect_file_type(file_name, file_content)
                
                self.assertEqual(extension, ".xyz")
                self.assertEqual(mime_type, "application/octet-stream")
                self.assertFalse(is_supported)
    
    def test_get_converter_for_file_pdf(self):
        """Test getting the right converter for PDF files"""
        converter_type = get_converter_for_file(".pdf", "application/pdf")
        self.assertEqual(converter_type, "pdf")
    
    def test_get_converter_for_file_docx(self):
        """Test getting the right converter for DOCX files"""
        converter_type = get_converter_for_file(".docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        self.assertEqual(converter_type, "docx")
    
    def test_get_converter_for_file_fallback(self):
        """Test fallback converter when type is unknown"""
        converter_type = get_converter_for_file(".unknown", "application/octet-stream")
        self.assertEqual(converter_type, "text")
    
    def test_get_converter_for_file_by_extension(self):
        """Test getting converter by extension when mime type is missing"""
        converter_type = get_converter_for_file(".pdf", None)
        self.assertEqual(converter_type, "pdf")
    
    def test_get_converter_for_file_by_mimetype(self):
        """Test getting converter by mime type when extension doesn't match"""
        converter_type = get_converter_for_file(".bin", "application/pdf")
        self.assertEqual(converter_type, "pdf")

if __name__ == '__main__':
    unittest.main()