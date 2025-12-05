from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import sys

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.utils import extractor
from app.services import verifier

app = FastAPI(
    title="TruthBot AI - Fact Verification API",
    description="AI-powered fact-checking using Google Gemini",
    version="2.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "TruthBot AI",
        "version": "2.0.0",
        "ai_engine": "Google Gemini"
    }

@app.post("/verify")
async def verify_document(file: UploadFile = File(...)):
    """
    Upload a file (PDF, Image, Text) to verify its content.
    Uses Google Gemini for comprehensive fact-checking.
    
    Returns:
        - verified: bool - Whether the content is accurate
        - percentage: int - Accuracy score (0-100)
        - analysis: str - Detailed explanation
        - errors: list - Any false or misleading claims found
        - summary: str - Brief summary of results
    """
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.txt']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return JSONResponse(
                status_code=400,
                content={
                    "verified": False,
                    "percentage": 0,
                    "errors": [f"Unsupported file type: {file_ext}. Please upload PDF, image, or text files."],
                    "analysis": "File type not supported for verification.",
                    "summary": "Invalid file format"
                }
            )
        
        # Read file content
        file_bytes = await file.read()
        
        if not file_bytes:
            return JSONResponse(
                status_code=400,
                content={
                    "verified": False,
                    "percentage": 0,
                    "errors": ["Empty file uploaded"],
                    "analysis": "The uploaded file appears to be empty.",
                    "summary": "No content to verify"
                }
            )
        
        # Check if it's an image - use Gemini Vision for direct OCR + verification
        if file_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp']:
            result = verifier.verify_content_with_image(image_bytes=file_bytes)
            return result
        
        # For PDF and text files, extract text first
        text = extractor.extract_text(file.filename, file_bytes)
        
        if not text or not text.strip():
            return JSONResponse(
                status_code=400,
                content={
                    "verified": False,
                    "percentage": 0,
                    "errors": ["No text could be extracted from the file"],
                    "analysis": "The file may be corrupted, password-protected, or contain no readable text.",
                    "summary": "Unable to extract text"
                }
            )

        # Verify content with Google Gemini
        result = verifier.verify_content(text)
        
        return result

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "verified": False,
                "percentage": 0,
                "errors": [str(e)],
                "analysis": "An unexpected error occurred during verification. Please try again.",
                "summary": "Internal server error"
            }
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting TruthBot AI Server...")
    print("📍 API: http://localhost:8000")
    print("🌐 Web UI: http://localhost:8000")
    print("📊 API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
