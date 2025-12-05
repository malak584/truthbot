# 🛡️ TruthBot AI - Advanced Fact Verification System

An AI-powered fact-checking application using **Google Gemini** for comprehensive document verification.

## ✨ Features

- 📄 **Multi-Format Support**: PDF, Images (PNG, JPG, JPEG), and Text files
- 🤖 **Google Gemini AI**: Advanced fact-checking with detailed analysis
- 📊 **Accuracy Scoring**: 0-100% percentage-based verification
- 🎨 **Beautiful UI**: Modern, responsive design with drag-and-drop
- 🔍 **Detailed Analysis**: Comprehensive explanations and error detection
- 🖼️ **OCR Support**: Direct image-to-text verification using Gemini Vision

## 🏗️ Project Structure

```
truthbot/
├── app/
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── verifier.py          # Gemini AI verification logic
│   └── utils/
│       ├── __init__.py
│       └── extractor.py          # Text extraction (PDF, OCR)
├── static/
│   ├── css/                      # Static CSS files (future)
│   └── js/                       # Static JS files (future)
├── templates/
│   └── index.html                # Main web interface
├── app.py                        # FastAPI application
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (API keys)
└── README.md                     # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create or edit `.env` file:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 3. Run the Application

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the Application

- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📋 Requirements

- Python 3.8+
- Google Gemini API Key
- Tesseract OCR (for image text extraction)

### Installing Tesseract

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

## 🔧 API Endpoints

### `POST /verify`

Upload a document for fact verification.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (PDF, Image, or Text file)

**Response:**
```json
{
    "verified": true,
    "percentage": 95,
    "summary": "The content is factually accurate",
    "analysis": "Detailed analysis of the claims...",
    "errors": []
}
```

### `GET /health`

Check service health and configuration.

**Response:**
```json
{
    "status": "healthy",
    "service": "TruthBot AI",
    "version": "2.0.0",
    "ai_engine": "Google Gemini"
}
```

## 🎯 How It Works

1. **Upload**: User uploads a document via web UI or API
2. **Extract**: Text is extracted from PDF/images using PyPDF2 or Tesseract OCR
3. **Verify**: Google Gemini AI analyzes the content for factual accuracy
4. **Report**: Detailed results with percentage score, analysis, and errors
5. **Display**: Beautiful UI shows results with color-coded feedback

## 🌟 Improvements in v2.0

✅ **Proper FastAPI Structure**: Organized code with services, utils, and routers  
✅ **Gemini 2.5 Flash**: Using the latest stable Gemini model (Dec 2024)  
✅ **Enhanced UI**: Modern gradient design with drag-and-drop support  
✅ **Better Analysis**: Percentage scoring, detailed explanations, error lists  
✅ **Improved Error Handling**: Comprehensive validation and error messages  
✅ **Vision Support**: Direct image verification using Gemini Vision  
✅ **Health Checks**: Monitoring and service status endpoints  

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Please open issues or submit pull requests.

---

**Powered by Google Gemini 2.5 Flash** 🚀 - AI Fact-Checking API

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
