from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import extractor
import verifier

app = FastAPI(title="TruthBot API")

# 1. Enable CORS for External Website Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your specific website domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "TruthBot AI is ready."}

@app.post("/verify")
async def verify_document(file: UploadFile = File(...)):
    """
    Endpoint to upload PDF or Image.
    Returns JSON: { "status": "APPROVED" | "FALSE", "reason": "..." }
    """
    try:
        # 1. Read File
        file_bytes = await file.read()
        
        # 2. Extract Text (OCR or PDF parsing)
        extracted_text = extractor.extract_text(file.filename, file_bytes)
        
        print(f"Extracted Text: {extracted_text[:100]}...") # Debug log

        if not extracted_text.strip():
            return {
                "status": "FALSE", 
                "reason": "Could not read any text from this file. It might be blurry or empty."
            }

        # 3. Verify with DeepSeek (Hugging Face)
        result = verifier.verify_content(extracted_text)
        
        return result

    except Exception as e:
        return {"status": "Error", "reason": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)