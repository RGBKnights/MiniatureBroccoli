import os
import json
import logging
import azure.functions as func
from .logging_config import log_request
from .converter.file_detector import detect_file_type, get_converter_for_file
from .converter.markitdown_service import MarkitdownService

# Create the Azure Function app
app = func.FunctionApp()

# Initialize the markitdown service
markitdown_service = MarkitdownService()

@app.route(route="convert", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
def convert_file(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP trigger function for file conversion.
    This function receives a file and converts it to markdown using the Markitdown library.
    """
    logging.info('Python HTTP trigger function processed a request for file conversion.')
    log_request(logging.getLogger(), req)
    
    try:
        # Check if the request has a file
        if not req.files:
            logging.warning("No file content received in the request")
            return func.HttpResponse(
                json.dumps({"error": "No file content in request"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Get the file from the request (assuming the first file if multiple are sent)
        file_name = list(req.files.keys())[0]
        file_content = req.files[file_name].read()  # Read the file content
        logging.info(f"Received file: {file_name}")
        
        # Detect file type
        file_extension, mime_type, is_supported = detect_file_type(file_name, file_content)
        
        # Check if file type is supported
        if not is_supported:
            logging.warning(f"Unsupported file type: {file_extension} with MIME type {mime_type}")
            return func.HttpResponse(
                json.dumps({
                    "error": f"Unsupported file type: {file_extension}",
                    "mime_type": mime_type
                }),
                status_code=415,  # Unsupported Media Type
                mimetype="application/json"
            )
        
        # Get the appropriate converter for the file type
        converter_type = get_converter_for_file(file_extension, mime_type)
        
        # Convert the file to markdown
        try:
            result = markitdown_service.convert_to_markdown(file_name, file_content, converter_type)
            return func.HttpResponse(
                json.dumps(result),
                status_code=200,
                mimetype="application/json"
            )
        except ValueError as value_error:
            # For known validation errors like file size
            logging.warning(f"Validation error: {str(value_error)}")
            return func.HttpResponse(
                json.dumps({"error": str(value_error)}),
                status_code=400,
                mimetype="application/json"
            )
        
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": f"Internal server error: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )