# 🛡️ TruthBot AI - Advanced Fact Verification System

An AI-powered fact-checking application using **Ollama (Qwen)** for local LLM processing and **Serper API** for web-based fact verification.

## ✨ Features

- 📄 **Multi-Format Support**: PDF, Images (PNG, JPG, JPEG), and Text files
- 🤖 **Local AI Engine**: Ollama with Qwen model - no cloud dependency
- 🔍 **Web Search Integration**: Serper API for real-time fact validation
- 📊 **Accuracy Scoring**: 0-100% percentage-based verification
- 🎨 **Beautiful UI**: Modern, responsive design with drag-and-drop
- 🖼️ **Image Analysis**: OCR and image-based fact verification
- ⚡ **Fast Processing**: Efficient local processing combined with API integration

## 🏗️ Project Structure

```
truthbot/
├── app/
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── verifier.py          # Qwen AI & Serper verification logic
│   └── utils/
│       ├── __init__.py
│       ├── extractor.py         # Text extraction (PDF, OCR)
│       └── search.py            # Serper API integration
├── static/                      # Static assets
├── templates/
│   └── index.html               # Main web interface
├── app.py                       # FastAPI application
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the root directory:

```env
OLLAMA_MODEL=qwen
OLLAMA_BASE_URL=http://localhost:11434
SERPER_API_KEY=your_serper_api_key_here
```

### 4. Start Ollama Service

**Option A - Using batch file (Windows):**
```bash
.\start_ollama.bat
```

**Option B - Command line:**
```bash
ollama run qwen
```

Keep this terminal open while using the API.

### 5. Start the API Server

Open a **new** terminal and navigate to your project directory:
```bash
cd path/to/truthbot
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access the Application

- **Web UI**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📋 Requirements

