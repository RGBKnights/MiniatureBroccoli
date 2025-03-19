import os
import hashlib
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from markitdown import MarkItDown
# import openai
from openai import OpenAI

# Constants
MAX_FILE_SIZE = os.environ.get("MAX_CONTENT_LENGTH", None)
if MAX_FILE_SIZE != None: MAX_FILE_SIZE = int(MAX_FILE_SIZE)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
LOG_FOLDER = "logs"
ERROR_LOG_FOLDER = "error_logs"

# LLM Settings
LLM_API_KEY = os.environ.get("LLM_API_KEY", None)
LLM_API_MODEL = os.environ.get("LLM_API_MODEL", "gemini-1.5-flash")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(ERROR_LOG_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
CORS(app)  # Enable CORS for all routes


def generate_unique_filename(file_stream, filename):
    """Generate a unique filename based on file content and timestamp."""
    file_stream.seek(0)  # Ensure reading from the beginning
    md5_hash = hashlib.md5(file_stream.read()).hexdigest()
    file_stream.seek(0)  # Reset file pointer
    ext = filename.rsplit(".", 1)[-1].lower()
    timestamp = int(time.time())  # Get current timestamp
    return f"{md5_hash}_{timestamp}.{ext}"


def log_conversion(filename, file_size):
    """Log the file conversion details."""
    file_size_mb = file_size / (1024 * 1024)  # Convert size to MB
    log_filename = time.strftime("%Y-%m-%d") + ".txt"
    log_path = os.path.join(LOG_FOLDER, log_filename)
    
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Filename: {filename}, Size: {file_size_mb:.2f} MB\n")


def log_error(message):
    """Log an error message."""
    error_log_path = os.path.join(ERROR_LOG_FOLDER, f"{time.strftime('%Y-%m-%d')}.txt")
    with open(error_log_path, "a", encoding="utf-8") as error_log_file:
        error_log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")


# def validate_api_key(api_key):
#     """Validate the OpenAI API key."""
#     if not api_key:
#         return None
    
#     client = OpenAI(api_key=api_key)
#     try:
#         client.models.retrieve("gpt-4o")
#         return client
#     except openai.APIError as e:
#         log_error(f"API Key validation failed: {e.body['message']}")
#         return None


def cleanup_files(*file_paths):
    """Remove files after processing."""
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.route("/convert", methods=["POST"])
def convert_file():
    """Handle file conversion to Markdown."""
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # api_key = request.form.get('APIKey', None)
    api_key = LLM_API_KEY
    client = None
    if api_key:
        client = OpenAI(
            api_key=api_key,
            base_url=LLM_BASE_URL
        )

    markitdown = MarkItDown(llm_client=client, llm_model=LLM_API_MODEL) if client else MarkItDown()

    try:
        # Generate logs and unique filename
        log_conversion(file.filename, os.fstat(file.stream.fileno()).st_size)
        unique_filename = generate_unique_filename(file.stream, file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        output_path = os.path.join(OUTPUT_FOLDER, unique_filename.rsplit(".", 1)[0] + ".md")

        # Save the uploaded file
        file.save(file_path)

        # Convert the file to Markdown
        result = markitdown.convert(file_path)
        if not result or not hasattr(result, "text_content"):
            raise ValueError("Conversion failed: No content extracted")

        # Write the Markdown content to a file
        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write(result.text_content)

        # Read and return Markdown content
        with open(output_path, "r", encoding="utf-8") as output_file:
            markdown_content = output_file.read()

        # Clean up files after processing
        cleanup_files(file_path, output_path)

        return jsonify({"message": "Conversion successful", "content": markdown_content}), 200

    except BaseException as e:
        cleanup_files(file_path, output_path)
        log_error(f"Failed to convert file: {str(e)}")
        return jsonify({"error": f"Failed to convert file: {str(e)}"}), 500


if __name__ == "__main__":
    app.run()