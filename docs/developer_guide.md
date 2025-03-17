# Azure Function Markitdown Developer Guide

This guide provides information for developers working on the Azure Function Markitdown project.

## Project Structure

```
src/
  function_app/             # Main Azure Function App
    __init__.py             # App initialization
    function_app.py         # Function trigger definitions
    host.json               # Azure Functions host configuration
    local.settings.json     # Local environment settings
    logging_config.py       # Logging configuration
    requirements.txt        # Function-specific dependencies
    converter/              # Markdown conversion module
      __init__.py           # Package initialization
      file_detector.py      # File type detection
      markitdown_service.py # Markitdown integration service
tests/
  unit/                     # Unit tests
    test_file_detector.py   # Tests for file detection
    test_markitdown_service.py  # Tests for conversion service
  integration/              # Integration tests
    test_api_endpoint.py    # Tests for the API endpoint
docs/
  api.md                    # API documentation
  developer_guide.md        # Developer documentation
```

## Local Development

### Prerequisites

- Python 3.10+
- Azure Functions Core Tools
- Azure CLI (for deployment)

### Setup Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/azure-function-markitdown.git
   cd azure-function-markitdown
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install the Azure Functions Core Tools if not already installed:
   ```bash
   npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```

### Running Locally

1. Start the function app:
   ```bash
   cd src/function_app
   func start
   ```

2. The API will be available at `http://localhost:7071/api/convert`

3. Test with curl:
   ```bash
   curl -X POST http://localhost:7071/api/convert \
     -F "file=@/path/to/your/document.docx" \
     -H "Content-Type: multipart/form-data"
   ```

### Running Tests

Run the tests using pytest:

```bash
pip install pytest
pytest
```

Run tests with coverage:

```bash
pip install pytest-cov
pytest --cov=src
```

## Adding Support for New File Types

To add support for a new file type:

1. Update the `SUPPORTED_TYPES` dictionary in `file_detector.py`
2. Add a mapping in the `extension_to_converter` and `mime_to_converter` dictionaries in `get_converter_for_file()`
3. Add a new converter implementation in `markitdown_service.py` (or use an existing one)
4. Write tests for the new file type

Example for adding support for a new file type:

```python
# In file_detector.py
SUPPORTED_TYPES = {
    # ...existing types...
    '.new': 'application/x-new-format',
}

# In get_converter_for_file()
extension_to_converter = {
    # ...existing converters...
    '.new': 'new_format',
}

mime_to_converter = {
    # ...existing converters...
    'application/x-new-format': 'new_format',
}

# In markitdown_service.py
if converter_type == 'new_format':
    result = markitdown.convert_new_format(temp_file_path)
```

## Deployment

### Deployment to Azure

1. Login to Azure:
   ```bash
   az login
   ```

2. Create required resources (if they don't exist):
   ```bash
   az group create --name YourResourceGroup --location YourLocation
   az storage account create --name YourStorageAccount --resource-group YourResourceGroup --location YourLocation --sku Standard_LRS
   az functionapp create --name YourFunctionApp --resource-group YourResourceGroup --consumption-plan-location YourLocation --storage-account YourStorageAccount --runtime python --functions-version 4 --os-type Linux --runtime-version 3.10
   ```

3. Configure application settings:
   ```bash
   az functionapp config appsettings set --name YourFunctionApp --resource-group YourResourceGroup --settings "MARKITDOWN_MAX_FILE_SIZE=25000000"
   ```

4. Deploy the function app:
   ```bash
   cd src/function_app
   func azure functionapp publish YourFunctionApp
   ```

### CI/CD with GitHub Actions

The project includes a GitHub Actions workflow for continuous deployment to Azure. To use it:

1. Create a publish profile for your Azure Function in the Azure Portal
2. Add the publish profile as a GitHub secret named `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`
3. Ensure the workflow is configured with the correct function app name in `env.AZURE_FUNCTIONAPP_NAME`
4. Commit and push to the main branch to trigger deployment

## Troubleshooting

Common issues and solutions:

1. **File size limits**: Check the `MARKITDOWN_MAX_FILE_SIZE` environment variable
2. **Missing dependencies**: Ensure all dependencies are installed, including optional markitdown extensions
3. **Deployment failures**: Check Azure Function logs with `func azure functionapp logstream YourFunctionApp`
4. **Local execution errors**: Check logs in the terminal where `func start` is running