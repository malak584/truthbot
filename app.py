from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import extractor
import verifier
import shutil
import os

app = FastAPI(title="TruthBot API", description="AI-powered Fact Checking API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "TruthBot API is running"}

@app.post("/verify")
async def verify_document(file: UploadFile = File(...)):
    """
    Upload a file (PDF, Image, Text) to verify its content.
    Uses Google Gemini for fact-checking.
    """
    try:
        # Read file content
        file_bytes = await file.read()
        filename = file.filename.lower()
        
        # Check if it's an image - send directly to DeepSeek for OCR + verification
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')):
            result = verifier.verify_content_with_image(image_bytes=file_bytes)
            return result
        
        # For PDF and text files, extract text first
        text = extractor.extract_text(file.filename, file_bytes)
        
        if not text.strip():
            return JSONResponse(
                status_code=400,
                content={
                    "verified": False, 
                    "percentage": 0,
                    "errors": ["No text could be extracted from the file."], 
                    "analysis": "Empty or unreadable file."
                }
            )

        # Verify content with Google Gemini
        result = verifier.verify_content(text)
        
        return result

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "verified": False, 
                "percentage": 0,
                "errors": [str(e)], 
                "analysis": "Internal Server Error"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
