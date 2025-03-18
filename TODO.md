# Azure Function Markitdown - TODO List

## Azure Function Implementation

- [x] Set up basic python Azure Function project structure
- [x] Implement file upload in API endpoint
- [] Integrate markitdown Python package use [all] option

Example:

```
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=True) # Set to True to enable plugins
result = md.convert("test.xlsx")
print(result.text_content)
```
