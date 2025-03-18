# Azure Function with Markitdown

An Azure Function Application that leverages the Markitdown Python library to provide file conversion to markdown via a serverless API.

## Features

- RESTful API powered by the Markitdown Python library
- File format conversion to markdown
- Support for multiple document types (PDF, Word, PowerPoint, etc.)

## Prerequisites

- Python 3.10+
- Azure Functions Core Tools
- Azure CLI (for deployment)
- Azure Subscription

## Installation

### Optional Dependencies

At the moment, the following optional dependencies are available:
[all] Installs all optional dependencies
[pptx] Installs dependencies for PowerPoint files
[docx] Installs dependencies for Word files
[xlsx] Installs dependencies for Excel files
[xls] Installs dependencies for older Excel files
[pdf] Installs dependencies for PDF files
[outlook] Installs dependencies for Outlook messages
[az-doc-intel] Installs dependencies for Azure Document Intelligence
[audio-transcription] Installs dependencies for audio transcription of wav and mp3 files

### Local Development

```bash
# Clone the repository
git clone https://github.com/RGBKnights/MiniatureBroccoli.git
cd MiniatureBroccoli

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Markitdown with required extensions
pip install markitdown[all]

# Install additional dependencies
pip install -r requirements.txt

# Start the function app locally
func start
```

### Azure Deployment

```bash
# Login to Azure
az login

# Create resource group (if needed)
az group create --name YourResourceGroup --location YourLocation

# Create storage account
az storage account create --name YourStorageAccount --resource-group YourResourceGroup --location YourLocation --sku Standard_LRS

# Create function app with Python support
az functionapp create --name YourFunctionApp --resource-group YourResourceGroup --consumption-plan-location YourLocation --storage-account YourStorageAccount --runtime python --functions-version 4 --os-type Linux --runtime-version 3.10

# Add application settings if needed
az functionapp config appsettings set --name YourFunctionApp --resource-group YourResourceGroup --settings "MARKITDOWN_MAX_FILE_SIZE=25000000"

# Update requirements.txt to include markitdown and extensions
echo "markitdown[all]" >> requirements.txt

# Deploy the function app
func azure functionapp publish YourFunctionApp
```

## API Usage

The API provides a single endpoint that processes various file types supported by the Microsoft Markitdown library and returns processed markdown content.

### Process File

```http
POST /api/convert
Content-Type: multipart/form-data

file: [Binary file content]
```

This endpoint accepts the following file types:

- PDF
- PowerPoint
- Word
- Excel
- Images (EXIF metadata and OCR)
- Audio (EXIF metadata and speech transcription)
- HTML
- Text-based formats (CSV, JSON, XML)
- ZIP files (iterates over contents)
- EPubs

#### Example usage with cURL:

```bash
curl -X POST https://your-function-app.azurewebsites.net/api/convert \
  -F "file=@/path/to/your/document.docx" \
  -H "Content-Type: multipart/form-data"
```

#### Response:

```json
[
  {
    "filename": "document.docx",
    "title": "Optional title of the document.",
    "markdown": "# Converted Document\n\n## Content from Original File\n\nThis is the content that was extracted and converted to markdown..."
  },
  {
    "filename": "presentation.pptx",
    "title": "Another document title",
    "markdown": "# Converted Presentation\n\n## Slide 1\n\nContent from the first slide..."
  }
]
```

NOTE: The response will always be an array, even when processing a single file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
