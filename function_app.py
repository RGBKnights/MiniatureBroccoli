import azure.functions as func
import logging
import json
from typing import Union, BinaryIO
from pathlib import Path
from markitdown import MarkItDown

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="Convert")
@app.route(route="convert", methods=["POST"])
def convert(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get file data from the request
    files = req.files.values()
    
    if not files:
        return func.HttpResponse(
            json.dumps({"error": "Please upload files in the request"}),
            mimetype="application/json",
            status_code=400
        )
    
    # Initialize MarkItDown
    md = MarkItDown(enable_plugins=False)
    
    results = []
    
    for file in files:
        try:
            # Pass the file stream directly to MarkItDown
            # The convert method accepts Union[str, requests.Response, Path, BinaryIO]
            # conversion_result = md.convert(file.stream)

            # Extract the result
            # result = {
            #     "filename": file.filename,
            #     "title": conversion_result.title if hasattr(conversion_result, 'title') else file.filename,
            #     "markdown": conversion_result.text_content
            # }

            result = {
                "filename": "test.docx",
                "title": "title",
                "markdown": "#title \n\n ##subtitle testing..."
            }
            
            results.append(result)
            
        except Exception as e:
            logging.error(f"Error processing file {file.filename}: {str(e)}")
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    # Always return an array of results, even for a single file
    return func.HttpResponse(
        json.dumps(results),
        mimetype="application/json",
        status_code=200
    )