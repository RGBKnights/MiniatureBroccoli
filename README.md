#  Markitdown Web Server

Example:

```
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=True) # Set to True to enable plugins
result = md.convert("test.xlsx")
print(result.text_content)
```
