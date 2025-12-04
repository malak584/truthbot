# TruthBot - AI Fact-Checking API

An AI-powered fact-checking system that verifies uploaded content (documents, images, text) using Qwen AI and Google Search (via Serper API).

## Features
- 📄 **Multi-format Support**: PDF, Images (OCR), Text files
- 🔍 **Google Search Integration**: Uses Serper API for real-time fact verification
- 🤖 **Qwen AI Analysis**: Advanced language model for claim verification
- 🌐 **REST API**: Easy integration with any application
- 💻 **Web Demo**: Beautiful HTML interface included

## Setup Instructions

### 1. Install Dependencies
```bash
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start Ollama
**Option A - Double-click:**
- Run `start_ollama.bat`

**Option B - Command line:**
```bash
"C:\Users\khmal\AppData\Local\Programs\Ollama\ollama.exe" run qwen
```

Keep this terminal open while using the API.

### 3. Start the API Server
Open a **new** terminal:
```bash
cd c:\Users\khmal\Documents\truthbot
.\venv\Scripts\activate
uvicorn app:app --reload
```

### 4. Use the Demo
- Open `index.html` in your browser
- Upload any document, image, or text file
- Get instant fact-checking results!

## API Endpoint

### POST `/verify`
Upload a file to verify its content.

**Request:**
```bash
curl -X POST http://localhost:8000/verify \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "verified": true/false,
  "errors": ["list of specific errors if any"],
  "analysis": "detailed explanation..."
}
```

## Project Structure
```
truthbot/
├── app.py              # FastAPI server
├── verifier.py         # Fact-checking logic (Qwen + Serper)
├── extractor.py        # Text extraction (PDF, Image, Text)
├── index.html          # Web demo interface
├── requirements.txt    # Python dependencies
├── start_ollama.bat    # Helper to start Ollama
└── test_api.py         # API test script
```

## Technologies Used
- **FastAPI**: Modern Python web framework
- **Ollama + Qwen**: Local AI model for analysis
- **Serper API**: Google Search integration
- **Tesseract OCR**: Image text extraction
- **PyPDF2**: PDF parsing

## Notes
- Ensure Ollama is running before making API requests
- The Qwen model (~2.3GB) will be downloaded on first run
- Serper API key is configured in `verifier.py`
