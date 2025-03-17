import os
import json
import logging
import azure.functions as func
from .logging_config import log_request

# Create the Azure Function app
app = func.FunctionApp()

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
        file_content = req.files[file_name]
        logging.info(f"Received file: {file_name}")
        
        # TODO: Implement file type detection and conversion with Markitdown
        # For now, return a mock response
        mock_response = {
            "filename": file_name,
            "title": "Mock Document Title",
            "markdown": "# Mock Document\n\nThis is a mock conversion response. The actual conversion will be implemented soon."
        }
        
        # Return the response
        return func.HttpResponse(
            json.dumps(mock_response),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": f"Internal server error: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )