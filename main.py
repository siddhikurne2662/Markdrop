import os
from pathlib import Path
import tempfile
from typing import Dict, Any

from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from markitdown import MarkItDown

app = FastAPI(title="MarkDrop API", version="1.0.4")

# CORS Configuration - Allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls", ".csv", ".html", ".htm",
    ".txt", ".md", ".json", ".xml", ".zip", ".jpg", ".jpeg", ".png", ".gif", ".webp",
    ".mp3", ".wav", ".m4a"
}

@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/convert")
async def convert_file(file: UploadFile = File(...)) -> JSONResponse:
    """
    Endpoint to convert uploaded files to Markdown.
    Validates extension and size, performs conversion using MarkItDown,
    and returns metadata along with the Markdown content.
    """
    filename = file.filename or "file"
    file_path_obj = Path(filename)
    extension = file_path_obj.suffix.lower()

    # 1. Validate file extension
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extension '{extension}'. Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    # 2. Validate file size
    # Check size by seeking to the end of the file object
    try:
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not determine file size: {str(e)}"
        )

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size ({file_size} bytes) exceeds the maximum allowed limit of 50MB."
        )

    # 3. Write to temporary file preserving extension
    temp_file = None
    tmp_path = None
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
        tmp_path = temp_file.name
        
        # Read uploaded file content in chunks and write to tempfile
        while chunk := await file.read(1024 * 1024):  # 1MB chunk size
            temp_file.write(chunk)
        temp_file.close()

        # 4. Convert file using MarkItDown
        md = MarkItDown()
        result = md.convert(tmp_path)
        content = result.text_content

        # 5. Validate empty content
        if not content or not content.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="File was parsed successfully but yielded no markdown content."
            )

        # Calculate counts
        char_count = len(content)
        line_count = len(content.splitlines())
        stem_md_name = f"{file_path_obj.stem}.md"

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "filename": stem_md_name,
                "original_filename": filename,
                "content": content,
                "char_count": char_count,
                "line_count": line_count
            }
        )

    except HTTPException as he:
        # Re-raise HTTPExceptions directly
        raise he
    except Exception as e:
        # Handle conversion errors or any other exception
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Conversion failed: {str(e)}"
        )
    finally:
        # 6. Delete tempfile in finally block
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

# Serve static files from './static' directory
# Ensure static folder exists
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index() -> FileResponse:
    """Serve static/index.html at root path."""
    return FileResponse("static/index.html")

@app.get("/{path:path}")
def serve_static_fallback(path: str) -> FileResponse:
    """
    Fallback route. If path is a file in static folder, serve it.
    Otherwise serve static/index.html to support single-page application routing.
    """
    if path:
        static_file = os.path.join("static", path)
        if os.path.isfile(static_file):
            return FileResponse(static_file)
    return FileResponse("static/index.html")
