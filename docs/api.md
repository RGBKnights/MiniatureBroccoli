# Azure Function Markitdown API Documentation

This document provides detailed information about the API endpoints exposed by the Azure Function Markitdown service.

## File Conversion Endpoint

### POST /api/convert

Converts a document to markdown format.

#### Request

- **Method**: POST
- **Content-Type**: `multipart/form-data`
- **Body**: Form data containing the file to convert

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | Yes | The file to convert. Supported formats include PDF, DOCX, PPTX, XLSX, HTML, images, and more. |

#### Example Request

```bash
curl -X POST https://your-function-app.azurewebsites.net/api/convert \
  -F "file=@/path/to/your/document.docx" \
  -H "Content-Type: multipart/form-data"
```

#### Response

- **Content-Type**: `application/json`
- **Status Codes**:
  - `200 OK`: File successfully converted
  - `400 Bad Request`: Invalid request (missing file, file too large)
  - `415 Unsupported Media Type`: Unsupported file format
  - `500 Internal Server Error`: Server error during conversion

#### Response Body

A JSON object containing the following properties:

| Property | Type | Description |
|----------|------|-------------|
| `filename` | String | The original filename that was uploaded |
| `title` | String | The title extracted from the document, or "Untitled Document" if none found |
| `markdown` | String | The converted markdown content |
| `metadata` | Object | Metadata about the conversion process |
| `metadata.converter_type` | String | The converter type used (pdf, docx, text, etc.) |
| `metadata.file_size` | Number | Size of the original file in bytes |

#### Example Response

```json
{
  "filename": "sample.docx",
  "title": "Sample Document",
  "markdown": "# Sample Document\n\n## Introduction\n\nThis is a sample document that has been converted to markdown...",
  "metadata": {
    "converter_type": "docx",
    "file_size": 25600
  }
}
```

#### Error Response

```json
{
  "error": "File size exceeds maximum allowed size of 25000000 bytes"
}
```

## Supported File Types

The API supports converting the following file types to markdown:

- **Documents**: PDF, Word (DOCX), PowerPoint (PPTX), Excel (XLSX)
- **Web**: HTML, HTM
- **Text**: Markdown (MD), Plain Text (TXT)
- **E-books**: EPUB
- **Images**: JPG, JPEG, PNG (with OCR for text extraction)
- **Audio**: MP3, WAV (with transcription)
- **Archives**: ZIP (iterates through contents)

## File Size Limits

- Maximum file size: 25MB by default
- This limit can be configured by setting the `MARKITDOWN_MAX_FILE_SIZE` environment variable

## Notes

- The API does not store uploaded files; they are processed in memory and temporary files are deleted after conversion
- No authentication is currently required to use the API
- Rate limiting is not currently implemented