from fastapi import FastAPI, UploadFile, File
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
    title="TruthBot AI - Local + Serper",
    description="Fact-checking using Ollama (Qwen) and Serper Dev",
    version="3.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "TruthBot AI",
        "version": "3.0.0",
        "ai_engine": os.getenv("OLLAMA_MODEL", "qwen"),
        "search_engine": "Serper.dev"
    }

@app.post("/verify")
async def verify_document(file: UploadFile = File(...)):
    try:
        allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.txt']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return JSONResponse(status_code=400, content={"error": "Invalid file type"})
        
        file_bytes = await file.read()
        
        # Image handling (Requires Multimodal model)
        if file_ext in ['.png', '.jpg', '.jpeg']:
            return verifier.verify_content_with_image(image_bytes=file_bytes)
        
        # Text/PDF handling
        text = extractor.extract_text(file.filename, file_bytes)
        if not text:
             return JSONResponse(status_code=400, content={"error": "No text extracted"})

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
                "analysis": "Internal Server Error",
                "summary": "Error"
            }
        )

@app.post("/verifyimage")
async def verify_image(file: UploadFile = File(...)):
    try:
        # Define allowed extensions
        allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.txt']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return JSONResponse(status_code=400, content={"error": "Invalid file type"})
        
        # Read file bytes once
        file_bytes = await file.read()
        
        # IMAGE HANDLING (LLaVA)
        if file_ext in ['.png', '.jpg', '.jpeg']:
            # This calls the updated function in verifier.py
            result = verifier.verify_content_with_image(image_bytes=file_bytes)
            return JSONResponse(content=result)
        
        # TEXT/PDF HANDLING
        text = extractor.extract_text(file.filename, file_bytes)
        if not text:
             return JSONResponse(status_code=400, content={"error": "No text extracted"})

        result = verifier.verify_content(text)
        return JSONResponse(content=result)

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "verified": False,
                "percentage": 0,
                "errors": [str(e)],
                "analysis": "Internal Server Error",
                "summary": "Error"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)