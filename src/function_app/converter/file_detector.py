"""
File type detection module for Markitdown converter.
"""
import os
import logging
import mimetypes
import magic

logger = logging.getLogger(__name__)

# Map of file extensions to their corresponding MIME types
SUPPORTED_TYPES = {
    # Document formats
    '.pdf': 'application/pdf',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    
    # Web formats
    '.html': 'text/html',
    '.htm': 'text/html',
    
    # Text formats
    '.md': 'text/markdown',
    '.txt': 'text/plain',
    
    # E-book formats
    '.epub': 'application/epub+zip',
    
    # Image formats
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    
    # Audio formats
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    
    # Archive formats
    '.zip': 'application/zip'
}

def detect_file_type(file_name, file_content):
    """
    Detects the file type based on the file name and content.
    
    Args:
        file_name (str): The name of the file
        file_content (bytes): The binary content of the file
        
    Returns:
        tuple: (file_extension, mime_type, is_supported)
    """
    # Initialize mimetypes
    mimetypes.init()
    
    # Get the file extension
    _, file_extension = os.path.splitext(file_name.lower())
    
    # Try to detect MIME type from file content
    try:
        mime_type = magic.from_buffer(file_content, mime=True)
        logger.info(f"Detected MIME type: {mime_type} for file: {file_name}")
    except Exception as e:
        logger.warning(f"Failed to detect MIME type from content: {str(e)}")
        # Fallback to extension-based detection
        mime_type = mimetypes.guess_type(file_name)[0]
        logger.info(f"Fallback MIME type based on extension: {mime_type} for file: {file_name}")
    
    # Check if the file type is supported
    is_supported = False
    if file_extension in SUPPORTED_TYPES:
        is_supported = True
    elif mime_type and any(mime_type == m for m in SUPPORTED_TYPES.values()):
        is_supported = True
    
    return file_extension, mime_type, is_supported

def get_converter_for_file(file_extension, mime_type):
    """
    Determines the appropriate converter based on file type.
    
    Args:
        file_extension (str): The file extension
        mime_type (str): The MIME type of the file
        
    Returns:
        str: The converter type to use
    """
    # Map file types to converter types
    extension_to_converter = {
        '.pdf': 'pdf',
        '.docx': 'docx',
        '.pptx': 'pptx',
        '.xlsx': 'xlsx',
        '.html': 'html',
        '.htm': 'html',
        '.md': 'markdown',
        '.txt': 'text',
        '.epub': 'epub',
        '.jpg': 'image',
        '.jpeg': 'image',
        '.png': 'image',
        '.mp3': 'audio',
        '.wav': 'audio',
        '.zip': 'archive'
    }
    
    # Try to get converter based on extension
    converter_type = extension_to_converter.get(file_extension.lower())
    
    # If not found, try to determine based on MIME type
    if not converter_type and mime_type:
        # Map MIME types to converter types
        mime_to_converter = {
            'application/pdf': 'pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
            'text/html': 'html',
            'text/markdown': 'markdown',
            'text/plain': 'text',
            'application/epub+zip': 'epub',
            'image/jpeg': 'image',
            'image/png': 'image',
            'audio/mpeg': 'audio',
            'audio/wav': 'audio',
            'application/zip': 'archive'
        }
        converter_type = mime_to_converter.get(mime_type)
    
    # Default to text if we couldn't determine the type
    if not converter_type:
        logger.warning(f"Could not determine converter for {file_extension} with MIME type {mime_type}. Defaulting to 'text'.")
        converter_type = 'text'
    
    logger.info(f"Selected converter '{converter_type}' for file with extension '{file_extension}' and MIME type '{mime_type}'")
    return converter_type