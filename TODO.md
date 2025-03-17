# Azure Function Markitdown - TODO List

## High Priority
- [ ] Set up basic Azure Function project structure
- [ ] Create requirements.txt with markitdown and dependencies
- [ ] Implement file upload API endpoint (/api/convert)
- [ ] Add file type detection and validation
- [ ] Create core document conversion logic using markitdown
- [ ] Implement proper error handling and logging
- [ ] Add basic tests for the API endpoint

## Medium Priority
- [ ] Implement file size limits and validation
- [ ] Add support for converting specific file types:
  - [ ] PDF documents
  - [ ] Word documents (.docx)
  - [ ] PowerPoint presentations (.pptx)
  - [ ] Excel spreadsheets (.xlsx)
  - [ ] HTML pages
- [ ] Create local development documentation
- [ ] Implement response metadata (file type, size, processing time)
- [ ] Add Azure Application Insights integration
- [ ] Create deployment scripts

## Low Priority
- [ ] Add support for additional file types:
  - [ ] Images with OCR
  - [ ] Audio files with transcription
  - [ ] EPub documents
  - [ ] ZIP files
- [ ] Implement caching mechanism for frequently accessed documents
- [ ] Add authentication mechanism for API
- [ ] Create a simple web interface for file upload
- [ ] Add Swagger/OpenAPI documentation

## Completed
- [x] Create initial repository
- [x] Document project setup and API usage in README.md