- Python 3.8+
- Ollama installed and running
- Serper API Key (https://serper.dev)
- Tesseract OCR binary (required for image text extraction)
- Windows/Mac/Linux

### Installing Ollama

**Windows & Mac:**
1. Download from https://ollama.ai
2. Run the installer
3. Ensure it's added to PATH

**Linux (Ubuntu/Debian):**
```bash
curl https://ollama.ai/install.sh | sh
```

### Installing Tesseract OCR

Tesseract is required for image text extraction (OCR). Installing only the Python package isn't enough—you need the binary.

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (recommend default path: `C:\Program Files\Tesseract-OCR`)
3. Verify installation:
```bash
tesseract --version
```

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install tesseract
```

### Downloading Models

You need to download two models for full functionality:

**Qwen Model** (for text analysis):
```bash
ollama pull qwen:7b
```
Downloads ~2.3GB. Used for general text fact-checking. **Note:** Always specify `qwen:7b` to ensure correct model version.

**LLaVA Model** (for image analysis - optional):
```bash
ollama pull llava
```
Downloads ~4.7GB. Required only if you want image verification with OCR. Skip if you only need text analysis.

## 🔧 API Endpoints

### `GET /health`

Check service health and configuration.

**Response:**
```json
{
    "status": "healthy",
    "service": "TruthBot AI",
    "version": "3.0.0",
    "ai_engine": "qwen",
    "search_engine": "Serper.dev"
}
```

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
    "analysis": "Detailed fact-checking analysis...",
    "errors": []
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/verify \
  -F "file=@document.pdf"
```

### `POST /verifyimage`

Verify an image file specifically.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (PNG, JPG, or JPEG image)

**Response:** Same as `/verify`

**Example:**
```bash
curl -X POST http://localhost:8000/verifyimage \
  -F "file=@screenshot.png"
```

## 🎯 How It Works

1. **Upload**: User uploads a document via web UI or API
2. **Extract**: Text is extracted from PDF/images
3. **Analyze**: Qwen AI analyzes claims for factual accuracy
4. **Search**: Serper API validates claims against web sources
5. **Report**: Detailed results with percentage score and analysis
6. **Display**: Beautiful UI shows results with visual feedback

## 🌟 Key Features Explained

### Local Processing
- All AI processing happens locally using Ollama
- No data sent to cloud (except Serper search queries)
- Complete privacy for sensitive documents

### Web Verification
- Serper API provides real-time web search results
- Cross-references claims against multiple sources
- Combines AI analysis with factual data

### Multi-Format Support
| Format | Support | Method |
|--------|---------|--------|
| PDF | ✅ | Text extraction |
| TXT | ✅ | Direct parsing |
| PNG | ✅ | OCR + analysis |
| JPG | ✅ | OCR + analysis |
| JPEG | ✅ | OCR + analysis |

## 🔧 Configuration

### Environment Variables

Edit `.env` to customize:

```env
# Ollama Configuration
OLLAMA_MODEL=qwen              # Model to use
OLLAMA_BASE_URL=http://localhost:11434  # Ollama server

# Search Configuration
SERPER_API_KEY=xxxxx           # Get from https://serper.dev

# Optional
UPLOAD_DIR=./uploads           # Temporary file storage
MAX_FILE_SIZE=10485760         # 10MB in bytes
```

### Advanced Settings

You can modify these in `app.py`:
- Port: Change port 8000 to your preferred port
- Host: Change 0.0.0.0 to restrict access
- CORS settings: Modify `allow_origins` for security

## 🧪 Testing

### Test with Python Script
```bash
python test_api.py
```

### Test with curl
```bash
# Create a test file
echo "The capital of France is London." > test.txt

# Send to API
curl -X POST http://localhost:8000/verify \
  -F "file=@test.txt"
```

### Test via Web UI
1. Open http://localhost:8000
2. Click "Choose File" and select a document
3. Click "Verify"
4. Wait for analysis to complete
5. Review results

## 🐛 Troubleshooting

### Issue: "Connection refused" or Ollama not found
**Solution:**
```bash
# Check if Ollama is running
ollama serve

# Or run the batch file
.\start_ollama.bat
```

### Issue: Model not found error
**Solution:**
```bash
# Download the model
ollama pull qwen

# Verify it's installed
ollama list
```

### Issue: Serper API errors
**Solution:**
1. Verify API key in `.env` is correct
2. Check Serper account has credits
3. Test key directly at https://serper.dev/dashboard

### Issue: File upload fails
**Solution:**
- Ensure file format is supported
- Check file size is under limit
- Verify temp directory permissions

### Issue: Tesseract path error on different systems
**Solution:**
- Tesseract installation path varies by OS and installation method
- If using default installation on Windows, the path should be auto-detected
- If you get "Tesseract not found" errors on Linux/macOS, pytesseract may not detect it:
```python
# In your code, add before importing pytesseract:
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
# pytesseract.pytesseract.pytesseract_cmd = '/usr/bin/tesseract'  # Linux
# pytesseract.pytesseract.pytesseract_cmd = '/opt/homebrew/bin/tesseract'  # M1 Mac
```

## 📊 Performance Tips

- **First Run**: Model loading takes 10-30 seconds
- **Subsequent Runs**: 2-5 seconds per document
- **GPU**: 5-10x faster with NVIDIA GPU support
- **Large Files**: Split into smaller chunks for faster processing

## 🚀 Deployment

### Local Network
```bash
# Make accessible from other machines
python app.py  # Already binds to 0.0.0.0:8000
# Access from another machine: http://<your-ip>:8000
```

### Docker (Optional)
```bash
# Build
docker build -t truthbot .

# Run
docker run -p 8000:8000 truthbot
```

## 📝 Version History

**v3.0.0** (Current)
- Ollama + Serper integration
- Image verification support
- Enhanced error handling

**v2.0.0**
- Google Gemini integration
- Web UI improvements

**v1.0.0**
- Initial release

## 🤝 Contributing

Contributions welcome! Please:
1. Test your changes locally
2. Update documentation
3. Submit pull requests

## 📄 License

MIT License - Feel free to use and modify!

## 🆘 Support

For issues or questions:
1. Check TROUBLESHOOTING.md for common problems
2. Review console output for error details
3. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Your environment (OS, Python version, etc.)

---

**Powered by Ollama + Qwen + Serper API** 🚀
