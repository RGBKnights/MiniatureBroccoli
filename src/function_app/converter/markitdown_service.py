"""
Core service for converting documents to markdown using markitdown library.
"""
import os
import io
import tempfile
import logging
from pathlib import Path
import importlib.util

logger = logging.getLogger(__name__)

# Check if markitdown is installed
markitdown_installed = importlib.util.find_spec("markitdown") is not None

if markitdown_installed:
    import markitdown
    logger.info("Markitdown library successfully imported")
else:
    logger.warning("Markitdown library not installed, using mock implementation")
    # Create a mock implementation for local testing without markitdown
    class MockMarkitdown:
        def __init__(self):
            pass
            
        def convert_to_markdown(self, *args, **kwargs):
            return "# Mock Markdown Conversion\n\nThis is a mock conversion since the markitdown library is not installed."
    
    markitdown = MockMarkitdown()

class MarkitdownService:
    """
    Service for converting documents to markdown using the markitdown library.
    """
    
    def __init__(self):
        """Initialize the Markitdown service with configuration."""
        self.max_file_size = int(os.environ.get('MARKITDOWN_MAX_FILE_SIZE', 25000000))  # Default: 25MB
        logger.info(f"Initialized MarkitdownService with max file size: {self.max_file_size} bytes")
    
    def check_file_size(self, file_content):
        """
        Check if the file size is within the allowed limit.
        
        Args:
            file_content (bytes): The binary content of the file
            
        Returns:
            bool: True if file size is within limits, False otherwise
        """
        file_size = len(file_content)
        
        if file_size > self.max_file_size:
            logger.warning(f"File size {file_size} exceeds maximum allowed size {self.max_file_size}")
            return False
            
        logger.info(f"File size {file_size} is within limits")
        return True
    
    def convert_to_markdown(self, file_name, file_content, converter_type=None):
        """
        Convert a document to markdown using the markitdown library.
        
        Args:
            file_name (str): The name of the file
            file_content (bytes): The binary content of the file
            converter_type (str, optional): The type of converter to use
            
        Returns:
            dict: A dictionary containing the markdown result and metadata
        """
        # Check file size
        if not self.check_file_size(file_content):
            raise ValueError(f"File size exceeds maximum allowed size of {self.max_file_size} bytes")
        
        try:
            # Create a temporary file to save the content
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file_name).suffix) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            logger.info(f"Processing file {file_name} using converter: {converter_type}")
            
            # Process the file with markitdown
            if markitdown_installed:
                # Use the actual markitdown library
                try:
                    # Different converters based on file type
                    if converter_type == 'pdf':
                        result = markitdown.convert_pdf(temp_file_path)
                    elif converter_type == 'docx':
                        result = markitdown.convert_docx(temp_file_path)
                    elif converter_type == 'pptx':
                        result = markitdown.convert_pptx(temp_file_path)
                    elif converter_type == 'xlsx':
                        result = markitdown.convert_xlsx(temp_file_path)
                    elif converter_type == 'html':
                        result = markitdown.convert_html(temp_file_path)
                    elif converter_type == 'epub':
                        result = markitdown.convert_epub(temp_file_path)
                    elif converter_type == 'image':
                        result = markitdown.convert_image(temp_file_path)
                    elif converter_type == 'audio':
                        result = markitdown.convert_audio(temp_file_path)
                    else:
                        # Default converter for text and other formats
                        with open(temp_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        result = f"# {file_name}\n\n{content}"
                except Exception as e:
                    logger.error(f"Error converting file using markitdown: {str(e)}", exc_info=True)
                    # Fallback to basic text extraction
                    try:
                        with open(temp_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        result = f"# {file_name}\n\n{content}"
                    except Exception as read_error:
                        logger.error(f"Error reading file as text: {str(read_error)}", exc_info=True)
                        result = f"# {file_name}\n\nError: Could not convert file content."
            else:
                # Use mock implementation
                result = f"# {file_name}\n\nMock conversion for {converter_type} file type."
            
            # Extract title from the markdown content
            title = self._extract_title(result)
            
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
            return {
                "filename": file_name,
                "title": title,
                "markdown": result,
                "metadata": {
                    "converter_type": converter_type,
                    "file_size": len(file_content)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in convert_to_markdown: {str(e)}", exc_info=True)
            # Clean up the temporary file if it exists
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise
    
    def _extract_title(self, markdown_content):
        """
        Extract the title from the markdown content.
        
        Args:
            markdown_content (str): The markdown content
            
        Returns:
            str: The extracted title or a default title
        """
        try:
            # Look for the first h1 header
            lines = markdown_content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    return line.replace('# ', '')
            return "Untitled Document"
        except Exception as e:
            logger.warning(f"Error extracting title: {str(e)}")
            return "Untitled Document"