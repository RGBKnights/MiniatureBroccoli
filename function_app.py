import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

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
    
    results = []
    
    for file in files:
        # Here we would process the file using Markitdown
        # For now, we'll just return a placeholder markdown content
        result = {
            "filename": file.filename,
            "title": f"Title for {file.filename}",
            "markdown": f"# Converted Document\n\n## Content from {file.filename}\n\nThis is the content that was extracted and converted to markdown..."
        }
        results.append(result)
    
    # Always return an array of results, even for a single file
    return func.HttpResponse(
        json.dumps(results),
        mimetype="application/json",
        status_code=200
    )